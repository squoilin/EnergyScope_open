"""
EnergyScope Core Model - Linopy Implementation

This module translates the AMPL core model (ESTD_model_core.mod) into linopy.
The translation is done incrementally, constraint group by constraint group.

Original AMPL model: src/energyscope/data/models/core/td/ESTD_model_core.mod
37 constraints, 1 objective function

Translation progress:
- Phase 3.1: Energy balance constraints (4 constraints) - IN PROGRESS
- Phase 3.2: Resources (2 constraints) - TODO
- Phase 3.3: Storage (7 constraints) - TODO
- Phase 3.4: Costs (4 constraints) - TODO
- Phase 3.5: GWP (4 constraints) - TODO
- Phase 3.6: Mobility (5 constraints) - TODO
- Phase 3.7: Heating (3 constraints) - TODO
- Phase 3.8: Network (4 constraints) - TODO
- Phase 3.9: Policy (4 constraints) - TODO
"""

import linopy
import numpy as np
import pandas as pd
import xarray as xr
from typing import Dict, List, Any


def load_core_data_from_ampl(mod_file, dat_files):
    """
    Load core model data from AMPL files.
    
    This is a placeholder - in practice, you would either:
    1. Parse AMPL .dat files
    2. Use amplpy to load and extract data
    3. Convert to native Python format
    
    For now, this returns None to indicate manual data preparation is needed.
    """
    raise NotImplementedError(
        "AMPL .dat file parsing not yet implemented. "
        "Use manual data preparation for now."
    )


