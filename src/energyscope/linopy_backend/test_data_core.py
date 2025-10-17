"""
Minimal test data for core model development.

This module provides simplified datasets for testing core model constraints
incrementally without needing the full EnergyScope dataset.
"""

import pandas as pd
import numpy as np


def create_minimal_core_data():
    """
    Create minimal core model data for testing Group 1 constraints.
    
    Simplified version:
    - 3 technologies (WIND, GAS_PLANT, GRID)
    - 1 storage (BATTERY)
    - 2 typical days (winter, summer)
    - 24 hours per day
    - 3 main layers (ELECTRICITY, GAS, END_USE)
    
    Returns:
        dict: Model data with sets, parameters, time_series
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
    
    # Layers in/out matrix
    # Positive = output, Negative = input
    layers_in_out_data = {
        'WIND': {'ELECTRICITY': 1.0, 'GAS': 0.0, 'END_USE': 0.0},
        'GAS_PLANT': {'ELECTRICITY': 0.4, 'GAS': -1.0, 'END_USE': 0.0},  # 40% efficient
        'GRID': {'ELECTRICITY': -1.0, 'GAS': 0.0, 'END_USE': 1.0},  # Converts elec to end-use
        'GAS': {'ELECTRICITY': 0.0, 'GAS': 1.0, 'END_USE': 0.0},  # Gas resource
        'ELECTRICITY_IMPORT': {'ELECTRICITY': 1.0, 'GAS': 0.0, 'END_USE': 0.0},
    }
    
    layers_in_out = pd.DataFrame(layers_in_out_data).T
    
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
    
    # Cost parameters (for later)
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
        },
        'time_series': {
            'End_uses': End_uses,  # Pre-computed end-use demand
        }
    }


def print_data_summary(data):
    """Print summary of data for verification."""
    print("=" * 60)
    print("MINIMAL CORE MODEL DATA SUMMARY")
    print("=" * 60)
    
    print("\nSets:")
    for name, value in data['sets'].items():
        if isinstance(value, list):
            print(f"  {name}: {len(value)} elements")
        else:
            print(f"  {name}: {value}")
    
    print("\nKey Parameters:")
    print(f"  total_time: {data['parameters']['total_time']:.0f} hours")
    print(f"  Technologies: {data['sets']['TECHNOLOGIES']}")
    print(f"  Storage: {data['sets']['STORAGE_TECH']}")
    print(f"  Layers: {data['sets']['LAYERS']}")
    
    print("\nCapacity Limits:")
    for tech in data['sets']['TECHNOLOGIES'] + data['sets']['STORAGE_TECH']:
        print(f"  {tech}: {data['parameters']['f_min'][tech]:.1f} - {data['parameters']['f_max'][tech]:.1f} GW")
    
    print("\nDemand Statistics:")
    demand = data['time_series']['End_uses']
    print(f"  Min: {demand.min():.2f} GW")
    print(f"  Max: {demand.max():.2f} GW")
    print(f"  Mean: {demand.mean():.2f} GW")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Test data creation
    data = create_minimal_core_data()
    print_data_summary(data)
    
    print("\n✓ Minimal core data created successfully!")
    print(f"  Ready for Group 1 constraint testing")

