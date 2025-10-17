"""
Toy model implementation in linopy.

This is a simplified version of the EnergyScope core model for testing
and development purposes. It includes:
- Basic energy balance
- Capacity constraints
- Simple storage
- Cost minimization
"""

import linopy
import numpy as np
import pandas as pd
from .data_loader import ModelData


def build_toy_model(data: ModelData) -> linopy.Model:
    """
    Build a simplified EnergyScope model using linopy.
    
    This toy model includes:
    1. Decision variables: F (capacity), F_t (operation), Storage_level
    2. Constraints: 
       - Capacity limits
       - Energy balance
       - Storage balance
       - Operation limits (capacity factor)
    3. Objective: Minimize total cost (investment + maintenance + operation)
    
    Args:
        data: ModelData instance with model parameters
        
    Returns:
        linopy.Model instance ready to solve
    """
    m = linopy.Model()
    
    # Extract data
    TECHNOLOGIES = data.sets['TECHNOLOGIES']
    STORAGE_TECH = data.sets['STORAGE_TECH']
    LAYERS = data.sets['LAYERS']
    PERIODS = data.sets['PERIODS']
    
    f_max = data.parameters['f_max']
    f_min = data.parameters['f_min']
    c_inv = data.parameters['c_inv']
    c_maint = data.parameters['c_maint']
    layers_in_out = data.parameters['layers_in_out']
    c_p_t = data.parameters['c_p_t']
    demand = data.time_series['demand']
    
    i_rate = data.parameters['i_rate']
    lifetime = data.parameters['lifetime']
    
    # Non-storage technologies
    TECH_NOSTORAGE = [t for t in TECHNOLOGIES if t not in STORAGE_TECH]
    
    # ==========================
    # DECISION VARIABLES
    # ==========================
    
    # F: Installed capacity [GW] or storage capacity [GWh]
    F = m.add_variables(
        lower={tech: f_min[tech] for tech in TECHNOLOGIES},
        upper={tech: f_max[tech] for tech in TECHNOLOGIES},
        coords=[TECHNOLOGIES],
        name="F"
    )
    
    # F_t: Operation level at each time period [GW]
    F_t = m.add_variables(
        lower=0,
        coords=[TECH_NOSTORAGE, PERIODS],
        name="F_t"
    )
    
    # Storage variables
    if STORAGE_TECH:
        # Storage_in: Energy going into storage [GW]
        Storage_in = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, PERIODS],
            name="Storage_in"
        )
        
        # Storage_out: Energy coming out of storage [GW]
        Storage_out = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, PERIODS],
            name="Storage_out"
        )
        
        # Storage_level: Energy stored [GWh]
        Storage_level = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, PERIODS],
            name="Storage_level"
        )
    
    # ==========================
    # CONSTRAINTS
    # ==========================
    
    # 1. Capacity limits (operation cannot exceed capacity * capacity factor)
    for tech in TECH_NOSTORAGE:
        for t in PERIODS:
            m.add_constraints(
                F_t.loc[tech, t] <= F.loc[tech] * c_p_t.loc[t, tech],
                name=f"capacity_limit_{tech}_{t}"
            )
    
    # 2. Energy balance for each layer and time period
    # sum(F_t * layers_out) >= demand
    for layer in LAYERS:
        for t in PERIODS:
            # Production from technologies
            production_terms = []
            for tech in TECH_NOSTORAGE:
                coef = layers_in_out.loc[tech, layer]
                if coef != 0:
                    production_terms.append(F_t.loc[tech, t] * coef)
            
            # Storage contribution (if applicable)
            if STORAGE_TECH and layer == 'ELECTRICITY':
                for storage in STORAGE_TECH:
                    eff_in = data.parameters['storage_charge_eff'][storage]
                    eff_out = data.parameters['storage_discharge_eff'][storage]
                    # Storage output adds to supply, input subtracts
                    production_terms.append(Storage_out.loc[storage, t] * eff_out)
                    production_terms.append(-Storage_in.loc[storage, t] / eff_in)
            
            # Balance constraint
            if production_terms:
                total_production = sum(production_terms)
                demand_value = demand.loc[t] if layer == 'END_USE' else 0
                
                m.add_constraints(
                    total_production >= demand_value,
                    name=f"energy_balance_{layer}_{t}"
                )
    
    # 3. Storage balance
    if STORAGE_TECH:
        for storage in STORAGE_TECH:
            eff_in = data.parameters['storage_charge_eff'][storage]
            eff_out = data.parameters['storage_discharge_eff'][storage]
            
            for i, t in enumerate(PERIODS):
                if i == 0:
                    # First period: assume storage starts at 50% capacity
                    m.add_constraints(
                        Storage_level.loc[storage, t] == 
                        0.5 * F.loc[storage] + Storage_in.loc[storage, t] * eff_in 
                        - Storage_out.loc[storage, t] / eff_out,
                        name=f"storage_balance_{storage}_{t}_initial"
                    )
                else:
                    prev_t = PERIODS[i-1]
                    m.add_constraints(
                        Storage_level.loc[storage, t] == 
                        Storage_level.loc[storage, prev_t] + Storage_in.loc[storage, t] * eff_in 
                        - Storage_out.loc[storage, t] / eff_out,
                        name=f"storage_balance_{storage}_{t}"
                    )
            
            # Storage level cannot exceed capacity
            for t in PERIODS:
                m.add_constraints(
                    Storage_level.loc[storage, t] <= F.loc[storage],
                    name=f"storage_capacity_{storage}_{t}"
                )
            
            # Cyclic boundary: end level = start level
            first_t = PERIODS[0]
            last_t = PERIODS[-1]
            m.add_constraints(
                Storage_level.loc[storage, last_t] == 0.5 * F.loc[storage],
                name=f"storage_cyclic_{storage}"
            )
    
    # ==========================
    # OBJECTIVE
    # ==========================
    
    # Calculate annualized investment cost
    def annualized_cost(tech):
        lt = lifetime[tech]
        ir = i_rate
        # Capital recovery factor: i(1+i)^n / ((1+i)^n - 1)
        crf = ir * (1 + ir)**lt / ((1 + ir)**lt - 1)
        return c_inv[tech] * crf
    
    # Investment cost
    investment_cost = sum(F.loc[tech] * annualized_cost(tech) for tech in TECHNOLOGIES)
    
    # Maintenance cost (annual)
    maintenance_cost = sum(F.loc[tech] * c_maint[tech] for tech in TECHNOLOGIES)
    
    # Operating cost (resource consumption)
    # For simplicity, charge operating cost to gas consumption
    operating_cost = 0
    if 'GAS_PLANT' in TECH_NOSTORAGE and 'GAS' in data.parameters['c_op']:
        # Gas consumption = gas plant output / efficiency
        # From layers_in_out: GAS_PLANT has GAS input = -1.0
        gas_cost_per_gwh = data.parameters['c_op']['GAS']
        for t in PERIODS:
            # Gas consumption (positive value)
            gas_consumption = -F_t.loc['GAS_PLANT', t] * layers_in_out.loc['GAS_PLANT', 'GAS']
            operating_cost += gas_consumption * gas_cost_per_gwh
    
    # Grid import cost
    if 'GRID' in TECH_NOSTORAGE and 'GRID' in data.parameters['c_op']:
        grid_cost_per_gwh = data.parameters['c_op']['GRID']
        for t in PERIODS:
            # Grid consumption (positive value)
            grid_consumption = F_t.loc['GRID', t]
            operating_cost += grid_consumption * grid_cost_per_gwh
    
    # Total cost
    total_cost = investment_cost + maintenance_cost + operating_cost
    
    m.add_objective(total_cost, sense="min")
    
    return m


def solve_toy_model(data: ModelData, solver='gurobi', solver_options=None):
    """
    Build and solve the toy model.
    
    Args:
        data: ModelData instance
        solver: Solver name (e.g., 'gurobi', 'highs', 'glpk')
        solver_options: Dict of solver-specific options
        
    Returns:
        Tuple of (model, solution_status)
    """
    # Build model
    model = build_toy_model(data)
    
    # Solve
    if solver_options is None:
        solver_options = {}
    
    try:
        result = model.solve(solver_name=solver, **solver_options)
        return model, result
    except Exception as e:
        print(f"Solver error: {e}")
        raise

