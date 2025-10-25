"""
Data loading utilities for linopy models using xarray.

This module extends the original data_loader.py to support xarray DataArrays,
which enable vectorized constraint formulation in linopy models.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Union
import pandas as pd
import numpy as np
import xarray as xr


def create_toy_data_xarray() -> dict:
    """
    Create toy dataset with xarray DataArrays.
    
    This creates a minimal energy system with:
    - 5 technologies (PV, Wind, Gas, Battery, Grid)
    - 3 layers (Electricity, Gas, End-use)
    - 24 time periods (1 day, hourly)
    
    Returns:
        Dictionary with 'sets' and 'params' containing xarray DataArrays
    """
    # =========================================================================
    # DEFINE COORDINATE SETS
    # =========================================================================
    
    # Use pandas Index objects for proper coordinate handling in linopy
    TECHNOLOGIES = pd.Index(['PV', 'WIND', 'GAS_PLANT', 'BATTERY', 'GRID'], name='tech')
    STORAGE_TECH = pd.Index(['BATTERY'], name='storage')
    LAYERS = pd.Index(['ELECTRICITY', 'GAS', 'END_USE'], name='layer')
    PERIODS = pd.RangeIndex(start=1, stop=25, name='period')  # 1 to 24
    TECH_NOSTORAGE = TECHNOLOGIES.difference(STORAGE_TECH)
    
    # =========================================================================
    # 1D PARAMETERS (indexed by technology)
    # =========================================================================
    
    F_MAX = xr.DataArray(
        [10.0, 5.0, 8.0, 2.0, 3.0],
        coords=[TECHNOLOGIES],
        dims=['tech'],
        name='f_max'
    )
    
    F_MIN = xr.DataArray(
        [0.0, 0.0, 0.0, 0.0, 0.0],
        coords=[TECHNOLOGIES],
        dims=['tech'],
        name='f_min'
    )
    
    # Investment costs (M€/GW or M€/GWh for storage)
    C_INV = xr.DataArray(
        [100.0, 150.0, 80.0, 50.0, 10.0],
        coords=[TECHNOLOGIES],
        dims=['tech'],
        name='c_inv'
    )
    
    # Maintenance costs (M€/GW/year or M€/GWh/year for storage)
    C_MAINT = xr.DataArray(
        [2.0, 3.0, 5.0, 1.0, 0.5],
        coords=[TECHNOLOGIES],
        dims=['tech'],
        name='c_maint'
    )
    
    # Technology lifetime (years)
    LIFETIME = xr.DataArray(
        [25.0, 25.0, 25.0, 15.0, 25.0],
        coords=[TECHNOLOGIES],
        dims=['tech'],
        name='lifetime'
    )
    
    # =========================================================================
    # 2D PARAMETERS (tech x layer)
    # =========================================================================
    
    # Layers in/out matrix
    # Positive = output to layer, Negative = input from layer
    layers_in_out_values = [
        [1.0, 0.0, 0.0],      # PV → ELECTRICITY
        [1.0, 0.0, 0.0],      # WIND → ELECTRICITY
        [0.4, -1.0, 0.0],     # GAS_PLANT: ELEC out (40% eff), GAS in
        [0.0, 0.0, 0.0],      # BATTERY (handled separately by storage vars)
        [-1.0, 0.0, 1.0],     # GRID: ELEC in, END_USE out
    ]
    
    LAYERS_IN_OUT = xr.DataArray(
        layers_in_out_values,
        coords=[TECHNOLOGIES, LAYERS],
        dims=['tech', 'layer'],
        name='layers_in_out'
    )
    
    # =========================================================================
    # TIME-VARYING PARAMETERS (tech x period)
    # =========================================================================
    
    # Capacity factors (time-varying)
    pv_profile = [0.0]*6 + [0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 0.9, 0.8, 0.7, 0.5, 0.3, 0.1] + [0.0]*6
    
    c_p_t_values = [
        pv_profile,          # PV: solar pattern
        [0.6]*24,           # WIND: constant availability
        [1.0]*24,           # GAS_PLANT: fully dispatchable
        [1.0]*24,           # BATTERY: fully dispatchable
        [1.0]*24,           # GRID: always available
    ]
    
    C_P_T = xr.DataArray(
        c_p_t_values,
        coords=[TECHNOLOGIES, PERIODS],
        dims=['tech', 'period'],
        name='c_p_t'
    )
    
    # =========================================================================
    # TIME SERIES (period,)
    # =========================================================================
    
    # Demand time series (GW) - represents END_USE layer demand
    demand_values = [
        0.5, 0.4, 0.4, 0.4, 0.5, 0.6,  # Night/early morning
        0.8, 1.0, 1.2, 1.3, 1.4, 1.5,  # Morning/midday
        1.4, 1.3, 1.2, 1.3, 1.5, 1.8,  # Afternoon/evening peak
        1.6, 1.4, 1.2, 1.0, 0.8, 0.6   # Evening/night
    ]
    
    DEMAND = xr.DataArray(
        demand_values,
        coords=[PERIODS],
        dims=['period'],
        name='demand'
    )
    
    # =========================================================================
    # STORAGE PARAMETERS (indexed by storage tech)
    # =========================================================================
    
    # Charging efficiency (energy stored / energy input)
    STORAGE_EFF_IN = xr.DataArray(
        [0.95],
        coords=[STORAGE_TECH],
        dims=['storage'],
        name='storage_eff_in'
    )
    
    # Discharging efficiency (energy output / energy from storage)
    STORAGE_EFF_OUT = xr.DataArray(
        [0.95],
        coords=[STORAGE_TECH],
        dims=['storage'],
        name='storage_eff_out'
    )
    
    # =========================================================================
    # OPERATING COSTS (resources)
    # =========================================================================
    
    # Operating costs for resources (M€/GWh)
    C_OP_GAS = 50.0    # Cost of gas
    C_OP_GRID = 100.0  # Cost of grid electricity import
    
    # =========================================================================
    # SCALAR PARAMETERS
    # =========================================================================
    
    # Discount rate for investment annualization
    I_RATE = 0.05  # 5%
    
    # =========================================================================
    # RETURN DATA STRUCTURE
    # =========================================================================
    
    return {
        'sets': {
            # Store both pandas Index (for linopy) and lists (for iteration)
            'TECHNOLOGIES': TECHNOLOGIES,
            'STORAGE_TECH': STORAGE_TECH,
            'LAYERS': LAYERS,
            'PERIODS': PERIODS,
            'TECH_NOSTORAGE': TECH_NOSTORAGE,
            # Also provide as lists for convenience
            'TECHNOLOGIES_LIST': TECHNOLOGIES.tolist(),
            'STORAGE_TECH_LIST': STORAGE_TECH.tolist(),
            'LAYERS_LIST': LAYERS.tolist(),
            'PERIODS_LIST': PERIODS.tolist(),
            'TECH_NOSTORAGE_LIST': TECH_NOSTORAGE.tolist(),
        },
        'params': {
            # 1D parameters
            'F_MAX': F_MAX,
            'F_MIN': F_MIN,
            'C_INV': C_INV,
            'C_MAINT': C_MAINT,
            'LIFETIME': LIFETIME,
            
            # 2D parameters
            'LAYERS_IN_OUT': LAYERS_IN_OUT,
            'C_P_T': C_P_T,
            
            # Time series
            'DEMAND': DEMAND,
            
            # Storage parameters
            'STORAGE_EFF_IN': STORAGE_EFF_IN,
            'STORAGE_EFF_OUT': STORAGE_EFF_OUT,
            
            # Operating costs
            'C_OP_GAS': C_OP_GAS,
            'C_OP_GRID': C_OP_GRID,
            
            # Scalars
            'I_RATE': I_RATE,
        }
    }


def verify_xarray_data(data: dict) -> bool:
    """
    Verify that xarray data has correct dimensions and coordinates.
    
    Args:
        data: Dictionary returned by create_toy_data_xarray()
        
    Returns:
        True if data is valid, raises ValueError otherwise
    """
    sets = data['sets']
    params = data['params']
    
    # Check that all expected keys exist
    expected_sets = ['TECHNOLOGIES', 'STORAGE_TECH', 'LAYERS', 'PERIODS', 'TECH_NOSTORAGE']
    for key in expected_sets:
        if key not in sets:
            raise ValueError(f"Missing set: {key}")
    
    expected_params = [
        'F_MAX', 'F_MIN', 'C_INV', 'C_MAINT', 'LIFETIME',
        'LAYERS_IN_OUT', 'C_P_T', 'DEMAND',
        'STORAGE_EFF_IN', 'STORAGE_EFF_OUT',
        'C_OP_GAS', 'C_OP_GRID', 'I_RATE'
    ]
    for key in expected_params:
        if key not in params:
            raise ValueError(f"Missing parameter: {key}")
    
    # Verify dimensions
    TECHNOLOGIES = sets['TECHNOLOGIES']
    LAYERS = sets['LAYERS']
    PERIODS = sets['PERIODS']
    STORAGE_TECH = sets['STORAGE_TECH']
    
    n_tech = len(TECHNOLOGIES)
    n_layers = len(LAYERS)
    n_periods = len(PERIODS)
    n_storage = len(STORAGE_TECH)
    
    # Check 1D tech parameters
    for param_name in ['F_MAX', 'F_MIN', 'C_INV', 'C_MAINT', 'LIFETIME']:
        param = params[param_name]
        if not isinstance(param, xr.DataArray):
            raise ValueError(f"{param_name} is not an xarray DataArray")
        if param.dims != ('tech',):
            raise ValueError(f"{param_name} has wrong dimensions: {param.dims}, expected ('tech',)")
        if len(param) != n_tech:
            raise ValueError(f"{param_name} has wrong size: {len(param)}, expected {n_tech}")
    
    # Check 2D parameters
    layers_in_out = params['LAYERS_IN_OUT']
    if layers_in_out.dims != ('tech', 'layer'):
        raise ValueError(f"LAYERS_IN_OUT has wrong dimensions: {layers_in_out.dims}")
    if layers_in_out.shape != (n_tech, n_layers):
        raise ValueError(f"LAYERS_IN_OUT has wrong shape: {layers_in_out.shape}")
    
    c_p_t = params['C_P_T']
    if c_p_t.dims != ('tech', 'period'):
        raise ValueError(f"C_P_T has wrong dimensions: {c_p_t.dims}")
    if c_p_t.shape != (n_tech, n_periods):
        raise ValueError(f"C_P_T has wrong shape: {c_p_t.shape}")
    
    # Check time series
    demand = params['DEMAND']
    if demand.dims != ('period',):
        raise ValueError(f"DEMAND has wrong dimensions: {demand.dims}")
    if len(demand) != n_periods:
        raise ValueError(f"DEMAND has wrong size: {len(demand)}")
    
    # Check storage parameters
    for param_name in ['STORAGE_EFF_IN', 'STORAGE_EFF_OUT']:
        param = params[param_name]
        if param.dims != ('storage',):
            raise ValueError(f"{param_name} has wrong dimensions: {param.dims}")
        if len(param) != n_storage:
            raise ValueError(f"{param_name} has wrong size: {len(param)}")
    
    print("✓ XArray data verification passed")
    return True


if __name__ == "__main__":
    """Test the xarray data loader."""
    print("Creating xarray toy data...")
    data = create_toy_data_xarray()
    
    print("\nVerifying data structure...")
    verify_xarray_data(data)
    
    print("\nData summary:")
    print(f"  Technologies: {data['sets']['TECHNOLOGIES'].tolist()}")
    print(f"  Layers: {data['sets']['LAYERS'].tolist()}")
    print(f"  Periods: {len(data['sets']['PERIODS'])} hours")
    print(f"  Storage technologies: {data['sets']['STORAGE_TECH'].tolist()}")
    
    print("\nParameter shapes:")
    for name, param in data['params'].items():
        if isinstance(param, xr.DataArray):
            print(f"  {name}: dims={param.dims}, shape={param.shape}")
        else:
            print(f"  {name}: scalar = {param}")
    
    print("\n✓ XArray data loader test passed!")

