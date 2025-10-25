"""
Energyscope Core Model implemented in PyOptInterface.
"""

import pyoptinterface as poi
from pyoptinterface import highs
import pandas as pd
from energyscope.linopy_backend.test_data_core import create_minimal_core_data

def build_and_run_core_model():
    """
    Builds and solves the Energyscope core model using pyoptinterface.
    """
    print("="*70)
    print("Building and running PyOptInterface core model")
    print("="*70)

    # 1. Load data
    data = create_minimal_core_data()
    print("  Minimal core data loaded.")

    # Extract sets and parameters
    TECHNOLOGIES = data['sets']['TECHNOLOGIES']
    STORAGE_TECH = data['sets']['STORAGE_TECH']
    RESOURCES = data['sets']['RESOURCES']
    LAYERS = data['sets']['LAYERS']
    HOURS = data['sets']['HOURS']
    TYPICAL_DAYS = data['sets']['TYPICAL_DAYS']
    END_USES_TYPES = data['sets']['END_USES_TYPES']
    ALL_TECH = TECHNOLOGIES + STORAGE_TECH
    TECH_NOSTORAGE = [t for t in ALL_TECH if t not in STORAGE_TECH]
    ENTITIES_WITH_F_T = RESOURCES + TECH_NOSTORAGE

    f_max = data['parameters']['f_max']
    f_min = data['parameters']['f_min']
    c_p_t = data['parameters']['c_p_t']
    layers_in_out = data['parameters']['layers_in_out']
    End_uses = data['time_series'].get('End_uses', data['time_series'].get('end_uses_demand', None))

    # 2. Create a model
    model = highs.Model()
    print("  Model created with HiGHS backend.")

    # 3. Define variables
    F = {
        tech: model.add_variable(lb=f_min[tech], ub=f_max[tech], name=f"F_{tech}")
        for tech in ALL_TECH
    }

    F_t = {
        (entity, h, td): model.add_variable(lb=0, name=f"F_t_{entity}_{h}_{td}")
        for entity in ENTITIES_WITH_F_T for h in HOURS for td in TYPICAL_DAYS
    }

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
            for s in STORAGE_TECH for t in data['sets']['PERIODS']
        }

    print("  Variables created.")

    # 4. Add constraints (starting with energy balance)
    print("  Adding energy balance constraints...")
    
    # Constraint 1.1: capacity_factor_t
    for j in TECH_NOSTORAGE:
        for h in HOURS:
            for td in TYPICAL_DAYS:
                cf = c_p_t.get((j, h, td), 1.0)
                model.add_linear_constraint(F_t[j, h, td] - F[j] * cf <= 0)

    # Constraint 1.2: layer_balance
    for l in LAYERS:
        for h in HOURS:
            for td in TYPICAL_DAYS:
                balance_expr = 0
                for entity in ENTITIES_WITH_F_T:
                    coef = layers_in_out.get((entity, l), 0)
                    if abs(coef) > 1e-9:
                        balance_expr += F_t[entity, h, td] * coef
                
                if STORAGE_TECH:
                    for s in STORAGE_TECH:
                        balance_expr += Storage_out[s, l, h, td] - Storage_in[s, l, h, td]

                demand = End_uses.get((l, h, td), 0)
                # Only add constraint if it involves variables
                if hasattr(balance_expr, 'is_expression'):
                    model.add_linear_constraint(balance_expr - demand == 0)
    
    print("  Energy balance constraints added.")

    # ADD RESOURCES CONSTRAINTS
    print("  Adding resource constraints...")
    avail = data['parameters'].get('avail', {})
    t_op = data['parameters']['t_op']
    for i in RESOURCES:
        if i in avail:
            annual_consumption = 0
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    t_op_val = t_op.get((h, td), 1.0)
                    annual_consumption += F_t[i, h, td] * t_op_val
            model.add_linear_constraint(annual_consumption <= avail[i])
    print("  Resource constraints added.")

    # ADD STORAGE CONSTRAINTS
    print("  Adding storage constraints...")
    if STORAGE_TECH:
        storage_eff_in = data['parameters']['storage_eff_in']
        storage_eff_out = data['parameters']['storage_eff_out']
        storage_losses = data['parameters'].get('storage_losses', {s: 0 for s in STORAGE_TECH})
        PERIODS = data['sets']['PERIODS']
        T_H_TD = data['sets']['T_H_TD']

        for j in STORAGE_TECH:
            loss_rate = storage_losses.get(j, 0)
            for t in PERIODS:
                h_td_for_t = [(h, td) for (p, h, td) in T_H_TD if p == t]
                if not h_td_for_t: continue
                h, td = h_td_for_t[0]
                t_op_val = t_op.get((h, td), 1.0)
                
                storage_input = sum(Storage_in[j, l, h, td] * storage_eff_in.get((j, l), 0) for l in LAYERS)
                storage_output = sum(Storage_out[j, l, h, td] / storage_eff_out.get((j, l), 1) for l in LAYERS if storage_eff_out.get((j, l), 0) != 0)

                if t == 1:
                    last_period = PERIODS[-1]
                    model.add_linear_constraint(Storage_level[j, t] == Storage_level[j, last_period] * (1.0 - loss_rate) + t_op_val * (storage_input - storage_output))
                else:
                    model.add_linear_constraint(Storage_level[j, t] == Storage_level[j, t-1] * (1.0 - loss_rate) + t_op_val * (storage_input - storage_output))
            
            for t in PERIODS:
                model.add_linear_constraint(Storage_level[j, t] <= F[j])

    print("  Storage constraints added.")


    # 5. Define objective function
    print("  Adding cost constraints and objective...")
    TotalCost = model.add_variable(lb=0, name="TotalCost")
    c_inv = data['parameters']['c_inv']
    c_maint = data['parameters']['c_maint']
    c_op = data['parameters'].get('c_op', {})
    lifetime = data['parameters']['lifetime']
    i_rate = data['parameters']['i_rate']

    investment_total = 0
    for j in ALL_TECH:
        lt = lifetime[j]
        tau = i_rate * (1 + i_rate)**lt / ((1 + i_rate)**lt - 1)
        investment_total += tau * c_inv[j] * F[j]

    maintenance_total = sum(c_maint[j] * F[j] for j in ALL_TECH)
    
    operating_total = 0
    for i in RESOURCES:
        if i in c_op:
            annual_usage = sum(F_t[i, h, td] * t_op.get((h,td), 1.0) for h in HOURS for td in TYPICAL_DAYS)
            operating_total += c_op[i] * annual_usage

    model.add_linear_constraint(TotalCost == investment_total + maintenance_total + operating_total)
    model.set_objective(TotalCost, poi.ObjectiveSense.Minimize)
    print("  Objective function set.")

    # ADD GWP CONSTRAINTS
    print("  Adding GWP constraints...")
    gwp_constr_param = data['parameters'].get('gwp_constr', {})
    gwp_op_param = data['parameters'].get('gwp_op', {})
    gwp_limit_param = data['parameters'].get('gwp_limit', float('inf'))
    TotalGWP = model.add_variable(lb=0, name="TotalGWP")

    gwp_constr_total = sum(gwp_constr_param.get(j, 0) * F[j] for j in ALL_TECH)
    
    gwp_op_total = 0
    for i in RESOURCES:
        if i in gwp_op_param:
            annual_usage = sum(F_t[i, h, td] * t_op.get((h,td), 1.0) for h in HOURS for td in TYPICAL_DAYS)
            gwp_op_total += gwp_op_param[i] * annual_usage

    model.add_linear_constraint(TotalGWP == gwp_constr_total + gwp_op_total)
    if gwp_limit_param < float('inf'):
        model.add_linear_constraint(TotalGWP <= gwp_limit_param)
    print("  GWP constraints added.")

    # ADD NETWORK CONSTRAINTS
    print("  Adding network constraints...")
    loss_network = data['parameters'].get('loss_network', {})
    if loss_network:
        Network_losses = {
            (eut, h, td): model.add_variable(lb=0, name=f"Network_losses_{eut}_{h}_{td}")
            for eut in END_USES_TYPES for h in HOURS for td in TYPICAL_DAYS
        }
        for eut in END_USES_TYPES:
            loss_pct = loss_network.get(eut, 0)
            if loss_pct > 0:
                for h in HOURS:
                    for td in TYPICAL_DAYS:
                        production = 0
                        for entity in ENTITIES_WITH_F_T:
                            coef = layers_in_out.get((entity, eut), 0)
                            if coef > 0:
                                production += coef * F_t[entity, h, td]
                        model.add_linear_constraint(Network_losses[eut, h, td] == production * loss_pct)
    print("  Network constraints added.")

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
        print("\n  Installed Capacities (F):")
        for tech in ALL_TECH:
            val = model.get_value(F[tech])
            if val > 1e-6:
                print(f"    - {tech}: {val:.4f}")
        print("\n✓ PyOptInterface core model ran successfully.")
    else:
        print("\n✗ Could not find the optimal solution.")

if __name__ == "__main__":
    build_and_run_core_model()
