"""
Energyscope Full Model implemented in PyOptInterface.
This implementation matches the AMPL model structure.
"""

import time
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
    
    # Start timing
    t_start_total = time.time()

    # 1. Load data
    print("\n[1/3] Loading data...")
    t_data_start = time.time()
    data = create_full_dataset()
    t_data = time.time() - t_data_start
    print(f"  ✓ Data loaded in {t_data:.2f}s")

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
    
    # Optional sets for advanced constraints
    V2G = data['sets'].get('V2G', [])
    EVs_BATT = data['sets'].get('EVs_BATT', [])
    EVs_BATT_OF_V2G = data['sets'].get('EVs_BATT_OF_V2G', {})
    TS_OF_DEC_TECH = data['sets'].get('TS_OF_DEC_TECH', {})
    
    ALL_TECH = TECHNOLOGIES + STORAGE_TECH
    TECH_NOSTORAGE = [t for t in ALL_TECH if t not in STORAGE_TECH]
    # F_t is defined for RESOURCES union TECHNOLOGIES (including storage)
    ENTITIES_WITH_F_T = RESOURCES + ALL_TECH

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
    storage_charge_time = data['parameters'].get('storage_charge_time', pd.Series()).to_dict() if 'storage_charge_time' in data['parameters'] else {}
    storage_discharge_time = data['parameters'].get('storage_discharge_time', pd.Series()).to_dict() if 'storage_discharge_time' in data['parameters'] else {}
    storage_availability = data['parameters'].get('storage_availability', pd.Series()).to_dict() if 'storage_availability' in data['parameters'] else {}
    STORAGE_DAILY = data['sets'].get('STORAGE_DAILY', [])
    
    # Loss network
    loss_network = data['parameters'].get('loss_network', {})
    if isinstance(loss_network, pd.Series):
        loss_network = loss_network.to_dict()
    
    # Optional parameters for V2G/EV storage
    vehicle_capacity = data['parameters'].get('vehicle_capacity', pd.Series()).to_dict() if 'vehicle_capacity' in data['parameters'] else {}
    batt_per_car = data['parameters'].get('batt_per_car', pd.Series()).to_dict() if 'batt_per_car' in data['parameters'] else {}

    # 2. Build model (variables + constraints)
    print("\n[2/3] Building model (variables + constraints)...")
    t_build_start = time.time()
    
    model = gurobi.Model()
    
    # Enable Gurobi output for real-time monitoring
    model.set_model_attribute(poi.ModelAttribute.Silent, False)
    
    # Also set Gurobi-specific OutputFlag to ensure output is shown
    try:
        model.set_raw_parameter("OutputFlag", 1)  # 1 = enable output, 0 = disable
        model.set_raw_parameter("LogToConsole", 1)  # Ensure logs go to console
    except:
        pass  # Older versions may not support this

    # 3. Define variables
    
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
    # OPTIMIZATION: Only create storage variables where efficiency > 0
    # This eliminates ~500K unnecessary constraints and ~300K variables
    Storage_in, Storage_out, Storage_level = {}, {}, {}
    if STORAGE_TECH:
        Storage_in = {
            (s, l, h, td): model.add_variable(lb=0, name=f"Storage_in_{s}_{l}_{h}_{td}")
            for s in STORAGE_TECH 
            for l in LAYERS 
            if storage_eff_in.get((s, l), 0) > 0  # Only create if storage can accept this layer
            for h in HOURS 
            for td in TYPICAL_DAYS
        }
        Storage_out = {
            (s, l, h, td): model.add_variable(lb=0, name=f"Storage_out_{s}_{l}_{h}_{td}")
            for s in STORAGE_TECH 
            for l in LAYERS 
            if storage_eff_out.get((s, l), 0) > 0  # Only create if storage can output this layer
            for h in HOURS 
            for td in TYPICAL_DAYS
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
    
    # Shares for decentralized low-temperature heating technologies (for thermal solar)
    Shares_lowT_dec = {}
    dec_heat_techs = TECHNOLOGIES_OF_END_USES_TYPE.get('HEAT_LOW_T_DECEN', [])
    dec_heat_techs_no_solar = [t for t in dec_heat_techs if t != 'DEC_SOLAR']
    for tech in dec_heat_techs_no_solar:
        Shares_lowT_dec[tech] = model.add_variable(lb=0, name=f"Shares_lowT_dec_{tech}")
    
    # Thermal solar variables (F_solar, F_t_solar)
    F_solar = {}
    F_t_solar = {}
    if dec_heat_techs_no_solar:
        for tech in dec_heat_techs_no_solar:
            F_solar[tech] = model.add_variable(lb=0, name=f"F_solar_{tech}")
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    F_t_solar[tech, h, td] = model.add_variable(lb=0, name=f"F_t_solar_{tech}_{h}_{td}")
    
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

    # 4. Add constraints
    
    # Constraint: Freight shares must sum to 1 [Eq. 2.26]
    model.add_linear_constraint(Share_freight_train + Share_freight_road + Share_freight_boat == 1)
    
    # Constraint: End-uses demand calculation [Eq. 2.8 / Figure 2.8]
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
    for j in ALL_TECH:  # Applies to all technologies including storage
        for h in HOURS:
            for td in TYPICAL_DAYS:
                cf = c_p_t.get((j, h, td), 1.0)
                model.add_linear_constraint(F_t[j, h, td] <= F[j] * cf)
    
    # Constraint: Yearly capacity factor [Eq. 2.11]
    # This limits total annual output to account for downtime and maintenance
    c_p = data['parameters'].get('c_p', pd.Series()).to_dict() if 'c_p' in data['parameters'] else {}
    for j in ALL_TECH:
        if j in c_p:
            annual_output = sum(
                F_t[j, h, td] * t_op.get((h, td), 1.0)
                for h in HOURS for td in TYPICAL_DAYS
            )
            model.add_linear_constraint(annual_output <= F[j] * c_p[j] * total_time)

    # Constraint: Layer balance [Eq. 2.13]
    for l in LAYERS:
        for h in HOURS:
            for td in TYPICAL_DAYS:
                # Sum over RESOURCES and non-storage TECHNOLOGIES only
                balance_expr = sum(
                    layers_in_out.get((entity, l), 0) * F_t[entity, h, td]
                    for entity in (RESOURCES + TECH_NOSTORAGE)
                )
                
                # Add storage contribution (only for layers where storage is compatible)
                if STORAGE_TECH:
                    for s in STORAGE_TECH:
                        # Only add if variables exist (efficiency > 0)
                        if (s, l, h, td) in Storage_out:
                            balance_expr += Storage_out[s, l, h, td]
                        if (s, l, h, td) in Storage_in:
                            balance_expr -= Storage_in[s, l, h, td]
                
                model.add_linear_constraint(balance_expr == End_uses[l, h, td])

    # Constraint: Resources availability [Eq. 2.12]
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
    if STORAGE_TECH:
        for j in STORAGE_TECH:
            loss_rate = storage_losses.get(j, 0)
            for t in PERIODS:
                h_td_for_t = [(h, td) for (p, h, td) in T_H_TD if p == t]
                if not h_td_for_t: 
                    continue
                h, td = h_td_for_t[0]
                t_op_val = t_op.get((h, td), 1.0)
                
                # Storage input: sum over layers with eff_in > 0
                storage_input = sum(
                    Storage_in[j, l, h, td] * storage_eff_in[(j, l)]
                    for l in LAYERS 
                    if (j, l, h, td) in Storage_in  # Variable exists
                )
                # Storage output: sum over layers with eff_out > 0
                storage_output = sum(
                    Storage_out[j, l, h, td] / storage_eff_out[(j, l)]
                    for l in LAYERS 
                    if (j, l, h, td) in Storage_out  # Variable exists
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
        
        # Constraint: Daily storage [Eq. 2.15]
        # For daily storage, level must equal F_t at each period
        for j in STORAGE_DAILY:
            for t in PERIODS:
                h_td_for_t = [(h, td) for (p, h, td) in T_H_TD if p == t]
                if not h_td_for_t: 
                    continue
                h, td = h_td_for_t[0]
                # In AMPL: Storage_level [j, t] = F_t [j, h, td]
                # F_t for storage represents the storage level at that time
                model.add_linear_constraint(Storage_level[j, t] == F_t[j, h, td])
        
        # Constraint: Seasonal storage level cannot exceed capacity [Eq. 2.16]
        for j in STORAGE_TECH:
            if j not in STORAGE_DAILY:  # Only for seasonal storage
                for t in PERIODS:
                    model.add_linear_constraint(Storage_level[j, t] <= F[j])
        
        # Constraint: Storage layer compatibility [Eqs. 2.17-2.18]
        # OPTIMIZATION: No longer needed! We only created variables where eff > 0
        # The constraint is implicitly satisfied by not creating incompatible variables
        
        # Constraint: Energy-to-power ratio [Eq. 2.19]
        for j in STORAGE_TECH:
            # Skip EV batteries (they have special constraints in Eq. 2.19-bis)
            if j in EVs_BATT:
                continue
            
            charge_time = storage_charge_time.get(j, 0)
            discharge_time = storage_discharge_time.get(j, 0)
            availability = storage_availability.get(j, 1.0)
            
            # Apply constraint per layer (only where variables exist)
            for l in LAYERS:
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        # Only add constraint if both variables exist
                        if (j, l, h, td) in Storage_in and (j, l, h, td) in Storage_out:
                            model.add_linear_constraint(
                                Storage_in[j, l, h, td] * charge_time + 
                                Storage_out[j, l, h, td] * discharge_time <= 
                                F[j] * availability
                            )
        
        # Constraint: Energy-to-power ratio for EV batteries [Eq. 2.19-bis]
        # This accounts for battery discharge to power the vehicle (F_t) in addition to V2G discharge
        if V2G and EVs_BATT_OF_V2G:
            for i in V2G:
                if i not in EVs_BATT_OF_V2G:
                    continue
                # Get the battery associated with this V2G vehicle
                batt_list = EVs_BATT_OF_V2G[i]
                if not batt_list:
                    continue
                j = batt_list[0]  # Should be exactly one battery per V2G technology
                
                charge_time = storage_charge_time.get(j, 0)
                discharge_time = storage_discharge_time.get(j, 0)
                availability = storage_availability.get(j, 1.0)
                veh_cap = vehicle_capacity.get(i, 1.0)
                batt_size = batt_per_car.get(i, 0)
                
                # AMPL: Storage_in * charge_time + (Storage_out + layers_in_out[i,"ELECTRICITY"]* F_t) * discharge_time 
                #       <= (F[j] - F_t[i] / vehicle_capacity * batt_per_car) * availability
                # layers_in_out[i,"ELECTRICITY"] is negative (consumption), so we take absolute value
                layers_elec_consumption = abs(layers_in_out.get((i, "ELECTRICITY"), 0))
                
                for l in LAYERS:
                    for h in HOURS:
                        for td in TYPICAL_DAYS:
                            # Only add constraint if both variables exist
                            if (j, l, h, td) in Storage_in and (j, l, h, td) in Storage_out:
                                # Available battery capacity = Total battery - battery in use by driving vehicles
                                available_batt = F[j] - (F_t[i, h, td] / veh_cap * batt_size if veh_cap > 0 else 0)
                                
                                model.add_linear_constraint(
                                    Storage_in[j, l, h, td] * charge_time + 
                                    (Storage_out[j, l, h, td] + layers_elec_consumption * F_t[i, h, td]) * discharge_time <= 
                                    available_batt * availability
                                )
    
    # Constraint: Operating strategy for passenger mobility [Eq. 2.24]
    if 'MOBILITY_PASSENGER' in TECHNOLOGIES_OF_END_USES_CATEGORY and Shares_mobility_passenger:
        for j in TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_PASSENGER']:
            if j in TECH_NOSTORAGE:
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        t_op_val = t_op.get((h, td), 1.0)
                        mob_pass_demand = end_uses_input.get("MOBILITY_PASSENGER", 0) * mob_pass_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                        model.add_linear_constraint(F_t[j, h, td] == Shares_mobility_passenger[j] * mob_pass_demand)
    
    # Constraint: Operating strategy for freight mobility [Eq. 2.25]
    if 'MOBILITY_FREIGHT' in TECHNOLOGIES_OF_END_USES_CATEGORY and Shares_mobility_freight:
        for j in TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_FREIGHT']:
            if j in TECH_NOSTORAGE:
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        t_op_val = t_op.get((h, td), 1.0)
                        mob_freight_demand = end_uses_input.get("MOBILITY_FREIGHT", 0) * mob_freight_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                        model.add_linear_constraint(F_t[j, h, td] == Shares_mobility_freight[j] * mob_freight_demand)
    
    # Constraint: Extra grid [Eq. 2.21]
    c_grid_extra = data['parameters'].get('c_grid_extra', 0)
    if 'GRID' in ALL_TECH and c_grid_extra > 0:
        grid_tech = ['WIND_ONSHORE', 'WIND_OFFSHORE', 'PV']
        grid_f = sum(F.get(t, 0) for t in grid_tech if t in F)
        grid_f_min = sum(f_min.get(t, 0) for t in grid_tech if t in f_min)
        model.add_linear_constraint(F['GRID'] == 1 + (c_grid_extra / c_inv.get('GRID', 1)) * (grid_f - grid_f_min))
    
    # Constraint: Extra DHN [Eq. 2.22]
    if 'DHN' in ALL_TECH:
        dhn_capacity = sum(
            layers_in_out.get((j, "HEAT_LOW_T_DHN"), 0) * F.get(j, 0)
            for j in TECH_NOSTORAGE
            if layers_in_out.get((j, "HEAT_LOW_T_DHN"), 0) > 0
        )
        model.add_linear_constraint(F['DHN'] == dhn_capacity)
    
    # Constraint: Extra efficiency [Eq. 2.37]
    if 'EFFICIENCY' in ALL_TECH:
        model.add_linear_constraint(F['EFFICIENCY'] == 1 / (1 + i_rate))
    
    # Constraint: Solar area limited [Eq. 2.39]
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
    
    # Constraint: Thermal solar capacity factor [Eq. 2.27]
    if F_solar and 'DEC_SOLAR' in ALL_TECH:
        for j in dec_heat_techs_no_solar:
            if j in F_solar:
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        cf_solar = c_p_t.get(('DEC_SOLAR', h, td), 1.0)
                        model.add_linear_constraint(F_t_solar[j, h, td] <= F_solar[j] * cf_solar)
    
    # Constraint: Total thermal solar capacity [Eq. 2.28]
    if F_solar and 'DEC_SOLAR' in ALL_TECH:
        total_solar = sum(F_solar.get(j, 0) for j in dec_heat_techs_no_solar if j in F_solar)
        model.add_linear_constraint(F['DEC_SOLAR'] == total_solar)
    
    # Constraint: Decentralized heating balance with thermal solar [Eq. 2.29]
    if TS_OF_DEC_TECH and Shares_lowT_dec:
        for j in dec_heat_techs_no_solar:
            if j not in TS_OF_DEC_TECH or j not in Shares_lowT_dec:
                continue
            # Get the thermal storage associated with this technology
            ts_list = TS_OF_DEC_TECH[j]
            if not ts_list:
                continue
            i = ts_list[0]  # Should be exactly one thermal storage per technology
            
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    t_op_val = t_op.get((h, td), 1.0)
                    
                    # Heat demand for decentralized heating
                    hw = end_uses_input.get("HEAT_LOW_T_HW", 0) / total_time if total_time > 0 else 0
                    sh = end_uses_input.get("HEAT_LOW_T_SH", 0) * heating_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    heat_demand = hw + sh
                    
                    # Heat balance: tech output + solar output + storage net output = share * demand
                    # F_t[j] + F_t_solar[j] + sum_over_layers(Storage_out - Storage_in) = Shares_lowT_dec[j] * demand
                    storage_contribution = 0
                    for l in LAYERS:
                        if (i, l, h, td) in Storage_out:
                            storage_contribution += Storage_out[i, l, h, td]
                        if (i, l, h, td) in Storage_in:
                            storage_contribution -= Storage_in[i, l, h, td]
                    
                    model.add_linear_constraint(
                        F_t[j, h, td] + F_t_solar[j, h, td] + storage_contribution == 
                        Shares_lowT_dec[j] * heat_demand
                    )
    
    # Constraint: EV storage sizing [Eq. 2.30]
    if V2G and EVs_BATT_OF_V2G and vehicle_capacity and batt_per_car:
        for j in V2G:
            if j not in EVs_BATT_OF_V2G:
                continue
            batt_list = EVs_BATT_OF_V2G[j]
            if not batt_list:
                continue
            i = batt_list[0]  # Battery for this V2G vehicle
            
            veh_cap = vehicle_capacity.get(j, 1.0)
            batt_size = batt_per_car.get(j, 0)
            
            # F[battery] = F[vehicle] / vehicle_capacity * batt_per_car
            if veh_cap > 0 and j in F and i in F:
                model.add_linear_constraint(F[i] == F[j] / veh_cap * batt_size)
    
    # Constraint: EV battery supplies vehicle demand (V2G) [Eq. 2.31]
    if V2G and EVs_BATT_OF_V2G:
        for j in V2G:
            if j not in EVs_BATT_OF_V2G:
                continue
            batt_list = EVs_BATT_OF_V2G[j]
            if not batt_list:
                continue
            i = batt_list[0]  # Battery for this V2G vehicle
            
            # layers_in_out[j, "ELECTRICITY"] is negative (consumption)
            elec_consumption = abs(layers_in_out.get((j, "ELECTRICITY"), 0))
            
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    # Storage_out must be at least enough to power the vehicle
                    # Only add if variable exists
                    if (i, "ELECTRICITY", h, td) in Storage_out:
                        model.add_linear_constraint(
                            Storage_out[i, "ELECTRICITY", h, td] >= elec_consumption * F_t[j, h, td]
                        )
    
    # Constraint: fmax_perc and fmin_perc [Eq. 2.36]
    # These limit technology output as a percentage of total sector output
    fmax_perc = data['parameters'].get('fmax_perc', pd.Series()).to_dict() if 'fmax_perc' in data['parameters'] else {}
    fmin_perc = data['parameters'].get('fmin_perc', pd.Series()).to_dict() if 'fmin_perc' in data['parameters'] else {}
    
    for eut in END_USES_TYPES:
        if eut in TECHNOLOGIES_OF_END_USES_TYPE:
            techs_in_type = [t for t in TECHNOLOGIES_OF_END_USES_TYPE[eut] if t in TECH_NOSTORAGE]
            if not techs_in_type:
                continue
            
            # Total output for this end-use type across all technologies
            total_output = sum(
                F_t[j2, h, td] * t_op.get((h, td), 1.0)
                for j2 in techs_in_type
                for h in HOURS for td in TYPICAL_DAYS
            )
            
            # Apply constraints for each technology
            for j in techs_in_type:
                tech_output = sum(
                    F_t[j, h, td] * t_op.get((h, td), 1.0)
                    for h in HOURS for td in TYPICAL_DAYS
                )
                
                # fmax_perc constraint
                if j in fmax_perc and fmax_perc[j] < 1.0:
                    model.add_linear_constraint(tech_output <= fmax_perc[j] * total_output)
                
                # fmin_perc constraint
                if j in fmin_perc and fmin_perc[j] > 0.0:
                    model.add_linear_constraint(tech_output >= fmin_perc[j] * total_output)

    # 5. Define objective function
    
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

    # GWP calculation - ONLY operational emissions from resources (construction emissions commented out in AMPL)
    # gwp_constr_total = sum(gwp_constr_param.get(j, 0) * F[j] for j in ALL_TECH)  # NOT USED
    gwp_op_total = sum(
        gwp_op_param.get(i, 0) * sum(F_t[i, h, td] * t_op.get((h,td), 1.0) for h in HOURS for td in TYPICAL_DAYS) 
        for i in RESOURCES if i in gwp_op_param
    )
    # TotalGWP = operational emissions only (as per AMPL line 214)
    model.add_linear_constraint(TotalGWP == gwp_op_total)
    if gwp_limit_param < float('inf'):
        model.add_linear_constraint(TotalGWP <= gwp_limit_param)
    
    model.set_objective(TotalCost, poi.ObjectiveSense.Minimize)
    
    t_build = time.time() - t_build_start
    print(f"  ✓ Model built in {t_build:.2f}s")
    
    # Get model statistics
    n_vars = len(F) + len(F_t) + len(Storage_in) + len(Storage_out) + len(Storage_level) + len(End_uses) + len(Network_losses) + len(Shares_mobility_passenger) + len(Shares_mobility_freight) + len(Shares_lowT_dec) + len(F_solar) + len(F_t_solar) + 7
    print(f"    Variables: ~{n_vars:,}")
    print(f"    F: {len(F):,}, F_t: {len(F_t):,}, Storage vars: {len(Storage_in) + len(Storage_out) + len(Storage_level):,}")

    # 6. Solve the model
    print("\n[3/3] Solving with Gurobi...")
    t_solve_start = time.time()
    
    # Set Gurobi parameters right before optimization
    model.set_raw_parameter("OutputFlag", 1)
    model.set_raw_parameter("DisplayInterval", 5)  # Show output every 5 seconds
    
    model.optimize()
    t_solve = time.time() - t_solve_start

    # 7. Print results
    t_total = time.time() - t_start_total
    
    term_status = model.get_model_attribute(poi.ModelAttribute.TerminationStatus)
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"  Termination status: {term_status}")
    print(f"\n  TIMING SUMMARY:")
    print(f"    Data loading:   {t_data:>8.2f}s ({100*t_data/t_total:>5.1f}%)")
    print(f"    Model building: {t_build:>8.2f}s ({100*t_build/t_total:>5.1f}%)")
    print(f"    Solving:        {t_solve:>8.2f}s ({100*t_solve/t_total:>5.1f}%)")
    print(f"    TOTAL:          {t_total:>8.2f}s")

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
        print("\n  Trying to compute IIS for debugging...")
        try:
            # Try to compute IIS and write to file
            model.compute_iis()
            model.write("pyopt_full_model.ilp")
            print("  IIS computed and written to pyopt_full_model.ilp")
        except Exception as e:
            print(f"  Could not compute IIS: {e}")


if __name__ == "__main__":
    build_and_run_full_model()
