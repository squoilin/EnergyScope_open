"""
Data loading utilities for PyOptInterface models.

This module provides functions to load and preprocess data from various sources
for PyOptInterface model building.
"""

import os
import pandas as pd
import numpy as np
from amplpy import AMPL, add_to_path
from dotenv import load_dotenv


# ============================================================================
# TOY MODEL DATA LOADER
# ============================================================================

def create_toy_data():
    """
    Create a simple toy dataset for testing.
    
    This creates a minimal energy system with:
    - 5 technologies (PV, Wind, Gas, Battery, Grid)
    - 3 layers (Electricity, Gas, End-use)
    - 24 time periods (1 day, hourly)
    
    Returns:
        dict: Model data with keys 'sets', 'parameters', 'time_series'
    """
    # Sets
    technologies = ['PV', 'WIND', 'GAS_PLANT', 'BATTERY', 'GRID']
    storage_tech = ['BATTERY']
    layers = ['ELECTRICITY', 'GAS', 'END_USE']
    periods = list(range(1, 25))  # 24 hours
    
    # Technology parameters
    f_max = {
        'PV': 10.0,
        'WIND': 5.0,
        'GAS_PLANT': 8.0,
        'BATTERY': 2.0,  # GWh storage capacity
        'GRID': 3.0
    }
    
    f_min = {tech: 0.0 for tech in technologies}
    
    # Investment costs (M€/GW)
    c_inv = {
        'PV': 100.0,
        'WIND': 150.0,
        'GAS_PLANT': 80.0,
        'BATTERY': 50.0,  # M€/GWh for storage
        'GRID': 10.0
    }
    
    # Maintenance costs (M€/GW/year)
    c_maint = {
        'PV': 2.0,
        'WIND': 3.0,
        'GAS_PLANT': 5.0,
        'BATTERY': 1.0,
        'GRID': 0.5
    }
    
    # Operating costs for resources (M€/GWh)
    c_op = {
        'GAS': 50.0,
        'GRID': 100.0
    }
    
    # Layers in/out matrix
    # Positive = output, Negative = input
    layers_in_out = pd.DataFrame({
        'PV': {'ELECTRICITY': 1.0, 'GAS': 0.0, 'END_USE': 0.0},
        'WIND': {'ELECTRICITY': 1.0, 'GAS': 0.0, 'END_USE': 0.0},
        'GAS_PLANT': {'ELECTRICITY': 0.4, 'GAS': -1.0, 'END_USE': 0.0},  # 40% efficiency
        'BATTERY': {'ELECTRICITY': 0.0, 'GAS': 0.0, 'END_USE': 0.0},  # Storage handled separately
        'GRID': {'ELECTRICITY': -1.0, 'GAS': 0.0, 'END_USE': 1.0},  # Grid delivers to end-use
    }).T
    
    # Capacity factors (time-varying)
    # Simplified: PV has solar pattern, Wind is constant, rest are dispatchable
    c_p_t = pd.DataFrame({
        'PV': [0.0]*6 + [0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 0.9, 0.8, 0.7, 0.5, 0.3, 0.1] + [0.0]*6,
        'WIND': [0.6]*24,
        'GAS_PLANT': [1.0]*24,
        'BATTERY': [1.0]*24,
        'GRID': [1.0]*24,
    }, index=periods)
    
    # Demand time series (GW)
    demand = pd.Series([
        0.5, 0.4, 0.4, 0.4, 0.5, 0.6,  # Night/early morning
        0.8, 1.0, 1.2, 1.3, 1.4, 1.5,  # Morning/midday
        1.4, 1.3, 1.2, 1.3, 1.5, 1.8,  # Afternoon/evening peak
        1.6, 1.4, 1.2, 1.0, 0.8, 0.6   # Evening/night
    ], index=periods, name='END_USE')
    
    # Storage parameters
    storage_efficiency = {'BATTERY': 0.9}  # Round-trip efficiency
    storage_charge_eff = {'BATTERY': 0.95}
    storage_discharge_eff = {'BATTERY': 0.95}
    
    # Other parameters
    i_rate = 0.05  # 5% discount rate
    lifetime = {tech: 25.0 for tech in technologies}
    lifetime['BATTERY'] = 15.0
    
    # Return as plain dict (compatible with PyOptInterface models)
    return {
        'sets': {
            'TECHNOLOGIES': technologies,
            'STORAGE_TECH': storage_tech,
            'LAYERS': layers,
            'PERIODS': periods,
        },
        'parameters': {
            'f_max': f_max,
            'f_min': f_min,
            'c_inv': c_inv,
            'c_maint': c_maint,
            'c_op': c_op,
            'layers_in_out': layers_in_out,
            'c_p_t': c_p_t,
            'storage_efficiency': storage_efficiency,
            'storage_charge_eff': storage_charge_eff,
            'storage_discharge_eff': storage_discharge_eff,
            'i_rate': i_rate,
            'lifetime': lifetime,
        },
        'time_series': {
            'demand': demand,
        }
    }


