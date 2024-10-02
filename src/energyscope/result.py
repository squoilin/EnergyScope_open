from dataclasses import dataclass, field
import numpy as np
import pandas as pd


@dataclass
class Result:
    constraints: dict[str, pd.DataFrame] = field(default_factory=dict)
    parameters: dict[str, pd.DataFrame] = field(default_factory=dict)
    objectives: dict[str, pd.DataFrame] = field(default_factory=dict)
    sets: dict[str, pd.DataFrame] = field(default_factory=dict)
    variables: dict[str, pd.DataFrame] = field(default_factory=dict)
    postprocessing: dict[str, pd.DataFrame] = field(default_factory=dict)


    def __add__(self, other: 'Result') -> 'Result':
        def __concat(current: dict[str, pd.DataFrame], other: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
            merged = {}
            for name in current.keys() & other.keys():
                merged[name] = pd.concat([current[name], other[name]])
            for name in current.keys() - other.keys():
                merged[name] = current[name]
            for name in other.keys() - current.keys():
                merged[name] = other[name]
            return merged

        return Result(
            constraints=__concat(self.constraints, other.constraints),
            parameters=__concat(self.parameters, other.parameters),
            objectives=__concat(self.objectives, other.objectives),
            sets=__concat(self.sets, other.sets),
            variables=__concat(self.variables, other.variables),
            postprocessing=__concat(self.variables, other.variables),

        )


def parse_result(ampl, id_run=None, results_old=None) -> Result: 
    def _parse_set(ampl, name, set_) -> dict[str, pd.DataFrame]:
        if set_.is_scalar():
            return {name: set_.to_pandas().reset_index().rename(columns={'index': name})}
        else:
            result={name:{index[0]: index[1].get_values().toList() for index in ampl.get_set(name).instances()}}
            return result
        
    objectives = {name: objective.to_pandas().rename(columns=lambda v: v.rstrip('.val'))
                  for name, objective in ampl.get_objectives()}
    variables = {name: variable.to_pandas().rename(columns=lambda v: v.rstrip('.val'))
                 for name, variable in ampl.get_variables()}
    parameters = {name: parameter.to_pandas() for name, parameter in ampl.get_parameters()}
    sets = {}
    for name, set_ in ampl.get_sets():
        sets = {**sets, **_parse_set(ampl, name, set_)}

# If the solving of the model is not ideal we replace all results by 0 so that the rest of the optimizations continue,
#  to check which optimizations failed check the objectives results, OBJ = 0 means failed optimization
    if ampl.solve_result_num>99:
        for key in variables.keys():
            variables[key].loc[:,:]=0
        for key in parameters.keys():
            parameters[key].loc[:,:]=0
        for key in objectives.keys():
            objectives[key].loc[:,:]=0

    if id_run is not None:
        for _, value in objectives.items():
            value['Run'] = id_run
        for _, value in variables.items():
            value['Run'] = id_run
        for _, value in parameters.items():
            value['Run'] = id_run
        # for _, value in sets.items():
        #     value['Run'] = id_run

    # if results_old is not None:   # TODO implement the option to merge results in the parser
    #     variables = {name: pd.concat([results_old.variables[name], variables[name]]) for name in results_old.variables.keys()}
    #     parameters = {name: pd.concat([results_old.parameters[name], parameters[name]]) for name in results_old.parameters.keys()}

    return Result(
        objectives=objectives,
        variables=variables,
        parameters=parameters,
        sets=sets,
    )

def postprocessing(Result, df_monthly=True, df_annual=True) -> Result:
    """
        Performs post-processing of EnergyScope results by organizing and categorizing key metrics into annual and monthly dataframes.

        Parameters:
        ----------
        Result : object
            The result object containing the outputs of the model's run.

        df_monthly : bool, optional
            If True, the function processes and stores monthly results, including the flows of different technologies. Defaults to True.

        df_annual : bool, optional
            If True, the function processes and stores annual results, including investment costs, maintenance costs, production, and the economic lifetimes (tau) of technologies. Defaults to True.

        Returns:
        -------
        Result : object
            The updated Result object, containing the processed dataframes

        Processing Steps:
        -----------------
        - For annual results (`df_annual`), the function compiles investment costs, maintenance costs, annual production, and flow multipliers. It also calculates annualized investment costs based on the economic lifetime (`tau`).
        - For monthly results (`df_monthly`), it computes the monthly flows of technologies using flow multipliers, operating time, and layer factors (in/out ratios).
        - Both annual and monthly results are categorized into high-level sectors (e.g., Electricity, Mobility, Industry) and assigned `Category`, `Category_2`, and `Sector` labels.
        - Technologies that do not fit predefined categories are assigned the "Others" label.

        Sector-Technology Mapping:
        --------------------------
        The function uses predefined mappings between sectors (e.g., Electricity, Mobility, Industry) and their respective technologies to categorize the results accordingly.

        Examples:
        ---------
        - Annual Data:
        The function aggregates and processes investment costs (`C_inv`), maintenance costs (`C_maint`), and production (`Annual_Prod`), calculates annualized costs, and categorizes the data.
        - Monthly Data:
        It merges flow multipliers (`F_Mult_t`), operating time (`t_op`), and layer in-out factors (`layers_in_out`) to compute the monthly flows of technologies and their associated categories.
        """

    sector_technologies = {
        "Electricity": [
            "CCGT", "CCGT_CC", "COAL_US", "COAL_IGCC", "COAL_US_CC", "COAL_IGCC_CC", 
            "HYDRO_GAS_CHP", "NUCLEAR"
        ],
        "Mobility": [
            "TRAMWAY", "COACH_CNG_STOICH", "COACH_DIESEL", "COACH_EV", 
            "COACH_FC_HYBRID_H2", "COACH_FC_HYBRID_CH4", "COACH_HY_DIESEL", 
            "COMMUTER_RAIL_DIESEL", "COMMUTER_RAIL_ELEC", "TRAIN_DIESEL", 
            "TRAIN_ELEC", "TRAIN_NG", "TRAIN_H2", "BUS_CNG_STOICH", "BUS_DIESEL", 
            "BUS_FC_HYBRID_H2", "BUS_FC_HYBRID_CH4", "BUS_HY_DIESEL", "BUS_EV", 
            "CAR_BEV_LOWRANGE", "CAR_BEV_MEDRANGE_LOCAL", "CAR_DIESEL_LOCAL", 
            "CAR_DME_D10_LOCAL", "CAR_ETOH_E10_LOCAL", "CAR_ETOH_E85_LOCAL", 
            "CAR_FC_H2_LOCAL", "CAR_FC_CH4_LOCAL", "CAR_GASOLINE_LOCAL", 
            "CAR_HEV_LOCAL", "CAR_MEOH_LOCAL", "CAR_NG_LOCAL", "CAR_PHEV_LOCAL", 
            "CAR_BEV_MEDRANGE_LONGD", "CAR_DIESEL_LONGD", "CAR_DME_D10_LONGD", 
            "CAR_ETOH_E10_LONGD", "CAR_ETOH_E85_LONGD", "CAR_FC_H2_LONGD", 
            "CAR_FC_CH4_LONGD", "CAR_GASOLINE_LONGD", "CAR_HEV_LONGD", "CAR_HEV", 
            "CAR_MEOH_LONGD", "CAR_NG_LONGD", "CAR_PHEV_LONGD", "TRAIN_FREIGHT", 
            "TRAIN_FREIGHT_DIESEL", "TRAIN_FREIGHT_NG", "TRAIN_FREIGHT_H2", 
            "TRUCK", "TRUCK_CO2", "TRUCK_EV", "TRUCK_SNG", "TRUCK_FC", "PLANE",
            "CAR_GASOLINE", "CAR_DIESEL", "CAR_NG", "CAR_PHEV", "CAR_MEOH", "CAR_FC_H2", "CAR_FC_CH4", "CAR_BEV_MEDRANGE", "CAR_ETOH_E10", "CAR_ETOH_E85", "CAR_DME_D10"
        ],
        "Electric Infrastructure": [
            "TRAFO_ML", "TRAFO_LM", "TRAFO_HM", "TRAFO_MH", "TRAFO_EH", "TRAFO_HE",
            "EHV_GRID", "HV_GRID", "MV_GRID", "LV_GRID","GRID"
        ],
        "Gas Infrastructure": [
            "EHP_H2_GRID", "HP_H2_GRID", "MP_H2_GRID", "LP_H2_GRID",
            "EHP_NG_GRID", "HP_NG_GRID", "MP_NG_GRID", "LP_NG_GRID",
            "NG_EXP_EH", "NG_EXP_HM", "NG_EXP_ML", "NG_EXP_EH_COGEN", "NG_EXP_HM_COGEN", "NG_EXP_ML_COGEN",
            "NG_COMP_HE", "NG_COMP_MH", "NG_COMP_LM",
            "H2_EXP_EH", "H2_EXP_HM", "H2_EXP_ML", "H2_EXP_EH_COGEN", "H2_EXP_HM_COGEN", "H2_EXP_ML_COGEN",
            "H2_COMP_HE", "H2_COMP_MH", "H2_COMP_LM"
        ],
        "Wind": ["WIND"],
        "PV": ["PV_LV", "PV_MV", "PV_HV", "PV_EHV"],
        "Geothermal": ["GEOTHERMAL", "DHN_DEEP_GEO", "DEC_DEEP_GEO"],
        "Hydro River & Dam": ["NEW_HYDRO_RIVER", "NEW_HYDRO_DAM", "HYDRO_RIVER", "HYDRO_DAM"],
        "Industry": [
             "AL_MAKING", "AL_MAKING_HR", "CEMENT_PROD", 
            "CEMENT_PROD_HP", "FOOD_PROD", "FOOD_PROD_HP", "FOOD_PROD_HR", "PAPER_MAKING", 
            "PAPER_MAKING_HP", "PAPER_MAKING_HR", "STEEL_MAKING", "STEEL_MAKING_HP", 
            "STEEL_MAKING_HR", "WOOD_METHANOL", "CO2_METHANOL", "METHANOL_FT", 
            "METHANE_TO_METHANOL", "CUMENE_PROCESS", "METHANOL_CARBONYLATION", 
            "ETHANE_OXIDATION", "ETHYLENE_POLYMERIZATION", "PET_FORMATION", 
            "PVC_FORMATION", "POLYPROPYLENE_PP", "STYRENE_POLYMERIZATION",
            "HYDRO_GAS","AN_DIG_SI","BIOMASS_ETHANOL","FT","AN_DIG", "SNG_NG",
            "EFFICIENCY", "METHANATION","GASIFICATION_SNG", "PYROLYSIS","NG_REFORMING",
            "METHANOL_TO_AROMATICS","METHANOL_TO_OLEFINS","CO2-To-Diesel","ETHANE_CRACKING",
            "METATHESIS_PROPYLENE","SMART_PROCESS","CROPS_TO_JETFUELS","CO2_TO_JETFUELS",
            "BIOGAS_BIOMETHANE","CROPS_TO_ETHANOL","ETHANE_TO_ETHYLENE","ETHANOL_TO_JETFUELS"
            ,"GASIFICATION_H2","OTHER_BIOMASS","EOR","DOGR","UNMINEABLE_COAL_SEAM","DEEP_SALINE",
            "MINES_STORAGE","DIRECT_USAGE","CEMENT"
        ],
        "Low Temperature Heat": [
            "DHN_HP_ELEC", "DHN_COGEN_GAS", "DHN_COGEN_WOOD", "DHN_COGEN_WASTE", 
            "DHN_BOILER_GAS", "DHN_BOILER_WOOD", "DHN_BOILER_OIL", "DHN_RENOVATION", 
            "DEC_HP_ELEC", "DEC_THHP_GAS", "DEC_COGEN_GAS", "DEC_COGEN_OIL", 
            "DEC_COGEN_WOOD", "DEC_ADVCOGEN_H2", "DEC_BOILER_GAS", "DEC_BOILER_WOOD", 
            "DEC_BOILER_OIL", "DEC_SOLAR", "DEC_DIRECT_ELEC", "DEC_RENOVATION","DHN",
            "LT_DEC_WH", "LT_DHN_WH", "HT_LT", "HT_LT_DEC",
        ],
        "High Temperature Heat": 
        ["IND_COGEN_GAS", "IND_COGEN_WOOD", "IND_COGEN_WASTE", "IND_BOILER_GAS", 
            "IND_BOILER_WOOD", "IND_BOILER_OIL", "IND_BOILER_COAL", "IND_BOILER_WASTE", 
            "IND_HP_ELEC", "IND_DIRECT_ELEC"],
        "Storage": [
            "DIE_STO", "STO_DIE", "GASO_STO", "STO_GASO", "ELEC_STO", "STO_ELEC", 
            "H2_STO", "STO_H2", "CO2_STO", "STO_CO2", "NG_STO", "STO_NG",
            "DHN_TH_STORAGE", "DEC_TH_STORAGE","BATTERY",""
        ],
        "Electrolysis": [
            "ALKALINE_ELECTROLYSIS", "PEM_ELECTROLYSIS", "SOEC_ELECTROLYSIS"
        ],
        "Carbon Capture": ["CARBON_CAPTURE","DAC_HT", "DAC_LT"]
        #"Car Fuel Types": [ "CAR_GASOLINE", "CAR_DIESEL", "CAR_NG", "CAR_PHEV", "CAR_MEOH", "CAR_FC_H2", "CAR_FC_CH4", "CAR_BEV_MEDRANGE", "CAR_ETOH_E10", "CAR_ETOH_E85", "CAR_DME_D10"]
    }

    if df_annual:
        # df_annual
        df_ = [
        Result.variables['C_inv'].set_index('Run',append=True),
        Result.variables['C_maint'].set_index('Run',append=True),
        Result.variables['Annual_Prod'].set_index('Run',append=True),
        Result.variables['F_Mult'].set_index('Run',append=True),
        Result.parameters['tau'].set_index('Run',append=True),
        ]
        df_ = pd.concat(df_, axis=1, join="inner").loc[:,~pd.concat(df_, axis=1).columns.duplicated()]
        df_.rename(columns={'C_in':'C_inv'},inplace=True)
        df_['C_inv_an'] = df_['C_inv'] * df_['tau']

        ## Add categories
        df_['Category'] = df_.index.to_series().apply(lambda x: next((k for k, v in Result.sets['TECHNOLOGIES_OF_END_USES_TYPE'].items() if x[0] in v), pd.NA))
        df_["Category_2"] = df_.index.get_level_values(0).map({tech: sector for sector, techs in sector_technologies.items() for tech in techs})
        df_['Sector'] = pd.Series(dtype='str')
        df_.loc[df_['Category'].str.contains('MOB_',na=False),'Sector'] = 'Mobility'
        df_.loc[df_['Category'].str.contains('ELECTRICITY_',na=False),'Sector'] = 'Electricity'
        df_.loc[df_['Category'].str.contains('HEAT_HIGH',na=False),'Sector'] = 'Industrial Heat'
        df_.loc[df_['Category'].str.contains('HEAT_LOW',na=False),'Sector'] = 'Domestic Heat'
        
        Industry_list = ['METHANOL','ALUMINUM','PHENOL','ACETIC_ACID','ACETONE','PE','PET','PVC','PP','PS','CEMENT','FOOD','PAPER','STEEL']
        df_.loc[df_['Category'].isin(Industry_list),'Sector'] = 'Industry'
        df_.loc[df_.loc[:,'Category'].isna(),'Sector'] = 'Others'

        ## Fill missing category with "Others"
        df_.loc[df_['Category'].isna(),'Category'] = 'Others'
        df_.loc[df_['Category_2'].isna(),'Category_2'] = 'Others'

        Result.postprocessing['df_annual'] = df_

    if df_monthly:
        # df_monthly

        F_Mult_t = Result.variables['F_Mult_t'].reset_index().rename(
            columns={"index0": "Technologies", "index1": "Periods"})

        lyrio = Result.parameters['layers_in_out'].reset_index().rename(
            columns={"index0": "Technologies", "index1": "Flow"})
        lyrio = lyrio.loc[lyrio['layers_in_out']!=0,:]  # Drop useless rows, lighten the postprocessing

        t_op = Result.parameters['t_op'].reset_index().rename(columns={'index':'Periods'})

        F_Mult_t = F_Mult_t[F_Mult_t['F_Mult_t']!=0]

        df_ = pd.merge(F_Mult_t,t_op,on=["Periods",'Run'])
        df_ = pd.merge(df_,lyrio,on=["Technologies",'Run'])

        df_['Monthly_flow']=df_['F_Mult_t']*df_['t_op']*df_['layers_in_out']

        # Drop row without information, ie. not production
        df_ = df_.loc[df_['layers_in_out']!=0,:]

        ## Add categories
        df_['Category'] = df_['Technologies'].apply(lambda x: next((k for k, v in Result.sets['TECHNOLOGIES_OF_END_USES_TYPE'].items() if x in v), pd.NA))

        # Assign 'Category_2' based on mapping 'Technologies' to sectors
        df_["Category_2"] = df_['Technologies'].map({tech: sector for sector, techs in sector_technologies.items() for tech in techs})
        df_['Sector'] = pd.Series(dtype='str')
        df_.loc[df_['Flow'].str.contains('MOB_',na=False),'Sector'] = 'Mobility'
        df_.loc[df_['Flow'].str.contains('ELECTRICITY_',na=False),'Sector'] = 'Electricity'
        df_.loc[df_['Flow'].str.contains('HEAT_HIGH',na=False),'Sector'] = 'Industrial Heat'
        df_.loc[df_['Flow'].str.contains('HEAT_LOW',na=False),'Sector'] = 'Domestic Heat'

        ## Fill missing category with "Others"
        df_.loc[df_['Category'].isna(),'Category'] = 'Others'
        df_.loc[df_['Category_2'].isna(),'Category_2'] = 'Others'
        df_.loc[df_['Sector'].isna(),'Sector'] = 'Others'

        Result.postprocessing['df_monthly'] = df_

    return Result
