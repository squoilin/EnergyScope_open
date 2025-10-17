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
    ALL_TECH = TECHNOLOGIES + STORAGE_TECH  # All technologies including storage
    TECH_NOSTORAGE = [t for t in ALL_TECH if t not in STORAGE_TECH]
    
    # Parameters
    f_max = data['parameters']['f_max']
    f_min = data['parameters']['f_min']
    layers_in_out = data['parameters']['layers_in_out']
    c_p_t = data['parameters']['c_p_t']  # Capacity factors
    # End_uses can be in time_series with different names
    End_uses = data['time_series'].get('End_uses', data['time_series'].get('end_uses_demand', None))
    
    # ====================================================================
    # DECISION VARIABLES
    # ====================================================================
    
    print("Creating decision variables...")
    
    # F: Installed capacity [GW] or storage level [GWh]
    # Note: Includes both regular technologies and storage
    F = m.add_variables(
        lower=pd.Series([f_min[tech] for tech in ALL_TECH], index=ALL_TECH),
        upper=pd.Series([f_max[tech] for tech in ALL_TECH], index=ALL_TECH),
        coords=[ALL_TECH],
        name="F"
    )
    
    # F_t: Operation of technology/resource at each time step [GW]
    # In AMPL: F_t {RESOURCES union TECHNOLOGIES, HOURS, TYPICAL_DAYS}
    # Indexed by: (RESOURCES + TECHNOLOGIES_NOSTORAGE) x HOURS x TYPICAL_DAYS
    ENTITIES_WITH_F_T = RESOURCES + TECH_NOSTORAGE
    F_t = m.add_variables(
        lower=0,
        coords=[ENTITIES_WITH_F_T, HOURS, TYPICAL_DAYS],
        name="F_t"
    )
    
    # Storage variables (create if there are storage technologies)
    if STORAGE_TECH:
        Storage_in = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, LAYERS, HOURS, TYPICAL_DAYS],
            name="Storage_in"
        )
        
        Storage_out = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, LAYERS, HOURS, TYPICAL_DAYS],
            name="Storage_out"
        )
        
        Storage_level = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, PERIODS],
            name="Storage_level"
        )
    
    # Resource consumption variables
    # In AMPL, resources also use F_t variable
    # For simplicity, we create separate R_t only if needed
    if RESOURCES and 'resources' in constraint_groups:
        # Note: In full AMPL model, resources use the same F_t variable
        # For now, we'll model resources through layers_in_out
        pass
    
    # Cost variables (if cost constraints included)
    if 'costs' in constraint_groups:
        TotalCost = m.add_variables(lower=0, name="TotalCost")
    
    # ====================================================================
    # CONSTRAINT GROUP 1: ENERGY BALANCE
    # ====================================================================
    
    if 'energy_balance' in constraint_groups:
        print("Adding Group 1: Energy Balance constraints...")
        
        # Get additional parameters
        t_op = data['parameters']['t_op']
        total_time = data['parameters']['total_time']
        c_p = data['parameters'].get('c_p', {tech: 1.0 for tech in TECHNOLOGIES})
        
        # ----------------------------------------------------------------
        # Constraint 1.1: capacity_factor_t
        # [Eq. 2.10] F_t[j,h,td] <= F[j] * c_p_t[j,h,td]
        # ----------------------------------------------------------------
        print("  Adding capacity_factor_t constraints...")
        constraint_count = 0
        for j in TECH_NOSTORAGE:
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    # Get capacity factor
                    if (j, h, td) in c_p_t.index:
                        cf = c_p_t.loc[(j, h, td)]
                    else:
                        cf = 1.0
                    
                    m.add_constraints(
                        F_t.loc[j, h, td] <= F.loc[j] * cf,
                        name=f"capacity_factor_t_{j}_{h}_{td}"
                    )
                    constraint_count += 1
        print(f"    Added {constraint_count} capacity_factor_t constraints")
        
        # ----------------------------------------------------------------
        # Constraint 1.2: layer_balance
        # [Eq. 2.13] sum(layers_in_out * F_t) + sum(Storage_out - Storage_in) - End_uses = 0
        # sum over RESOURCES union TECHNOLOGIES (excluding STORAGE_TECH)
        # ----------------------------------------------------------------
        print("  Adding layer_balance constraints...")
        constraint_count = 0
        for l in LAYERS:
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    # Get resources and technologies that interact with this layer
                    entity_layer_pairs = []
                    for entity in ENTITIES_WITH_F_T:
                        try:
                            coef = layers_in_out.loc[entity, l]
                            if abs(coef) > 1e-10:  # Non-zero
                                entity_layer_pairs.append((entity, coef))
                        except (KeyError, IndexError):
                            pass
                    
                    # Sum: layers_in_out[entity,l] * F_t[entity,h,td]
                    balance_expr = sum(
                        F_t.loc[entity, h, td] * coef 
                        for entity, coef in entity_layer_pairs
                    ) if entity_layer_pairs else 0
                    
                    # Add storage flows if storage exists
                    if STORAGE_TECH:
                        for s in STORAGE_TECH:
                            # Storage_out - Storage_in (net contribution to layer)
                            balance_expr = balance_expr + Storage_out.loc[s, l, h, td] - Storage_in.loc[s, l, h, td]
                    
                    # Get demand for this layer
                    if End_uses is not None:
                        try:
                            demand = End_uses.loc[(l, h, td)]
                        except (KeyError, IndexError):
                            demand = 0
                    else:
                        demand = 0
                    
                    # Balance: production - consumption - demand = 0
                    m.add_constraints(
                        balance_expr == demand,
                        name=f"layer_balance_{l}_{h}_{td}"
                    )
                    constraint_count += 1
        print(f"    Added {constraint_count} layer_balance constraints")
        
        # ----------------------------------------------------------------
        # Constraint 1.3: capacity_factor (annual)
        # [Eq. 2.11] sum(F_t * t_op) <= F * c_p * total_time
        # ----------------------------------------------------------------
        print("  Adding capacity_factor (annual) constraints...")
        constraint_count = 0
        for j in TECH_NOSTORAGE:
            # Sum over all periods
            annual_operation = 0
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    try:
                        t_op_val = t_op.loc[(h, td)]
                    except (KeyError, IndexError):
                        t_op_val = 1.0
                    
                    annual_operation += F_t.loc[j, h, td] * t_op_val
            
            # Annual capacity limit
            annual_capacity_factor = c_p.get(j, 1.0)
            m.add_constraints(
                annual_operation <= F.loc[j] * annual_capacity_factor * total_time,
                name=f"capacity_factor_{j}"
            )
            constraint_count += 1
        print(f"    Added {constraint_count} capacity_factor (annual) constraints")
    
    # ====================================================================
    # CONSTRAINT GROUP 2: RESOURCES
    # ====================================================================
    
    if 'resources' in constraint_groups:
        print("Adding Group 2: Resource constraints...")
        
        avail = data['parameters'].get('avail', {})
        RES_IMPORT_CONSTANT = data['sets'].get('RES_IMPORT_CONSTANT', [])
        t_op = data['parameters']['t_op']
        
        # ----------------------------------------------------------------
        # Constraint 2.1: resource_availability
        # [Eq. 2.12] sum(F_t[i,h,td] * t_op[h,td]) <= avail[i]
        # Annual resource consumption cannot exceed availability
        # ----------------------------------------------------------------
        if avail:
            print("  Adding resource_availability constraints...")
            constraint_count = 0
            for i in RESOURCES:
                if i in avail:
                    # Sum annual resource consumption
                    annual_consumption = 0
                    for h in HOURS:
                        for td in TYPICAL_DAYS:
                            try:
                                t_op_val = t_op.loc[(h, td)]
                            except (KeyError, IndexError):
                                t_op_val = 1.0
                            
                            # Resources use F_t variable (same as technologies)
                            annual_consumption += F_t.loc[i, h, td] * t_op_val
                    
                    m.add_constraints(
                        annual_consumption <= avail[i],
                        name=f"resource_availability_{i}"
                    )
                    constraint_count += 1
            print(f"    Added {constraint_count} resource_availability constraints")
        
        # ----------------------------------------------------------------
        # Constraint 2.2: resource_constant_import (skip for now)
        # [Eq. 2.12-bis] For constant imports
        # ----------------------------------------------------------------
        # Not needed for minimal model - will implement when needed
    
    # ====================================================================
    # CONSTRAINT GROUP 3: STORAGE
    # ====================================================================
    
    if 'storage' in constraint_groups and STORAGE_TECH:
        print("Adding Group 3: Storage constraints...")
        
        storage_eff_in = data['parameters']['storage_eff_in']
        storage_eff_out = data['parameters']['storage_eff_out']
        storage_losses = data['parameters'].get('storage_losses', {s: 0 for s in STORAGE_TECH})
        storage_charge_time = data['parameters'].get('storage_charge_time', {s: 1 for s in STORAGE_TECH})
        storage_discharge_time = data['parameters'].get('storage_discharge_time', {s: 1 for s in STORAGE_TECH})
        storage_availability = data['parameters'].get('storage_availability', {s: 1 for s in STORAGE_TECH})
        T_H_TD = data['sets']['T_H_TD']
        
        # ----------------------------------------------------------------
        # Constraint 3.1: storage_layer_in (compatibility)
        # [Eq. 2.17] Storage_in[j,l,h,td] * (ceil(storage_eff_in[j,l]) - 1) = 0
        # This sets Storage_in = 0 for incompatible layer/storage pairs
        # ----------------------------------------------------------------
        print("  Adding storage_layer_in constraints...")
        constraint_count = 0
        for j in STORAGE_TECH:
            for l in LAYERS:
                try:
                    eff = storage_eff_in.loc[j, l]
                    if eff == 0:  # Incompatible
                        for h in HOURS:
                            for td in TYPICAL_DAYS:
                                m.add_constraints(
                                    Storage_in.loc[j, l, h, td] == 0,
                                    name=f"storage_layer_in_{j}_{l}_{h}_{td}"
                                )
                                constraint_count += 1
                except (KeyError, IndexError):
                    # If efficiency not defined, assume incompatible
                    for h in HOURS:
                        for td in TYPICAL_DAYS:
                            m.add_constraints(
                                Storage_in.loc[j, l, h, td] == 0,
                                name=f"storage_layer_in_{j}_{l}_{h}_{td}"
                            )
                            constraint_count += 1
        print(f"    Added {constraint_count} storage_layer_in constraints")
        
        # ----------------------------------------------------------------
        # Constraint 3.2: storage_layer_out (compatibility)
        # [Eq. 2.18] Storage_out[j,l,h,td] * (ceil(storage_eff_out[j,l]) - 1) = 0
        # ----------------------------------------------------------------
        print("  Adding storage_layer_out constraints...")
        constraint_count = 0
        for j in STORAGE_TECH:
            for l in LAYERS:
                try:
                    eff = storage_eff_out.loc[j, l]
                    if eff == 0:  # Incompatible
                        for h in HOURS:
                            for td in TYPICAL_DAYS:
                                m.add_constraints(
                                    Storage_out.loc[j, l, h, td] == 0,
                                    name=f"storage_layer_out_{j}_{l}_{h}_{td}"
                                )
                                constraint_count += 1
                except (KeyError, IndexError):
                    # If efficiency not defined, assume incompatible
                    for h in HOURS:
                        for td in TYPICAL_DAYS:
                            m.add_constraints(
                                Storage_out.loc[j, l, h, td] == 0,
                                name=f"storage_layer_out_{j}_{l}_{h}_{td}"
                            )
                            constraint_count += 1
        print(f"    Added {constraint_count} storage_layer_out constraints")
        
        # ----------------------------------------------------------------
        # Constraint 3.3: storage_level
        # [Eq. 2.14] Storage_level[j,t] = Storage_level[j,t-1] * (1-losses) + inputs - outputs
        # ----------------------------------------------------------------
        print("  Adding storage_level constraints...")
        constraint_count = 0
        for j in STORAGE_TECH:
            loss_rate = storage_losses.get(j, 0)
            
            for t in PERIODS:
                # Find (h, td) for this period
                h_td_for_t = [(h, td) for (period, h, td) in T_H_TD if period == t]
                if not h_td_for_t:
                    continue
                h, td = h_td_for_t[0]
                
                try:
                    t_op_val = t_op.loc[(h, td)]
                except (KeyError, IndexError):
                    t_op_val = 1.0
                
                # Calculate input and output over all layers
                storage_input = 0
                storage_output = 0
                for l in LAYERS:
                    try:
                        eff_in = storage_eff_in.loc[j, l]
                        if eff_in > 0:
                            storage_input += Storage_in.loc[j, l, h, td] * eff_in
                    except (KeyError, IndexError):
                        pass
                    
                    try:
                        eff_out = storage_eff_out.loc[j, l]
                        if eff_out > 0:
                            storage_output += Storage_out.loc[j, l, h, td] / eff_out
                    except (KeyError, IndexError):
                        pass
                
                # Storage balance equation
                if t == 1:
                    # First period: cyclic boundary
                    last_period = PERIODS[-1]
                    m.add_constraints(
                        Storage_level.loc[j, t] == 
                        Storage_level.loc[j, last_period] * (1.0 - loss_rate) +
                        t_op_val * (storage_input - storage_output),
                        name=f"storage_level_{j}_{t}"
                    )
                else:
                    # Regular period
                    m.add_constraints(
                        Storage_level.loc[j, t] == 
                        Storage_level.loc[j, t-1] * (1.0 - loss_rate) +
                        t_op_val * (storage_input - storage_output),
                        name=f"storage_level_{j}_{t}"
                    )
                constraint_count += 1
        print(f"    Added {constraint_count} storage_level constraints")
        
        # ----------------------------------------------------------------
        # Constraint 3.4: limit_energy_stored_to_maximum
        # [Eq. 2.16] Storage_level[j,t] <= F[j]
        # ----------------------------------------------------------------
        print("  Adding limit_energy_stored_to_maximum constraints...")
        STORAGE_DAILY = data['sets'].get('STORAGE_DAILY', [])
        STORAGE_SEASONAL = [s for s in STORAGE_TECH if s not in STORAGE_DAILY]
        
        constraint_count = 0
        for j in STORAGE_SEASONAL:
            for t in PERIODS:
                m.add_constraints(
                    Storage_level.loc[j, t] <= F.loc[j],
                    name=f"limit_energy_stored_to_maximum_{j}_{t}"
                )
                constraint_count += 1
        print(f"    Added {constraint_count} limit_energy_stored_to_maximum constraints")
        
        # ----------------------------------------------------------------
        # Constraint 3.5: limit_energy_to_power_ratio
        # [Eq. 2.19] Storage_in * charge_time + Storage_out * discharge_time <= F * availability
        # ----------------------------------------------------------------
        print("  Adding limit_energy_to_power_ratio constraints...")
        constraint_count = 0
        EV_BATTERIES = {'BEV_BATT', 'PHEV_BATT'}  # Skip these
        for j in [s for s in STORAGE_TECH if s not in EV_BATTERIES]:
            charge_t = storage_charge_time.get(j, 1)
            discharge_t = storage_discharge_time.get(j, 1)
            avail = storage_availability.get(j, 1)
            
            for l in LAYERS:
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        m.add_constraints(
                            Storage_in.loc[j, l, h, td] * charge_t +
                            Storage_out.loc[j, l, h, td] * discharge_t <=
                            F.loc[j] * avail,
                            name=f"limit_energy_to_power_ratio_{j}_{l}_{h}_{td}"
                        )
                        constraint_count += 1
        print(f"    Added {constraint_count} limit_energy_to_power_ratio constraints")
    
    # ====================================================================
    # CONSTRAINT GROUP 4: COSTS
    # ====================================================================
    
    if 'costs' in constraint_groups:
        print("Adding Group 4: Cost constraints...")
        
        c_inv = data['parameters']['c_inv']
        c_maint = data['parameters']['c_maint']
        c_op = data['parameters'].get('c_op', {})
        lifetime = data['parameters']['lifetime']
        i_rate = data['parameters']['i_rate']
        
        # Create cost variables
        C_inv = m.add_variables(lower=0, coords=[ALL_TECH], name="C_inv")
        C_maint = m.add_variables(lower=0, coords=[ALL_TECH], name="C_maint")
        C_op_resources = m.add_variables(lower=0, coords=[RESOURCES], name="C_op")
        
        # ----------------------------------------------------------------
        # Constraint 4.1: investment_cost_calc
        # [Eq. 2.3] C_inv[j] = c_inv[j] * F[j]
        # ----------------------------------------------------------------
        print("  Adding investment_cost_calc constraints...")
        for j in ALL_TECH:
            m.add_constraints(
                C_inv.loc[j] == c_inv[j] * F.loc[j],
                name=f"investment_cost_calc_{j}"
            )
        
        # ----------------------------------------------------------------
        # Constraint 4.2: main_cost_calc (maintenance)
        # [Eq. 2.4] C_maint[j] = c_maint[j] * F[j]
        # ----------------------------------------------------------------
        print("  Adding main_cost_calc constraints...")
        for j in ALL_TECH:
            m.add_constraints(
                C_maint.loc[j] == c_maint[j] * F.loc[j],
                name=f"main_cost_calc_{j}"
            )
        
        # ----------------------------------------------------------------
        # Constraint 4.3: op_cost_calc
        # [Eq. 2.5] C_op[i] = sum(c_op[i] * F_t[i,h,td] * t_op[h,td])
        # ----------------------------------------------------------------
        print("  Adding op_cost_calc constraints...")
        constraint_count = 0
        for i in RESOURCES:
            if i in c_op:
                # Sum over all periods
                annual_cost = 0
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        try:
                            t_op_val = t_op.loc[(h, td)]
                        except (KeyError, IndexError):
                            t_op_val = 1.0
                        
                        # Resources use F_t variable (RESOURCES are in ENTITIES_WITH_F_T)
                        annual_cost += c_op[i] * F_t.loc[i, h, td] * t_op_val
                
                m.add_constraints(
                    C_op_resources.loc[i] == annual_cost,
                    name=f"op_cost_calc_{i}"
                )
                constraint_count += 1
        print(f"    Added {constraint_count} op_cost_calc constraints")
        
        # ----------------------------------------------------------------
        # Constraint 4.4: totalcost_cal
        # [Eq. 2.1] TotalCost = sum(tau * C_inv + C_maint) + sum(C_op)
        # ----------------------------------------------------------------
        print("  Adding totalcost_cal constraint...")
        # Calculate annualization factor (tau) for each technology
        investment_total = 0
        for j in ALL_TECH:
            lt = lifetime[j]
            tau = i_rate * (1 + i_rate)**lt / ((1 + i_rate)**lt - 1)
            investment_total += tau * C_inv.loc[j]
        
        maintenance_total = sum(C_maint.loc[j] for j in ALL_TECH)
        operating_total = sum(C_op_resources.loc[i] for i in RESOURCES)
        
        m.add_constraints(
            TotalCost == investment_total + maintenance_total + operating_total,
            name="totalcost_cal"
        )
        
        print(f"    Added cost constraints: 4 calc + 1 total")
    
    # ====================================================================
    # CONSTRAINT GROUP 5: GWP (Emissions)
    # ====================================================================
    
    if 'gwp' in constraint_groups:
        print("Adding Group 5: GWP (emissions) constraints...")
        
        gwp_constr_param = data['parameters'].get('gwp_constr', {})
        gwp_op_param = data['parameters'].get('gwp_op', {})
        gwp_limit_param = data['parameters'].get('gwp_limit', float('inf'))
        
        # Create GWP variables
        GWP_constr = m.add_variables(lower=0, coords=[ALL_TECH], name="GWP_constr")
        GWP_op = m.add_variables(lower=0, coords=[RESOURCES], name="GWP_op")
        TotalGWP = m.add_variables(lower=0, name="TotalGWP")
        
        # ----------------------------------------------------------------
        # Constraint 5.1: gwp_constr_calc
        # [Eq. 2.7] GWP_constr[j] = gwp_constr[j] * F[j]
        # ----------------------------------------------------------------
        print("  Adding gwp_constr_calc constraints...")
        for j in ALL_TECH:
            gwp_val = gwp_constr_param.get(j, 0)
            m.add_constraints(
                GWP_constr.loc[j] == gwp_val * F.loc[j],
                name=f"gwp_constr_calc_{j}"
            )
        
        # ----------------------------------------------------------------
        # Constraint 5.2: gwp_op_calc
        # [Eq. 2.8] GWP_op[i] = gwp_op[i] * sum(F_t[i,h,td] * t_op[h,td])
        # ----------------------------------------------------------------
        print("  Adding gwp_op_calc constraints...")
        for i in RESOURCES:
            gwp_val = gwp_op_param.get(i, 0)
            if gwp_val > 0:
                # Sum annual resource consumption
                annual_usage = 0
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        try:
                            t_op_val = t_op.loc[(h, td)]
                        except (KeyError, IndexError):
                            t_op_val = 1.0
                        
                        annual_usage += F_t.loc[i, h, td] * t_op_val
                
                m.add_constraints(
                    GWP_op.loc[i] == gwp_val * annual_usage,
                    name=f"gwp_op_calc_{i}"
                )
        
        # ----------------------------------------------------------------
        # Constraint 5.3: totalGWP_calc
        # [Eq. 2.6] TotalGWP = sum(GWP_op[i])
        # ----------------------------------------------------------------
        print("  Adding totalGWP_calc constraint...")
        m.add_constraints(
            TotalGWP == sum(GWP_op.loc[i] for i in RESOURCES),
            name="totalGWP_calc"
        )
        
        # ----------------------------------------------------------------
        # Constraint 5.4: Minimum_GWP_reduction
        # TotalGWP <= gwp_limit
        # ----------------------------------------------------------------
        print("  Adding Minimum_GWP_reduction constraint...")
        if gwp_limit_param < float('inf'):
            m.add_constraints(
                TotalGWP <= gwp_limit_param,
                name="Minimum_GWP_reduction"
            )
        
        print(f"    Added GWP constraints: {len(ALL_TECH)} constr + {len(RESOURCES)} op + 2 total")
    
    # ====================================================================
    # CONSTRAINT GROUP 8: NETWORK
    # ====================================================================
    
    if 'network' in constraint_groups:
        print("Adding Group 8: Network constraints...")
        
        loss_network = data['parameters'].get('loss_network', {})
        c_grid_extra = data['parameters'].get('c_grid_extra', 0)
        c_inv_dict = data['parameters']['c_inv']
        
        # Create Network_losses variable if needed
        if loss_network:
            Network_losses = m.add_variables(
                lower=0,
                coords=[END_USES_TYPES, HOURS, TYPICAL_DAYS],
                name="Network_losses"
            )
            
            # ----------------------------------------------------------------
            # Constraint 8.1: network_losses
            # [Eq. 2.20] Network_losses = sum(F_t * layers_in_out) * loss_network
            # ----------------------------------------------------------------
            print("  Adding network_losses constraints...")
            constraint_count = 0
            for eut in END_USES_TYPES:
                loss_pct = loss_network.get(eut, 0)
                if loss_pct > 0:
                    for h in HOURS:
                        for td in TYPICAL_DAYS:
                            # Sum production to this end-use type
                            production = 0
                            for entity in ENTITIES_WITH_F_T:
                                try:
                                    coef = layers_in_out.loc[entity, eut]
                                    if coef > 0:  # Output to this layer
                                        production += layers_in_out.loc[entity, eut] * F_t.loc[entity, h, td]
                                except (KeyError, IndexError):
                                    pass
                            
                            m.add_constraints(
                                Network_losses.loc[eut, h, td] == production * loss_pct,
                                name=f"network_losses_{eut}_{h}_{td}"
                            )
                            constraint_count += 1
            print(f"    Added {constraint_count} network_losses constraints")
        
        # ----------------------------------------------------------------
        # Constraints 8.2-4: extra_grid, extra_dhn, extra_efficiency
        # These are technology-specific and may not apply to minimal model
        # ----------------------------------------------------------------
        # Skip for now - not relevant to minimal test model
    
    # ====================================================================
    # CONSTRAINT GROUP 9: POLICY
    # ====================================================================
    
    if 'policy' in constraint_groups:
        print("Adding Group 9: Policy constraints...")
        
        fmax_perc = data['parameters'].get('fmax_perc', {})
        fmin_perc = data['parameters'].get('fmin_perc', {})
        TECHNOLOGIES_OF_END_USES_TYPE = data['sets'].get('TECHNOLOGIES_OF_END_USES_TYPE', {})
        
        # ----------------------------------------------------------------
        # Constraint 9.1: f_max_perc
        # [Eq. 2.36] sum(F_t[j]) <= fmax_perc[j] * sum(F_t[all j in category])
        # ----------------------------------------------------------------
        if fmax_perc and TECHNOLOGIES_OF_END_USES_TYPE:
            print("  Adding f_max_perc constraints...")
            constraint_count = 0
            for eut in END_USES_TYPES:
                if eut in TECHNOLOGIES_OF_END_USES_TYPE:
                    techs_in_category = TECHNOLOGIES_OF_END_USES_TYPE[eut]
                    for j in techs_in_category:
                        if j in fmax_perc and j in TECH_NOSTORAGE:
                            # Sum annual output of this tech
                            annual_j = 0
                            for h in HOURS:
                                for td in TYPICAL_DAYS:
                                    try:
                                        t_op_val = t_op.loc[(h, td)]
                                    except:
                                        t_op_val = 1.0
                                    annual_j += F_t.loc[j, h, td] * t_op_val
                            
                            # Sum annual output of all techs in category
                            annual_category = 0
                            for j2 in techs_in_category:
                                if j2 in TECH_NOSTORAGE:
                                    for h in HOURS:
                                        for td in TYPICAL_DAYS:
                                            try:
                                                t_op_val = t_op.loc[(h, td)]
                                            except:
                                                t_op_val = 1.0
                                            annual_category += F_t.loc[j2, h, td] * t_op_val
                            
                            if annual_category != 0:
                                m.add_constraints(
                                    annual_j <= fmax_perc[j] * annual_category,
                                    name=f"f_max_perc_{j}"
                                )
                                constraint_count += 1
            print(f"    Added {constraint_count} f_max_perc constraints")
        
        # ----------------------------------------------------------------
        # Constraint 9.2: f_min_perc (similar to f_max_perc)
        # ----------------------------------------------------------------
        if fmin_perc and TECHNOLOGIES_OF_END_USES_TYPE:
            print("  Adding f_min_perc constraints...")
            # Similar implementation to f_max_perc
            # Skip for minimal model
            pass
    
    # ====================================================================
    # OTHER CONSTRAINT GROUPS (Groups 6-7 TODO)
    # ====================================================================
    
    # Groups 6-7 (Mobility, Heating) to be implemented
    
    # ====================================================================
    # OBJECTIVE FUNCTION
    # ====================================================================
    
    if 'costs' in constraint_groups:
        print("Adding objective function...")
        m.add_objective(TotalCost, sense="min")
    else:
        # Placeholder objective: minimize total installed capacity
        total_capacity = sum(F.loc[j] for j in ALL_TECH)
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


