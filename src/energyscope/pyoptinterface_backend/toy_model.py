"""
Energyscope Toy Model implementation using PyOptInterface.

This module provides a simplified toy model for testing and demonstration.
"""

import pyoptinterface as poi
from pyoptinterface import highs


def build_toy_model(data, solver='highs', verbose=True):
    """
    Builds and solves the Energyscope toy model using pyoptinterface.
    
    Parameters
    ----------
    data : dict
        Dictionary containing sets, parameters, and time series data.
        Should have keys: 'sets', 'parameters', 'time_series'
    solver : str, optional
        Solver to use ('highs' or 'gurobi'). Default is 'highs'.
    verbose : bool, optional
        Whether to print progress messages. Default is True.
        
    Returns
    -------
    dict
        Dictionary with keys:
        - 'model': The optimization model object
        - 'variables': Dict of variable dictionaries (F, F_t, Storage_*)
        - 'status': Termination status
        - 'objective': Objective value (if optimal)
        - 'solution': Solution values for key variables (if optimal)
    """
    if verbose:
        print("="*70)
        print("Building PyOptInterface toy model")
        print("="*70)

    # Extract sets and parameters
    TECHNOLOGIES = data['sets']['TECHNOLOGIES']
    STORAGE_TECH = data['sets']['STORAGE_TECH']
    LAYERS = data['sets']['LAYERS']
    PERIODS = data['sets']['PERIODS']
    TECH_NOSTORAGE = [t for t in TECHNOLOGIES if t not in STORAGE_TECH]

    f_max = data['parameters']['f_max']
    f_min = data['parameters']['f_min']
    c_inv = data['parameters']['c_inv']
    c_maint = data['parameters']['c_maint']
    layers_in_out = data['parameters']['layers_in_out']
    c_p_t = data['parameters']['c_p_t']
    demand = data['time_series']['demand']
    i_rate = data['parameters']['i_rate']
    lifetime = data['parameters']['lifetime']
    c_op = data['parameters']['c_op']

    # Create model with appropriate solver
    if solver.lower() == 'gurobi':
        from pyoptinterface import gurobi
        model = gurobi.Model()
    elif solver.lower() == 'highs':
        model = highs.Model()
    else:
        # Default to Gurobi
        from pyoptinterface import gurobi
        model = gurobi.Model()
    
    if verbose:
        print(f"  Model created with {solver.upper()} backend.")

    # Define variables
    F = {
        tech: model.add_variable(lb=f_min[tech], ub=f_max[tech], name=f"F_{tech}")
        for tech in TECHNOLOGIES
    }

    F_t = {
        (tech, t): model.add_variable(lb=0, name=f"F_t_{tech}_{t}")
        for tech in TECH_NOSTORAGE for t in PERIODS
    }

    # Storage variables
    Storage_in, Storage_out, Storage_level = {}, {}, {}
    if STORAGE_TECH:
        for storage in STORAGE_TECH:
            for t in PERIODS:
                Storage_in[storage, t] = model.add_variable(lb=0, name=f"Storage_in_{storage}_{t}")
                Storage_out[storage, t] = model.add_variable(lb=0, name=f"Storage_out_{storage}_{t}")
                Storage_level[storage, t] = model.add_variable(lb=0, name=f"Storage_level_{storage}_{t}")
    
    if verbose:
        print("  Variables created.")

    # Add constraints
    # Capacity limits
    for tech in TECH_NOSTORAGE:
        for t in PERIODS:
            model.add_linear_constraint(
                F_t[tech, t] <= F[tech] * c_p_t.loc[t, tech]
            )

    # Energy balance
    for layer in LAYERS:
        for t in PERIODS:
            production = 0
            for tech in TECH_NOSTORAGE:
                coef = layers_in_out.loc[tech, layer]
                if coef != 0:
                    production += F_t[tech, t] * coef
            
            if STORAGE_TECH and layer == 'ELECTRICITY':
                for storage in STORAGE_TECH:
                    eff_in = data['parameters']['storage_charge_eff'][storage]
                    eff_out = data['parameters']['storage_discharge_eff'][storage]
                    production += Storage_out[storage, t] * eff_out - Storage_in[storage, t] / eff_in

            demand_value = demand.loc[t] if layer == 'END_USE' else 0
            if production != 0:
                model.add_linear_constraint(production >= demand_value)

    # Storage balance
    if STORAGE_TECH:
        for storage in STORAGE_TECH:
            eff_in = data['parameters']['storage_charge_eff'][storage]
            eff_out = data['parameters']['storage_discharge_eff'][storage]
            for i, t in enumerate(PERIODS):
                if i == 0:
                    model.add_linear_constraint(
                        Storage_level[storage, t] == 0.5 * F[storage] + Storage_in[storage, t] * eff_in - Storage_out[storage, t] / eff_out
                    )
                else:
                    prev_t = PERIODS[i - 1]
                    model.add_linear_constraint(
                        Storage_level[storage, t] == Storage_level[storage, prev_t] + Storage_in[storage, t] * eff_in - Storage_out[storage, t] / eff_out
                    )
            
            # Storage capacity
            for t in PERIODS:
                model.add_linear_constraint(Storage_level[storage, t] <= F[storage])
            
            # Cyclic storage
            first_t = PERIODS[0]
            last_t = PERIODS[-1]
            model.add_linear_constraint(Storage_level[storage, last_t] == 0.5 * F[storage])
    
    if verbose:
        print("  Constraints added.")

    # Define objective function
    def annualized_cost(tech):
        lt = lifetime[tech]
        ir = i_rate
        crf = ir * (1 + ir)**lt / ((1 + ir)**lt - 1) if lt > 0 else 0
        return c_inv[tech] * crf

    investment_cost = sum(F[tech] * annualized_cost(tech) for tech in TECHNOLOGIES)
    maintenance_cost = sum(F[tech] * c_maint[tech] for tech in TECHNOLOGIES)
    
    operating_cost = 0
    if 'GAS_PLANT' in TECH_NOSTORAGE and 'GAS' in c_op:
        gas_cost_per_gwh = c_op['GAS']
        for t in PERIODS:
            gas_consumption = -F_t['GAS_PLANT', t] * layers_in_out.loc['GAS_PLANT', 'GAS']
            operating_cost += gas_consumption * gas_cost_per_gwh

    if 'GRID' in TECH_NOSTORAGE and 'GRID' in c_op:
        grid_cost_per_gwh = c_op['GRID']
        for t in PERIODS:
            grid_consumption = F_t['GRID', t]
            operating_cost += grid_consumption * grid_cost_per_gwh

    total_cost = investment_cost + maintenance_cost + operating_cost
    model.set_objective(total_cost, poi.ObjectiveSense.Minimize)
    
    if verbose:
        print("  Objective function set.")

    # Solve the model
    if verbose:
        print("\nSolving the model...")
    model.optimize()

    # Get results
    term_status = model.get_model_attribute(poi.ModelAttribute.TerminationStatus)
    
    result = {
        'model': model,
        'variables': {
            'F': F,
            'F_t': F_t,
            'Storage_in': Storage_in,
            'Storage_out': Storage_out,
            'Storage_level': Storage_level
        },
        'status': term_status
    }

    if verbose:
        print("\n" + "="*70)
        print("RESULTS")
        print("="*70)
        print(f"  Termination status: {term_status}")

    if term_status == poi.TerminationStatusCode.OPTIMAL:
        obj_val = model.get_model_attribute(poi.ModelAttribute.ObjectiveValue)
        result['objective'] = obj_val
        
        # Extract solution
        solution = {}
        for tech in TECHNOLOGIES:
            val = model.get_value(F[tech])
            if val > 1e-6:
                solution[tech] = val
        result['solution'] = solution
        
        if verbose:
            print(f"  Objective value: {obj_val:.4f} M€")
            print("\n  Installed Capacities (F):")
            for tech, val in solution.items():
                print(f"    - {tech}: {val:.4f}")
            print("\n✓ PyOptInterface toy model solved successfully.")
    else:
        if verbose:
            print("\n✗ Could not find the optimal solution.")

    return result


if __name__ == "__main__":
    # Allow standalone execution for testing
    from data_loader import create_toy_data
    
    print("Running toy model in standalone mode...")
    data = create_toy_data()
    print("  Toy data loaded.")
    
    result = build_toy_model(data, solver='gurobi', verbose=True)