# ============================================================================
# MINIMAL CORE MODEL DATA LOADER
# ============================================================================

def create_minimal_core_data():
    """
    Create minimal core model data for testing.
    
    Simplified version:
    - 3 technologies (WIND, GAS_PLANT, GRID)
    - 1 storage (BATTERY)
    - 2 typical days (winter, summer)
    - 24 hours per day
    - 3 main layers (ELECTRICITY, GAS, END_USE)
    
    Returns:
        dict: Model data with keys 'sets', 'parameters', 'time_series'
    """
    
    # ==================================================================
    # SETS
    # ==================================================================
    
    HOURS = list(range(1, 25))  # 1-24
    TYPICAL_DAYS = [1, 2]  # Winter, Summer
    N_TD = len(TYPICAL_DAYS)
    
    # Create periods: each (hour, typical_day) combination
    PERIODS = list(range(1, 24 * N_TD + 1))  # 48 periods total
    
    # T_H_TD: mapping (period, hour, typical_day)
    T_H_TD = []
    for td in TYPICAL_DAYS:
        for h in HOURS:
            period = (td - 1) * 24 + h
            T_H_TD.append((period, h, td))
    
    TECHNOLOGIES = ['WIND', 'GAS_PLANT', 'GRID']
    STORAGE_TECH = ['BATTERY']
    RESOURCES = ['GAS', 'ELECTRICITY_IMPORT']
    
    LAYERS = ['ELECTRICITY', 'GAS', 'END_USE']
    END_USES_TYPES = ['END_USE']  # Simplified
    
    ALL_TECH = TECHNOLOGIES + STORAGE_TECH
    
    # ==================================================================
    # PARAMETERS
    # ==================================================================
    
    # Technology limits
    f_max = {
        'WIND': 5.0,
        'GAS_PLANT': 3.0,
        'GRID': 2.0,
        'BATTERY': 1.0,  # GWh
    }
    
    f_min = {tech: 0.0 for tech in ALL_TECH}
    
    # Capacity factors (time-varying)
    # WIND: higher in winter (TD=1), lower in summer (TD=2)
    c_p_t_data = []
    for td in TYPICAL_DAYS:
        for h in HOURS:
            # Winter: more wind
            if td == 1:
                cf_wind = 0.7 if 0 <= h < 12 else 0.5
            # Summer: less wind
            else:
                cf_wind = 0.4 if 0 <= h < 12 else 0.3
            
            c_p_t_data.append({
                'tech': 'WIND',
                'hour': h,
                'td': td,
                'cf': cf_wind
            })
            
            # Gas plant: always available
            c_p_t_data.append({
                'tech': 'GAS_PLANT',
                'hour': h,
                'td': td,
                'cf': 1.0
            })
            
            # Grid: always available
            c_p_t_data.append({
                'tech': 'GRID',
                'hour': h,
                'td': td,
                'cf': 1.0
            })
            
            # Battery: always available
            c_p_t_data.append({
                'tech': 'BATTERY',
                'hour': h,
                'td': td,
                'cf': 1.0
            })
    
    c_p_t = pd.DataFrame(c_p_t_data).set_index(['tech', 'hour', 'td'])['cf']
    
    # Annual capacity factors
    c_p = {
        'WIND': 0.5,  # 50% annual average
        'GAS_PLANT': 0.8,
        'GRID': 1.0,
        'BATTERY': 1.0,
    }
    
    # Operating time (hours per period)
    t_op_data = []
    for td in TYPICAL_DAYS:
        for h in HOURS:
            # Each typical day represents multiple days
            # TD1 (winter): 180 days, TD2 (summer): 185 days
            days_per_td = 180 if td == 1 else 185
            t_op_data.append({
                'hour': h,
                'td': td,
                't_op': days_per_td  # Each hour in TD represents this many hours/year
            })
    
    t_op = pd.DataFrame(t_op_data).set_index(['hour', 'td'])['t_op']
    total_time = t_op.sum()  # Should be ~8760
    
    # Layers in/out matrix (for resources and technologies)
    # Positive = output, Negative = input
    layers_in_out_data = {
        # Technologies
        'WIND': {'ELECTRICITY': 1.0, 'GAS': 0.0, 'END_USE': 0.0},
        'GAS_PLANT': {'ELECTRICITY': 0.4, 'GAS': -1.0, 'END_USE': 0.0},  # 40% efficient
        'GRID': {'ELECTRICITY': -1.0, 'GAS': 0.0, 'END_USE': 1.0},  # Converts elec to end-use
        # Resources
        'GAS': {'ELECTRICITY': 0.0, 'GAS': 1.0, 'END_USE': 0.0},  # Gas resource supplies GAS layer
        'ELECTRICITY_IMPORT': {'ELECTRICITY': 1.0, 'GAS': 0.0, 'END_USE': 0.0},  # Imports supply electricity
    }
    
    layers_in_out = pd.DataFrame(layers_in_out_data).T
    
    # Resource availability (annual limits)
    avail = {
        'GAS': 10000.0,  # 10,000 GWh/year available
        'ELECTRICITY_IMPORT': 20000.0,  # 20,000 GWh/year import limit
    }
    
    # Demand profile (simplified)
    # End-use demand varies by hour and typical day
    demand_data = []
    for td in TYPICAL_DAYS:
        for h in HOURS:
            # Higher demand in winter, peaks in evening
            if td == 1:  # Winter
                base = 1.0
                if 6 <= h <= 9:  # Morning peak
                    demand = base * 1.3
                elif 17 <= h <= 21:  # Evening peak
                    demand = base * 1.5
                else:
                    demand = base * 0.8
            else:  # Summer
                base = 0.8
                if 11 <= h <= 15:  # Midday peak (cooling)
                    demand = base * 1.2
                else:
                    demand = base * 0.9
            
            demand_data.append({
                'layer': 'END_USE',
                'hour': h,
                'td': td,
                'demand': demand
            })
    
    End_uses = pd.DataFrame(demand_data).set_index(['layer', 'hour', 'td'])['demand']
    
    # Annual demand (for end_uses_t calculation if needed)
    end_uses_input = {
        'END_USE': total_time * 1.0,  # Average 1 GW over year
    }
    
    # Storage parameters
    storage_eff_in = pd.DataFrame({
        'BATTERY': {'ELECTRICITY': 0.95, 'GAS': 0.0, 'END_USE': 0.0}
    }).T
    
    storage_eff_out = pd.DataFrame({
        'BATTERY': {'ELECTRICITY': 0.95, 'GAS': 0.0, 'END_USE': 0.0}
    }).T
    
    storage_losses = {'BATTERY': 0.001}  # 0.1% per hour
    storage_charge_time = {'BATTERY': 4.0}  # 4 hours for full charge
    storage_discharge_time = {'BATTERY': 4.0}
    storage_availability = {'BATTERY': 1.0}
    
    # Cost parameters
    c_inv = {
        'WIND': 150.0,
        'GAS_PLANT': 80.0,
        'GRID': 10.0,
        'BATTERY': 50.0,
    }
    
    c_maint = {
        'WIND': 3.0,
        'GAS_PLANT': 5.0,
        'GRID': 0.5,
        'BATTERY': 1.0,
    }
    
    c_op = {
        'GAS': 50.0,
        'ELECTRICITY_IMPORT': 100.0,
    }
    
    lifetime = {
        'WIND': 25.0,
        'GAS_PLANT': 25.0,
        'GRID': 25.0,
        'BATTERY': 15.0,
    }
    
    i_rate = 0.05
    
    # GWP and network parameters
    gwp_constr = {
        'WIND': 10.0, 'GAS_PLANT': 50.0, 'GRID': 5.0, 'BATTERY': 20.0,
    }
    gwp_op = {
        'GAS': 400.0, 'ELECTRICITY_IMPORT': 300.0,
    }
    gwp_limit = 100000.0
    loss_network = {'END_USE': 0.05}

    # ==================================================================
    # RETURN DATA STRUCTURE
    # ==================================================================
    
    return {
        'sets': {
            'PERIODS': PERIODS,
            'HOURS': HOURS,
            'TYPICAL_DAYS': TYPICAL_DAYS,
            'T_H_TD': T_H_TD,
            'TECHNOLOGIES': TECHNOLOGIES,
            'STORAGE_TECH': STORAGE_TECH,
            'RESOURCES': RESOURCES,
            'LAYERS': LAYERS,
            'END_USES_TYPES': END_USES_TYPES,
        },
        'parameters': {
            'f_max': f_max,
            'f_min': f_min,
            'c_p_t': c_p_t,
            'c_p': c_p,
            't_op': t_op,
            'total_time': total_time,
            'layers_in_out': layers_in_out,
            'avail': avail,  # Resource availability
            'storage_eff_in': storage_eff_in,
            'storage_eff_out': storage_eff_out,
            'storage_losses': storage_losses,
            'storage_charge_time': storage_charge_time,
            'storage_discharge_time': storage_discharge_time,
            'storage_availability': storage_availability,
            'end_uses_input': end_uses_input,
            'c_inv': c_inv,
            'c_maint': c_maint,
            'c_op': c_op,
            'lifetime': lifetime,
            'i_rate': i_rate,
            'gwp_constr': gwp_constr,
            'gwp_op': gwp_op,
            'gwp_limit': gwp_limit,
            'loss_network': loss_network,
        },
        'time_series': {
            'End_uses': End_uses,  # Pre-computed end-use demand
        }
    }


