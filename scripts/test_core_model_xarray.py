#!/usr/bin/env python
"""
Test script for xarray-based core model.

This script tests the core model constraint groups incrementally,
comparing results with the original loop-based implementation.

Usage:
    python scripts/test_core_model_xarray.py
    
    # Test specific group
    python scripts/test_core_model_xarray.py --group energy_balance
    
    # Compare with original
    python scripts/test_core_model_xarray.py --compare
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from energyscope.linopy_backend.core_model_xarray import (
    build_core_model_xarray, 
    test_constraint_group
)


def create_minimal_test_data():
    """
    Create minimal test data for core model in xarray format.
    
    This is a placeholder - replace with actual data loader when available.
    """
    import pandas as pd
    import xarray as xr
    import numpy as np
    
    print("Creating minimal test data...")
    
    # Minimal sets
    TECHNOLOGIES = pd.Index(['PV', 'CCGT'], name='tech')
    STORAGE_TECH = pd.Index(['BATTERY'], name='storage')
    RESOURCES = pd.Index(['GAS', 'ELECTRICITY'], name='resource')
    LAYERS = pd.Index(['ELECTRICITY', 'HEAT'], name='layer')
    HOURS = pd.RangeIndex(1, 25, name='hour')  # 24 hours
    TYPICAL_DAYS = pd.RangeIndex(1, 2, name='td')  # 1 typical day
    PERIODS = pd.RangeIndex(1, 25, name='period')  # 24 periods
    
    ALL_TECH = TECHNOLOGIES.union(STORAGE_TECH)
    TECH_NOSTORAGE = TECHNOLOGIES.difference(STORAGE_TECH)
    ENTITIES = RESOURCES.union(TECH_NOSTORAGE)
    
    # Minimal parameters
    F_MAX = xr.DataArray(
        [10.0, 8.0, 5.0],  # PV, CCGT, BATTERY
        coords=[ALL_TECH],
        dims=['tech']
    )
    
    F_MIN = xr.DataArray(
        [0.0, 0.0, 0.0],
        coords=[ALL_TECH],
        dims=['tech']
    )
    
    # Layers in/out: (entity, layer)
    # PV → ELEC, CCGT → ELEC (uses GAS), GAS resource, ELEC resource
    LAYERS_IN_OUT = xr.DataArray(
        [[1.0, 0.0],   # PV → ELEC
         [0.4, 0.0],   # CCGT → ELEC (40% efficiency)
         [0.0, -1.0],  # GAS (resource, consumed)
         [1.0, 0.0]],  # ELEC (resource, provided)
        coords=[ENTITIES, LAYERS],
        dims=['entity', 'layer']
    )
    
    # Capacity factors: (tech, hour, td)
    pv_cf = [0.0]*6 + [0.3, 0.5, 0.7, 0.8, 0.9, 0.9, 0.9, 0.8, 0.7, 0.5, 0.3, 0.1] + [0.0]*6
    C_P_T = xr.DataArray(
        np.array([pv_cf, [1.0]*24, [1.0]*24]).reshape(3, 24, 1),  # 3 techs (PV, CCGT, BATTERY), 24 hours, 1 td
        coords=[ALL_TECH, HOURS, TYPICAL_DAYS],
        dims=['tech', 'hour', 'td']
    )
    
    # Operating time: (hour, td)
    T_OP = xr.DataArray(
        np.ones((24, 1)),
        coords=[HOURS, TYPICAL_DAYS],
        dims=['hour', 'td']
    )
    
    # Demand: (layer, hour, td)
    demand_profile = [0.5, 0.4, 0.4, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.3, 1.4, 1.5,
                     1.4, 1.3, 1.2, 1.3, 1.5, 1.8, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6]
    END_USES = xr.DataArray(
        np.array([[d for d in demand_profile], [0.0]*24]).reshape(2, 24, 1),
        coords=[LAYERS, HOURS, TYPICAL_DAYS],
        dims=['layer', 'hour', 'td']
    )
    
    # Costs
    C_INV = xr.DataArray([100.0, 80.0, 50.0], coords=[ALL_TECH], dims=['tech'])
    C_MAINT = xr.DataArray([2.0, 5.0, 1.0], coords=[ALL_TECH], dims=['tech'])
    C_OP = xr.DataArray([50.0, 100.0], coords=[RESOURCES], dims=['resource'])
    LIFETIME = xr.DataArray([25.0, 25.0, 15.0], coords=[ALL_TECH], dims=['tech'])
    C_P = xr.DataArray([1.0, 1.0, 1.0], coords=[ALL_TECH], dims=['tech'])
    
    # Storage parameters
    STORAGE_EFF_IN = xr.DataArray(
        [[0.95, 0.0]],  # BATTERY: ELEC yes, HEAT no
        coords=[STORAGE_TECH, LAYERS],
        dims=['storage', 'layer']
    )
    
    STORAGE_EFF_OUT = xr.DataArray(
        [[0.95, 0.0]],
        coords=[STORAGE_TECH, LAYERS],
        dims=['storage', 'layer']
    )
    
    # Resource availability
    AVAIL = xr.DataArray([1000.0, 500.0], coords=[RESOURCES], dims=['resource'])
    
    # Period mapping
    T_H_TD = [(p, p, 1) for p in PERIODS]  # Simple 1:1 mapping
    
    return {
        'sets': {
            'PERIODS': PERIODS,
            'HOURS': HOURS,
            'TYPICAL_DAYS': TYPICAL_DAYS,
            'TECHNOLOGIES': TECHNOLOGIES,
            'STORAGE_TECH': STORAGE_TECH,
            'RESOURCES': RESOURCES,
            'LAYERS': LAYERS,
            'END_USES_TYPES': pd.Index([]),
            'T_H_TD': T_H_TD,
            'TECH_OF_CATEGORY': {},
            'TECH_OF_TYPE': {},
        },
        'params': {
            'F_MAX': F_MAX,
            'F_MIN': F_MIN,
            'LAYERS_IN_OUT': LAYERS_IN_OUT,
            'C_P_T': C_P_T,
            'T_OP': T_OP,
            'END_USES': END_USES,
            'C_INV': C_INV,
            'C_MAINT': C_MAINT,
            'C_OP': C_OP,
            'C_P': C_P,
            'LIFETIME': LIFETIME,
            'I_RATE': 0.05,
            'TOTAL_TIME': 8760.0,
            'AVAIL': AVAIL,
            'STORAGE_EFF_IN': STORAGE_EFF_IN,
            'STORAGE_EFF_OUT': STORAGE_EFF_OUT,
            'STORAGE_LOSSES': xr.DataArray([0.0], coords=[STORAGE_TECH], dims=['storage']),
        }
    }


def test_all_groups():
    """Test all constraint groups individually."""
    print("=" * 70)
    print("TESTING ALL CONSTRAINT GROUPS")
    print("=" * 70)
    
    data = create_minimal_test_data()
    
    groups = [
        'energy_balance',
        'resources',
        'storage',
        'costs',
        'gwp',
        'mobility',
        'heating',
        'network',
        'policy'
    ]
    
    results = {}
    for group in groups:
        print(f"\n{'='*70}")
        success = test_constraint_group(group, data)
        results[group] = success
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for group, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {group:20s}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n  Total: {passed}/{total} groups passed")
    
    return all(results.values())


def test_full_model():
    """Test full model with all groups."""
    print("=" * 70)
    print("TESTING FULL MODEL (ALL GROUPS)")
    print("=" * 70)
    
    data = create_minimal_test_data()
    
    try:
        model = build_core_model_xarray(data)
        
        print("\n✓ Full model built successfully")
        print(f"  Variables: {len(model.variables)} groups")
        print(f"  Constraints: {len(model.constraints)} groups")
        
        # Try to solve
        print("\nAttempting to solve with HiGHS...")
        result = model.solve(solver_name='highs')
        
        if isinstance(result, tuple):
            status = result[0]
        else:
            status = result
        
        print(f"  Status: {status}")
        
        if hasattr(model, 'objective') and model.objective is not None:
            print(f"  Objective: {model.objective.value}")
        
        return True
    except Exception as e:
        print(f"\n✗ Full model failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    parser = argparse.ArgumentParser(description='Test core model xarray implementation')
    parser.add_argument('--group', type=str, help='Test specific group only')
    parser.add_argument('--full', action='store_true', help='Test full model')
    parser.add_argument('--all', action='store_true', help='Test all groups individually')
    
    args = parser.parse_args()
    
    if args.group:
        # Test specific group
        data = create_minimal_test_data()
        success = test_constraint_group(args.group, data)
        sys.exit(0 if success else 1)
    elif args.full:
        # Test full model
        success = test_full_model()
        sys.exit(0 if success else 1)
    elif args.all:
        # Test all groups
        success = test_all_groups()
        sys.exit(0 if success else 1)
    else:
        # Default: test all groups individually
        print("No arguments specified, testing all groups individually...")
        print("Use --help for options\n")
        success = test_all_groups()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()





