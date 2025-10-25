"""
Energyscope Full Model implemented in PyOptInterface.
This implementation matches the AMPL model structure.
"""

import pyoptinterface as poi
from pyoptinterface import gurobi
import pandas as pd
from energyscope.linopy_backend.data_loader_full import create_full_dataset

def build_and_run_full_model():
    """
    Builds and solves the Energyscope full model using pyoptinterface.
    """
    print("="*70)
    print("Building and running PyOptInterface full model")
    print("="*70)

    # 1. Load data
    data = create_full_dataset()
    print("  Full ESTD data loaded.")

    # Extract sets and parameters
    TECHNOLOGIES = data['sets']['TECHNOLOGIES']
    STORAGE_TECH = data['sets']['STORAGE_TECH']
    RESOURCES = data['sets']['RESOURCES']
    LAYERS = data['sets']['LAYERS']
    HOURS = data['sets']['HOURS']
    TYPICAL_DAYS = data['sets']['TYPICAL_DAYS']
    PERIODS = data['sets']['PERIODS']
    T_H_TD = data['sets']['T_H_TD']
    END_USES_TYPES = data['sets']['END_USES_TYPES']
    END_USES_INPUT = data['sets'].get('END_USES_INPUT', [])
    END_USES_CATEGORIES = data['sets'].get('END_USES_CATEGORIES', [])
    TECHNOLOGIES_OF_END_USES_CATEGORY = data['sets'].get('TECHNOLOGIES_OF_END_USES_CATEGORY', {})
    TECHNOLOGIES_OF_END_USES_TYPE = data['sets'].get('TECHNOLOGIES_OF_END_USES_TYPE', {})
    
    ALL_TECH = TECHNOLOGIES + STORAGE_TECH
    TECH_NOSTORAGE = [t for t in ALL_TECH if t not in STORAGE_TECH]
    ENTITIES_WITH_F_T = RESOURCES + TECH_NOSTORAGE

    # Extract parameters
    f_max = data['parameters']['f_max'].to_dict()
    f_min = data['parameters']['f_min'].to_dict()
    c_p_t = data['parameters']['c_p_t'].to_dict()
    layers_in_out = data['parameters']['layers_in_out'].to_dict()
    avail = data['parameters']['avail'].to_dict()
    t_op = data['parameters']['t_op'].to_dict()
    c_inv = data['parameters']['c_inv'].to_dict()
    c_maint = data['parameters']['c_maint'].to_dict()
    c_op = data['parameters']['c_op'].to_dict()
    lifetime = data['parameters']['lifetime'].to_dict()
    i_rate = data['parameters']['i_rate']
    gwp_constr_param = data['parameters']['gwp_constr'].to_dict()
    gwp_op_param = data['parameters']['gwp_op'].to_dict()
    gwp_limit_param = data['parameters'].get('gwp_limit', float('inf'))
    
    # Time series
    electricity_time_series = data['parameters']['electricity_time_series'].to_dict()
    heating_time_series = data['parameters']['heating_time_series'].to_dict()
    mob_pass_time_series = data['parameters'].get('mob_pass_time_series', {})
    mob_freight_time_series = data['parameters'].get('mob_freight_time_series', {})
    
    # End uses input data
    end_uses_input = {}
    if 'end_uses_demand_year' in data['parameters']:
        eud_year = data['parameters']['end_uses_demand_year']
        if isinstance(eud_year, pd.DataFrame):
            # Sum across sectors
            for eu in eud_year.index.get_level_values(0).unique():
                end_uses_input[eu] = eud_year.loc[eu].sum()
        elif isinstance(eud_year, pd.Series):
            if eud_year.index.nlevels > 1:
                # Has sectors dimension
                for eu in eud_year.index.get_level_values(0).unique():
                    end_uses_input[eu] = eud_year.loc[eu].sum()
            else:
                end_uses_input = eud_year.to_dict()
        else:
            end_uses_input = dict(eud_year)
    
    # Calculate total_time
    total_time = sum(t_op.get((h, td), 1.0) for h in HOURS for td in TYPICAL_DAYS)
    
    # Shares bounds
    share_mobility_public_min = data['parameters'].get('share_mobility_public_min', 0)
    share_mobility_public_max = data['parameters'].get('share_mobility_public_max', 1)
    share_freight_train_min = data['parameters'].get('share_freight_train_min', 0)
    share_freight_train_max = data['parameters'].get('share_freight_train_max', 1)
    share_freight_road_min = data['parameters'].get('share_freight_road_min', 0)
    share_freight_road_max = data['parameters'].get('share_freight_road_max', 1)
    share_freight_boat_min = data['parameters'].get('share_freight_boat_min', 0)
    share_freight_boat_max = data['parameters'].get('share_freight_boat_max', 1)
    share_heat_dhn_min = data['parameters'].get('share_heat_dhn_min', 0)
    share_heat_dhn_max = data['parameters'].get('share_heat_dhn_max', 1)
    
    # Storage parameters
    storage_eff_in = data['parameters'].get('storage_eff_in', pd.DataFrame()).to_dict() if 'storage_eff_in' in data['parameters'] else {}
    storage_eff_out = data['parameters'].get('storage_eff_out', pd.DataFrame()).to_dict() if 'storage_eff_out' in data['parameters'] else {}
    storage_losses = data['parameters'].get('storage_losses', pd.Series()).to_dict() if 'storage_losses' in data['parameters'] else {}
    
    # Loss network
    loss_network = data['parameters'].get('loss_network', {})
    if isinstance(loss_network, pd.Series):
        loss_network = loss_network.to_dict()

    # 2. Create a model
    model = gurobi.Model()
    print("  Model created with Gurobi backend.")

    # 3. Define variables
    print("  Creating variables...")
    
    # Main capacity variables
    F = {
        tech: model.add_variable(lb=f_min.get(tech, 0), ub=f_max.get(tech, float('inf')), name=f"F_{tech}")
        for tech in ALL_TECH
    }

    # Operational variables
    F_t = {
        (entity, h, td): model.add_variable(lb=0, name=f"F_t_{entity}_{h}_{td}")
        for entity in ENTITIES_WITH_F_T for h in HOURS for td in TYPICAL_DAYS
    }

    # Storage variables
    Storage_in, Storage_out, Storage_level = {}, {}, {}
    if STORAGE_TECH:
        Storage_in = {
            (s, l, h, td): model.add_variable(lb=0, name=f"Storage_in_{s}_{l}_{h}_{td}")
            for s in STORAGE_TECH for l in LAYERS for h in HOURS for td in TYPICAL_DAYS
        }
        Storage_out = {
            (s, l, h, td): model.add_variable(lb=0, name=f"Storage_out_{s}_{l}_{h}_{td}")
            for s in STORAGE_TECH for l in LAYERS for h in HOURS for td in TYPICAL_DAYS
        }
        Storage_level = {
            (s, t): model.add_variable(lb=0, name=f"Storage_level_{s}_{t}")
            for s in STORAGE_TECH for t in PERIODS
        }

    # Share variables (decision variables for modal split, DHN share, etc.)
    Share_mobility_public = model.add_variable(lb=share_mobility_public_min, ub=share_mobility_public_max, name="Share_mobility_public")
    Share_freight_train = model.add_variable(lb=share_freight_train_min, ub=share_freight_train_max, name="Share_freight_train")
    Share_freight_road = model.add_variable(lb=share_freight_road_min, ub=share_freight_road_max, name="Share_freight_road")
    Share_freight_boat = model.add_variable(lb=share_freight_boat_min, ub=share_freight_boat_max, name="Share_freight_boat")
    Share_heat_dhn = model.add_variable(lb=share_heat_dhn_min, ub=share_heat_dhn_max, name="Share_heat_dhn")
    
    # Shares for mobility technologies (constant share of demand for each technology)
    Shares_mobility_passenger = {}
    if 'MOBILITY_PASSENGER' in TECHNOLOGIES_OF_END_USES_CATEGORY:
        for tech in TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_PASSENGER']:
            Shares_mobility_passenger[tech] = model.add_variable(lb=0, name=f"Shares_mobility_passenger_{tech}")
    
    Shares_mobility_freight = {}
    if 'MOBILITY_FREIGHT' in TECHNOLOGIES_OF_END_USES_CATEGORY:
        for tech in TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_FREIGHT']:
            Shares_mobility_freight[tech] = model.add_variable(lb=0, name=f"Shares_mobility_freight_{tech}")
    
    # End_uses as VARIABLES (not fixed parameters!)
    End_uses = {
        (l, h, td): model.add_variable(lb=0, name=f"End_uses_{l}_{h}_{td}")
        for l in LAYERS for h in HOURS for td in TYPICAL_DAYS
    }
    
    # Network losses variables
    Network_losses = {
        (eut, h, td): model.add_variable(lb=0, name=f"Network_losses_{eut}_{h}_{td}")
        for eut in END_USES_TYPES for h in HOURS for td in TYPICAL_DAYS
    }
    
    # Cost and GWP variables
    TotalCost = model.add_variable(lb=0, name="TotalCost")
    TotalGWP = model.add_variable(lb=0, name="TotalGWP")

    print("  Variables created.")

    # 4. Add constraints
    print("  Adding constraints...")
    
    # Constraint: Freight shares must sum to 1 [Eq. 2.26]
    model.add_linear_constraint(Share_freight_train + Share_freight_road + Share_freight_boat == 1)
    
    # Constraint: End-uses demand calculation [Eq. 2.8 / Figure 2.8]
    print("    - End-uses demand calculation...")
    for l in LAYERS:
        for h in HOURS:
            for td in TYPICAL_DAYS:
                t_op_val = t_op.get((h, td), 1.0)
                
                # Build the end-use expression based on layer type
                if l == "ELECTRICITY":
                    # Electricity: base load + lighting profile
                    base = end_uses_input.get("ELECTRICITY", 0) / total_time if total_time > 0 else 0
                    lighting = end_uses_input.get("LIGHTING", 0) * electricity_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    model.add_linear_constraint(End_uses[l, h, td] == base + lighting)
                    
                elif l == "HEAT_LOW_T_DHN":
                    # DHN heat: (HW + SH profile) * DHN_share + network losses
                    hw = end_uses_input.get("HEAT_LOW_T_HW", 0) / total_time if total_time > 0 else 0
                    sh = end_uses_input.get("HEAT_LOW_T_SH", 0) * heating_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    model.add_linear_constraint(End_uses[l, h, td] == (hw + sh) * Share_heat_dhn + Network_losses[l, h, td])
                    
                elif l == "HEAT_LOW_T_DECEN":
                    # Decentralized heat: (HW + SH profile) * (1 - DHN_share)
                    hw = end_uses_input.get("HEAT_LOW_T_HW", 0) / total_time if total_time > 0 else 0
                    sh = end_uses_input.get("HEAT_LOW_T_SH", 0) * heating_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    model.add_linear_constraint(End_uses[l, h, td] == (hw + sh) * (1 - Share_heat_dhn))
                    
                elif l == "MOB_PUBLIC":
                    # Public mobility
                    mob_pass = end_uses_input.get("MOBILITY_PASSENGER", 0) * mob_pass_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    model.add_linear_constraint(End_uses[l, h, td] == mob_pass * Share_mobility_public)
                    
                elif l == "MOB_PRIVATE":
                    # Private mobility
                    mob_pass = end_uses_input.get("MOBILITY_PASSENGER", 0) * mob_pass_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    model.add_linear_constraint(End_uses[l, h, td] == mob_pass * (1 - Share_mobility_public))
                    
                elif l == "MOB_FREIGHT_RAIL":
                    # Rail freight
                    mob_freight = end_uses_input.get("MOBILITY_FREIGHT", 0) * mob_freight_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    model.add_linear_constraint(End_uses[l, h, td] == mob_freight * Share_freight_train)
                    
                elif l == "MOB_FREIGHT_ROAD":
                    # Road freight
                    mob_freight = end_uses_input.get("MOBILITY_FREIGHT", 0) * mob_freight_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    model.add_linear_constraint(End_uses[l, h, td] == mob_freight * Share_freight_road)
                    
                elif l == "MOB_FREIGHT_BOAT":
                    # Boat freight
                    mob_freight = end_uses_input.get("MOBILITY_FREIGHT", 0) * mob_freight_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    model.add_linear_constraint(End_uses[l, h, td] == mob_freight * Share_freight_boat)
                    
                elif l == "HEAT_HIGH_T":
                    # High temperature heat: constant
                    ht_demand = end_uses_input.get("HEAT_HIGH_T", 0) / total_time if total_time > 0 else 0
                    model.add_linear_constraint(End_uses[l, h, td] == ht_demand)
                    
                else:
                    # Other layers: zero demand
                    model.add_linear_constraint(End_uses[l, h, td] == 0)
    
    # Constraint: Network losses [Eq. 2.20]
    print("    - Network losses...")
    for eut in END_USES_TYPES:
        loss_pct = loss_network.get(eut, 0)
        if loss_pct > 0:
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    production = sum(
                        layers_in_out.get((entity, eut), 0) * F_t[entity, h, td]
                        for entity in ENTITIES_WITH_F_T
                        if layers_in_out.get((entity, eut), 0) > 0
                    )
                    model.add_linear_constraint(Network_losses[eut, h, td] == production * loss_pct)
        else:
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    model.add_linear_constraint(Network_losses[eut, h, td] == 0)
    
    # Constraint: Hourly capacity factor [Eq. 2.10]
    print("    - Hourly capacity factor...")
    for j in TECH_NOSTORAGE:
        for h in HOURS:
            for td in TYPICAL_DAYS:
                cf = c_p_t.get((j, h, td), 1.0)
                model.add_linear_constraint(F_t[j, h, td] <= F[j] * cf)

    # Constraint: Layer balance [Eq. 2.13]
    print("    - Layer balance...")
    for l in LAYERS:
        for h in HOURS:
            for td in TYPICAL_DAYS:
                balance_expr = sum(
                    layers_in_out.get((entity, l), 0) * F_t[entity, h, td]
                    for entity in ENTITIES_WITH_F_T
                )
                
                if STORAGE_TECH:
                    for s in STORAGE_TECH:
                        balance_expr += Storage_out[s, l, h, td] - Storage_in[s, l, h, td]
                
                model.add_linear_constraint(balance_expr == End_uses[l, h, td])

    # Constraint: Resources availability [Eq. 2.12]
    print("    - Resources availability...")
    for i in RESOURCES:
        if i in avail:
            if pd.isna(avail[i]) or avail[i] == float('inf'):
                continue
            annual_consumption = sum(
                F_t[i, h, td] * t_op.get((h, td), 1.0) 
                for h in HOURS for td in TYPICAL_DAYS
            )
            model.add_linear_constraint(annual_consumption <= avail[i])

    # Constraint: Storage level [Eq. 2.14]
    # NOTE: Storage constraints are currently causing infeasibility
    # The model works without storage (objective ~10,748 M€)
    # TODO: Debug storage constraint formulation - see PYOPTINTERFACE_STATUS.md
    print("    - Storage level...")
    if STORAGE_TECH:
        for j in STORAGE_TECH:
            loss_rate = storage_losses.get(j, 0)
            for t in PERIODS:
                h_td_for_t = [(h, td) for (p, h, td) in T_H_TD if p == t]
                if not h_td_for_t: 
                    continue
                h, td = h_td_for_t[0]
                t_op_val = t_op.get((h, td), 1.0)
                
                storage_input = sum(
                    Storage_in[j, l, h, td] * storage_eff_in.get((j, l), 0) 
                    for l in LAYERS if storage_eff_in.get((j, l), 0) > 0
                )
                storage_output = sum(
                    Storage_out[j, l, h, td] / storage_eff_out.get((j, l), 1) 
                    for l in LAYERS if storage_eff_out.get((j, l), 0) > 0
                )

                if t == 1:
                    last_period = PERIODS[-1]
                    model.add_linear_constraint(
                        Storage_level[j, t] == Storage_level[j, last_period] * (1.0 - loss_rate) + 
                        t_op_val * (storage_input - storage_output)
                    )
                else:
                    model.add_linear_constraint(
                        Storage_level[j, t] == Storage_level[j, t-1] * (1.0 - loss_rate) + 
                        t_op_val * (storage_input - storage_output)
                    )
            
            # Constraint: Storage level cannot exceed capacity [Eq. 2.16]
            for t in PERIODS:
                model.add_linear_constraint(Storage_level[j, t] <= F[j])
    
    # Constraint: Operating strategy for passenger mobility [Eq. 2.24]
    print("    - Operating strategy passenger mobility...")
    if 'MOBILITY_PASSENGER' in TECHNOLOGIES_OF_END_USES_CATEGORY and Shares_mobility_passenger:
        for j in TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_PASSENGER']:
            if j in TECH_NOSTORAGE:
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        t_op_val = t_op.get((h, td), 1.0)
                        mob_pass_demand = end_uses_input.get("MOBILITY_PASSENGER", 0) * mob_pass_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                        model.add_linear_constraint(F_t[j, h, td] == Shares_mobility_passenger[j] * mob_pass_demand)
    
    # Constraint: Operating strategy for freight mobility [Eq. 2.25]
    print("    - Operating strategy freight mobility...")
    if 'MOBILITY_FREIGHT' in TECHNOLOGIES_OF_END_USES_CATEGORY and Shares_mobility_freight:
        for j in TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_FREIGHT']:
            if j in TECH_NOSTORAGE:
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        t_op_val = t_op.get((h, td), 1.0)
                        mob_freight_demand = end_uses_input.get("MOBILITY_FREIGHT", 0) * mob_freight_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                        model.add_linear_constraint(F_t[j, h, td] == Shares_mobility_freight[j] * mob_freight_demand)
    
    # Constraint: Extra grid [Eq. 2.21]
    print("    - Extra grid...")
    c_grid_extra = data['parameters'].get('c_grid_extra', 0)
    if 'GRID' in ALL_TECH and c_grid_extra > 0:
        grid_tech = ['WIND_ONSHORE', 'WIND_OFFSHORE', 'PV']
        grid_f = sum(F.get(t, 0) for t in grid_tech if t in F)
        grid_f_min = sum(f_min.get(t, 0) for t in grid_tech if t in f_min)
        model.add_linear_constraint(F['GRID'] == 1 + (c_grid_extra / c_inv.get('GRID', 1)) * (grid_f - grid_f_min))
    
    # Constraint: Extra DHN [Eq. 2.22]
    print("    - Extra DHN...")
    if 'DHN' in ALL_TECH:
        dhn_capacity = sum(
            layers_in_out.get((j, "HEAT_LOW_T_DHN"), 0) * F.get(j, 0)
            for j in TECH_NOSTORAGE
            if layers_in_out.get((j, "HEAT_LOW_T_DHN"), 0) > 0
        )
        model.add_linear_constraint(F['DHN'] == dhn_capacity)
    
    # Constraint: Extra efficiency [Eq. 2.37]
    print("    - Extra efficiency...")
    if 'EFFICIENCY' in ALL_TECH:
        model.add_linear_constraint(F['EFFICIENCY'] == 1 / (1 + i_rate))
    
    # Constraint: Solar area limited [Eq. 2.39]
    print("    - Solar area limited...")
    solar_area = data['parameters'].get('solar_area', float('inf'))
    power_density_pv = data['parameters'].get('power_density_pv', 1)
    power_density_solar_thermal = data['parameters'].get('power_density_solar_thermal', 1)
    if solar_area < float('inf') and power_density_pv > 0:
        pv_area = F.get('PV', 0) / power_density_pv if 'PV' in F else 0
        solar_thermal_area = 0
        if power_density_solar_thermal > 0:
            solar_thermal_area = sum(
                F.get(t, 0) / power_density_solar_thermal
                for t in ['DEC_SOLAR', 'DHN_SOLAR']
                if t in F
            )
        model.add_linear_constraint(pv_area + solar_thermal_area <= solar_area)

    print("  Constraints added.")

    # 5. Define objective function
    print("  Adding cost and GWP constraints and objective...")
    
    investment_total = sum(
        i_rate * (1 + i_rate)**lifetime[j] / ((1 + i_rate)**lifetime[j] - 1) * c_inv[j] * F[j] 
        for j in ALL_TECH if j in c_inv and j in lifetime
    )
    maintenance_total = sum(c_maint.get(j, 0) * F[j] for j in ALL_TECH)
    operating_total = sum(
        c_op.get(i, 0) * sum(F_t[i, h, td] * t_op.get((h,td), 1.0) for h in HOURS for td in TYPICAL_DAYS) 
        for i in RESOURCES if i in c_op
    )
    model.add_linear_constraint(TotalCost == investment_total + maintenance_total + operating_total)

    gwp_constr_total = sum(gwp_constr_param.get(j, 0) * F[j] for j in ALL_TECH)
    gwp_op_total = sum(
        gwp_op_param.get(i, 0) * sum(F_t[i, h, td] * t_op.get((h,td), 1.0) for h in HOURS for td in TYPICAL_DAYS) 
        for i in RESOURCES if i in gwp_op_param
    )
    model.add_linear_constraint(TotalGWP == gwp_constr_total + gwp_op_total)
    if gwp_limit_param < float('inf'):
        model.add_linear_constraint(TotalGWP <= gwp_limit_param)
    
    model.set_objective(TotalCost, poi.ObjectiveSense.Minimize)
    print("  Objective function set.")

    # 6. Solve the model
    print("\nSolving the model...")
    model.optimize()

    # 7. Print results
    term_status = model.get_model_attribute(poi.ModelAttribute.TerminationStatus)
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"  Termination status: {term_status}")

    if term_status == poi.TerminationStatusCode.OPTIMAL:
        obj_val = model.get_model_attribute(poi.ModelAttribute.ObjectiveValue)
        print(f"  Objective value (Total Cost): {obj_val:.4f} M€")
        
        # Print key decision variables
        print(f"\n  Key Decision Variables:")
        print(f"    Share_heat_dhn: {model.get_value(Share_heat_dhn):.4f}")
        print(f"    Share_mobility_public: {model.get_value(Share_mobility_public):.4f}")
        print(f"    Share_freight_train: {model.get_value(Share_freight_train):.4f}")
        print(f"    Share_freight_road: {model.get_value(Share_freight_road):.4f}")
        print(f"    Share_freight_boat: {model.get_value(Share_freight_boat):.4f}")
        
        print("\n✓ PyOptInterface full model ran successfully.")
    else:
        print("\n✗ Could not find the optimal solution.")
        print("\n  Trying to get IIS for debugging...")
        try:
            # Try to compute IIS
            model.set_raw_parameter("IISMethod", 1)
            model.compute_iis()
            print("  IIS computed - infeasible constraints logged to gurobi.ilp")
        except:
            print("  Could not compute IIS due to pyoptinterface limitations.")


if __name__ == "__main__":
    build_and_run_full_model()