# ============================================================================
# FULL DATASET LOADER (ESTD DATA VIA AMPL)
# ============================================================================

def load_ampl_data():
    """
    Load EnergyScope core data using amplpy.
    
    Returns:
        AMPL instance with loaded data
    """
    load_dotenv()
    ampl_path = os.environ.get("AMPL_PATH")
    if ampl_path:
        add_to_path(ampl_path)
    
    ampl = AMPL()
    
    model_path = "src/energyscope/data/models/core/td/"
    data_path = "src/energyscope/data/datasets/core/td/"
    
    print("Loading AMPL model and data...")
    print(f"  Model: {model_path}ESTD_model_core.mod")
    print(f"  Data:  {data_path}ESTD_12TD.dat")
    print(f"  Data:  {data_path}ESTD_data_core.dat")
    
    ampl.read(model_path + "ESTD_model_core.mod")
    ampl.readData(data_path + "ESTD_12TD.dat")
    ampl.readData(data_path + "ESTD_data_core.dat")
    
    print("✓ AMPL data loaded successfully")
    return ampl


def extract_data_from_ampl(ampl):
    """
    Extracts sets and parameters from an AMPL instance into a Python dictionary.
    """
    print("\nExtracting data into Python format...")
    
    # Extract sets
    sets = {s[0]: list(s[1].members()) for s in ampl.getSets()}
    print(f"  ✓ Extracted {len(sets)} sets")

    # Extract parameters
    parameters = {}
    for param_tuple in ampl.getParameters():
        param_name = param_tuple[0]
        param_obj = param_tuple[1]
        try:
            df = param_obj.getValues().toPandas()
            if not df.empty:
                if df.index.nlevels > 1:
                    parameters[param_name] = df.squeeze()
                else:
                    series_or_scalar = df.squeeze()
                    if isinstance(series_or_scalar, pd.Series):
                        parameters[param_name] = series_or_scalar
                    else:
                        parameters[param_name] = df.iloc[0,0]
            else:
                # If getValues() is empty, it might be a scalar defined with 'default'
                try:
                    val = param_obj.value()
                    if val is not None:
                        parameters[param_name] = val
                    else:
                        print(f"  ⚠ Parameter '{param_name}' is empty and has no scalar value.")
                except Exception as e_val:
                    print(f"  ⚠ Could not retrieve scalar value for '{param_name}': {e_val}")

        except Exception as e:
            print(f"  ⚠ Could not process parameter '{param_name}' as DataFrame: {e}")
            # Fallback for parameters that are not indexed
            try:
                val = param_obj.value()
                if val is not None:
                    parameters[param_name] = val
                    print(f"  ✓ Extracted '{param_name}' as a scalar fallback.")
                else:
                     print(f"  ⚠ Parameter '{param_name}' could not be extracted.")
            except Exception as e_scalar:
                print(f"  ✗ Failed to extract '{param_name}' with any method: {e_scalar}")

    print(f"  ✓ Extracted {len(parameters)} parameters")

    # Assemble the final data dictionary
    data = {
        'sets': sets,
        'parameters': parameters,
        'time_series': {} # This can be populated if needed
    }
    
    # Special handling for T_H_TD which is a set of tuples
    t_h_td_set = ampl.getSet('T_H_TD')
    data['sets']['T_H_TD'] = [tuple(m) for m in t_h_td_set.members()]
    
    # Extract indexed sets (sets that map from one set to another)
    print("  Extracting indexed sets...")
    try:
        # TECHNOLOGIES_OF_END_USES_TYPE: mapping from END_USES_TYPES to technologies
        toet_set = ampl.getSet('TECHNOLOGIES_OF_END_USES_TYPE')
        if toet_set and toet_set.arity() > 0:
            toet_dict = {}
            end_uses_types = data['sets'].get('END_USES_TYPES', [])
            for eut in end_uses_types:
                try:
                    indexed_set = toet_set.get(eut)
                    if indexed_set:
                        toet_dict[eut] = list(indexed_set.members())
                except:
                    pass
            if toet_dict:
                data['sets']['TECHNOLOGIES_OF_END_USES_TYPE'] = toet_dict
                print(f"    ✓ TECHNOLOGIES_OF_END_USES_TYPE: {len(toet_dict)} mappings")
    except Exception as e:
        print(f"    ⚠ Could not extract TECHNOLOGIES_OF_END_USES_TYPE: {e}")
    
    try:
        # TECHNOLOGIES_OF_END_USES_CATEGORY: mapping from END_USES_CATEGORIES to technologies
        toec_set = ampl.getSet('TECHNOLOGIES_OF_END_USES_CATEGORY')
        if toec_set and toec_set.arity() > 0:
            toec_dict = {}
            end_uses_categories = data['sets'].get('END_USES_CATEGORIES', [])
            for euc in end_uses_categories:
                try:
                    indexed_set = toec_set.get(euc)
                    if indexed_set:
                        toec_dict[euc] = list(indexed_set.members())
                except:
                    pass
            if toec_dict:
                data['sets']['TECHNOLOGIES_OF_END_USES_CATEGORY'] = toec_dict
                print(f"    ✓ TECHNOLOGIES_OF_END_USES_CATEGORY: {len(toec_dict)} mappings")
    except Exception as e:
        print(f"    ⚠ Could not extract TECHNOLOGIES_OF_END_USES_CATEGORY: {e}")
    
    # Extract EVs_BATT_OF_V2G indexed set (for V2G/EV storage constraints)
    try:
        evs_batt_v2g_set = ampl.getSet('EVs_BATT_OF_V2G')
        if evs_batt_v2g_set and evs_batt_v2g_set.arity() > 0:
            evs_dict = {}
            v2g_techs = data['sets'].get('V2G', [])
            for v2g in v2g_techs:
                try:
                    indexed_set = evs_batt_v2g_set.get(v2g)
                    if indexed_set:
                        # This set should have exactly one battery per V2G technology
                        evs_dict[v2g] = list(indexed_set.members())
                except:
                    pass
            if evs_dict:
                data['sets']['EVs_BATT_OF_V2G'] = evs_dict
                print(f"    ✓ EVs_BATT_OF_V2G: {len(evs_dict)} mappings")
    except Exception as e:
        print(f"    ⚠ Could not extract EVs_BATT_OF_V2G: {e}")
    
    # Extract TS_OF_DEC_TECH indexed set (for thermal solar constraints)
    try:
        ts_dec_set = ampl.getSet('TS_OF_DEC_TECH')
        if ts_dec_set and ts_dec_set.arity() > 0:
            ts_dict = {}
            # Get decentralized heating technologies (excluding DEC_SOLAR itself)
            dec_techs = data['sets'].get('TECHNOLOGIES_OF_END_USES_TYPE', {}).get('HEAT_LOW_T_DECEN', [])
            dec_techs = [t for t in dec_techs if t != 'DEC_SOLAR']
            for dec_tech in dec_techs:
                try:
                    indexed_set = ts_dec_set.get(dec_tech)
                    if indexed_set:
                        ts_dict[dec_tech] = list(indexed_set.members())
                except:
                    pass
            if ts_dict:
                data['sets']['TS_OF_DEC_TECH'] = ts_dict
                print(f"    ✓ TS_OF_DEC_TECH: {len(ts_dict)} mappings")
    except Exception as e:
        print(f"    ⚠ Could not extract TS_OF_DEC_TECH: {e}")

    # Reconstruct t_op, which is a parameter in AMPL with default value 1
    # In the ESTD model, t_op has "default 1" and is not explicitly set in data files
    # The typical day weighting is handled through the T_H_TD mapping, not through t_op
    print("  Reconstructing 't_op' parameter...")
    try:
        tds = data['sets']['TYPICAL_DAYS']
        hours = data['sets']['HOURS']
        t_op_data = {}

        if 'TYPICAL_DAYS_WEIGHT' in parameters:
            # Use the weight parameter if it was explicitly extracted
            print("  Using 'TYPICAL_DAYS_WEIGHT' to build t_op.")
            td_weight = parameters['TYPICAL_DAYS_WEIGHT'].to_dict()
            for td_name, weight in td_weight.items():
                for h in hours:
                    td_index = tds.index(td_name) + 1 if isinstance(td_name, str) else td_name
                    t_op_data[(h, td_index)] = weight
        else:
            # Default to 1 for each hour as per AMPL model definition
            # The weighting is implicit in the T_H_TD set structure
            print("  't_op' not found in data. Using default value of 1 (as per AMPL model).")
            for td in tds:
                for h in hours:
                    td_index = tds.index(td) + 1 if isinstance(td, str) else td
                    t_op_data[(h, td_index)] = 1.0
        
        if t_op_data:
            t_op_series = pd.Series(t_op_data)
            t_op_series.index.names = ['hour', 'td']
            parameters['t_op'] = t_op_series
            print("  ✓ 't_op' successfully reconstructed with default value 1.")
        else:
            print("  ⚠ 't_op' could not be reconstructed (no typical days?).")

    except Exception as e:
        print(f"  ✗ Failed to reconstruct 't_op': {e}")
        import traceback
        traceback.print_exc()

    return data


def create_full_dataset():
    """
    Loads and converts the full AMPL dataset for the linopy model.
    """
    ampl = load_ampl_data()
    data = extract_data_from_ampl(ampl)
    return data


if __name__ == '__main__':
    # For testing purposes
    print("="*70)
    print("Testing PyOptInterface data loaders")
    print("="*70)
    
    print("\n1. Testing toy data loader...")
    toy_data = create_toy_data()
    print(f"  ✓ Toy data: {len(toy_data['sets'])} sets, {len(toy_data['parameters'])} parameters")
    
    print("\n2. Testing minimal core data loader...")
    core_data = create_minimal_core_data()
    print(f"  ✓ Core data: {len(core_data['sets'])} sets, {len(core_data['parameters'])} parameters")
    
    print("\n3. Testing full dataset loader...")
    full_data = create_full_dataset()
    print(f"  ✓ Full data: {len(full_data['sets'])} sets, {len(full_data['parameters'])} parameters")
    
    print("\n✓ All data loaders tested successfully.")