def build_core_model_partial(data: Dict[str, Any], constraint_groups: List[str] = None) -> linopy.Model:
    """
    Build the EnergyScope core model in linopy (incremental version).
    
    This function allows building the model incrementally by specifying
    which constraint groups to include. Useful for testing each group
    before adding the next.
    
    Args:
        data: Dictionary containing all model data (sets, parameters, time_series)
        constraint_groups: List of constraint group names to include.
                          If None, includes all implemented groups.
                          Available groups:
                          - 'energy_balance'
                          - 'resources'
                          - 'storage'
                          - 'costs'
                          - 'gwp'
                          - 'mobility'
                          - 'heating'
                          - 'network'
                          - 'policy'
    
    Returns:
        linopy.Model instance ready to solve
    """
    if constraint_groups is None:
        constraint_groups = ['energy_balance']  # Start with just energy balance
    
    m = linopy.Model()
    
    # ====================================================================
    # EXTRACT DATA
    # ====================================================================
    
    # Sets
    PERIODS = data['sets']['PERIODS']
    HOURS = data['sets']['HOURS']
    TYPICAL_DAYS = data['sets']['TYPICAL_DAYS']
    T_H_TD = data['sets']['T_H_TD']  # Linking set
    TECHNOLOGIES = data['sets']['TECHNOLOGIES']
    STORAGE_TECH = data['sets']['STORAGE_TECH']
    RESOURCES = data['sets']['RESOURCES']
    LAYERS = data['sets']['LAYERS']
    END_USES_TYPES = data['sets']['END_USES_TYPES']
    
    # Derived sets
    TECH_NOSTORAGE = [t for t in TECHNOLOGIES if t not in STORAGE_TECH]
    
    # Parameters
    f_max = data['parameters']['f_max']
    f_min = data['parameters']['f_min']
    layers_in_out = data['parameters']['layers_in_out']
    c_p_t = data['parameters']['c_p_t']  # Capacity factors
    end_uses_demand = data['time_series']['end_uses_demand']  # Indexed by end_use, hour, typical_day
    
    # ====================================================================
    # DECISION VARIABLES
    # ====================================================================
    
    print("Creating decision variables...")
    
    # F: Installed capacity [GW] or storage level [GWh]
    F = m.add_variables(
        lower=pd.Series([f_min[tech] for tech in TECHNOLOGIES], index=TECHNOLOGIES),
        upper=pd.Series([f_max[tech] for tech in TECHNOLOGIES], index=TECHNOLOGIES),
        coords=[TECHNOLOGIES],
        name="F"
    )
    
    # F_t: Operation of technology at each time step [GW]
    # Indexed by: TECHNOLOGIES x HOURS x TYPICAL_DAYS
    F_t = m.add_variables(
        lower=0,
        coords=[TECH_NOSTORAGE, HOURS, TYPICAL_DAYS],
        name="F_t"
    )
    
    # Storage variables (if storage constraints are included)
    if 'storage' in constraint_groups:
        Storage_in = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, HOURS, TYPICAL_DAYS],
            name="Storage_in"
        )
        
        Storage_out = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, HOURS, TYPICAL_DAYS],
            name="Storage_out"
        )
        
        Storage_level = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, PERIODS],
            name="Storage_level"
        )
    
    # Resource consumption variables (if resource constraints included)
    if 'resources' in constraint_groups:
        R_t = m.add_variables(
            lower=0,
            coords=[RESOURCES, HOURS, TYPICAL_DAYS],
            name="R_t"
        )
    
    # Cost variables (if cost constraints included)
    if 'costs' in constraint_groups:
        TotalCost = m.add_variables(lower=0, name="TotalCost")
    
    # ====================================================================
    # CONSTRAINT GROUP 1: ENERGY BALANCE
    # ====================================================================
    
    if 'energy_balance' in constraint_groups:
        print("Adding energy balance constraints...")
        
        # end_uses_t: End-use demand must be met at each time step
        # sum over technologies of (F_t * layers_out) >= demand
        for l in LAYERS:
            if l in END_USES_TYPES:  # Only for end-use layers
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        # Get demand
                        if (l, h, td) in end_uses_demand.index:
                            demand_val = end_uses_demand.loc[(l, h, td)]
                        else:
                            demand_val = 0
                        
                        # Sum production from all technologies
                        production_terms = []
                        for j in TECH_NOSTORAGE:
                            if (j, l) in layers_in_out.index:
                                coef = layers_in_out.loc[(j, l)]
                                if coef > 0:  # Output to this layer
                                    production_terms.append(F_t.loc[j, h, td] * coef)
                        
                        if production_terms and demand_val > 0:
                            m.add_constraints(
                                sum(production_terms) >= demand_val,
                                name=f"end_uses_{l}_{h}_{td}"
                            )
        
        # capacity_factor_t: Operation limited by installed capacity and capacity factor
        # F_t[j,h,td] <= F[j] * c_p_t[j,h,td]
        for j in TECH_NOSTORAGE:
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    if (j, h, td) in c_p_t.index:
                        cf = c_p_t.loc[(j, h, td)]
                    else:
                        cf = 1.0
                    
                    m.add_constraints(
                        F_t.loc[j, h, td] <= F.loc[j] * cf,
                        name=f"capacity_factor_t_{j}_{h}_{td}"
                    )
        
        # layer_balance: All layers must be balanced (production >= consumption)
        # This is more general than end_uses_t
        for l in LAYERS:
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    production = []
                    consumption = []
                    
                    for j in TECH_NOSTORAGE:
                        if (j, l) in layers_in_out.index:
                            coef = layers_in_out.loc[(j, l)]
                            if coef > 0:
                                production.append(F_t.loc[j, h, td] * coef)
                            elif coef < 0:
                                consumption.append(F_t.loc[j, h, td] * (-coef))
                    
                    if production or consumption:
                        prod_sum = sum(production) if production else 0
                        cons_sum = sum(consumption) if consumption else 0
                        m.add_constraints(
                            prod_sum >= cons_sum,
                            name=f"layer_balance_{l}_{h}_{td}"
                        )
    
    # ====================================================================
    # CONSTRAINT GROUP 2: RESOURCES (TODO)
    # ====================================================================
    
    if 'resources' in constraint_groups:
        print("Adding resource constraints...")
        # TODO: Implement resource constraints
        # - resource_availability
        # - resource_constant_import
        pass
    
    # ====================================================================
    # CONSTRAINT GROUP 3: STORAGE (TODO)
    # ====================================================================
    
    if 'storage' in constraint_groups:
        print("Adding storage constraints...")
        # TODO: Implement storage constraints
        # - storage_level
        # - storage_layer_in
        # - storage_layer_out
        # - limit_energy_stored_to_maximum
        # - impose_daily_storage
        # - limit_energy_to_power_ratio
        # - limit_energy_to_power_ratio_bis (V2G)
        pass
    
    # ====================================================================
    # OTHER CONSTRAINT GROUPS (TODO)
    # ====================================================================
    
    # Groups 4-9 to be implemented incrementally
    
    # ====================================================================
    # OBJECTIVE FUNCTION
    # ====================================================================
    
    if 'costs' in constraint_groups:
        print("Adding objective function...")
        # TODO: Implement full cost calculation
        # For now, simple objective
        m.add_objective(TotalCost, sense="min")
    else:
        # Placeholder objective: minimize total installed capacity
        total_capacity = sum(F.loc[j] for j in TECHNOLOGIES)
        m.add_objective(total_capacity, sense="min")
    
    return m


def build_core_model(data: Dict[str, Any]) -> linopy.Model:
    """
    Build the complete EnergyScope core model in linopy.
    
    This is the final version that will include all 37 constraints.
    Currently under development - use build_core_model_partial() for
    incremental testing.
    
    Args:
        data: Dictionary containing all model data
    
    Returns:
        linopy.Model instance ready to solve
    """
    # For now, build with all implemented groups
    return build_core_model_partial(
        data, 
        constraint_groups=['energy_balance']  # Add more as implemented
    )


# ========================================================================
# NEXT STEPS
# ========================================================================
#
# 1. Prepare core model data in Python format
#    - Either parse AMPL .dat files
#    - Or create Python data structures manually
#    - Or export from AMPL and convert
#
# 2. Implement constraint Group 1 (energy balance) - CURRENT
#    - Test with partial data
#    - Verify constraints are correct
#    - Compare with AMPL if possible
#
# 3. Add constraint groups 2-9 incrementally
#    - One group at a time
#    - Test each group before adding next
#    - Update this file incrementally
#
# 4. Once all groups implemented, test full model
#    - Solve with real data
#    - Compare with AMPL version
#    - Validate results (< 0.1% difference)
#
# See: docs/linopy_migration_strategy.md for complete plan


