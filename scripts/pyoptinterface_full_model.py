"""
Energyscope Full Model implemented in PyOptInterface.
"""

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

    # 1. Load data
    data = create_full_dataset()
    print("  Full ESTD data loaded.")

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

    f_max = data['parameters']['f_max'].to_dict()
    f_min = data['parameters']['f_min'].to_dict()
    c_p_t = data['parameters']['c_p_t'].to_dict()
    layers_in_out = data['parameters']['layers_in_out'].to_dict()
    
    # Reconstruct End_uses
    print("  Reconstructing End_uses...")
    End_uses = {}
    
    # Use time series for electricity
    elec_ts = data['parameters']['electricity_time_series'].to_dict()
    for (h, td), val in elec_ts.items():
        End_uses['ELECTRICITY', h, td] = val

    # Use time series for heat
    heat_ts = data['parameters']['heating_time_series'].to_dict()
    for (h, td), val in heat_ts.items():
        End_uses['HEAT', h, td] = val

    # Use annual average for others
    end_uses_annual = data['parameters']['end_uses_demand_year'].to_dict()
    for layer, annual_demand in end_uses_annual.items():
        if layer not in ['ELECTRICITY', 'HEAT']:
            avg_demand = annual_demand / 8760
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    End_uses[layer, h, td] = avg_demand
    print("  End_uses reconstructed.")

    # 2. Create a model
    model = gurobi.Model()
    print("  Model created with Gurobi backend.")

    # 3. Define variables
    F = {
        tech: model.add_variable(lb=f_min.get(tech, 0), ub=f_max.get(tech, float('inf')), name=f"F_{tech}")
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

    TotalCost = model.add_variable(lb=0, name="TotalCost")
    TotalGWP = model.add_variable(lb=0, name="TotalGWP")

    print("  Variables created.")

    # 4. Add constraints
    print("  Adding constraints...")
    
    # Energy Balance
    for j in TECH_NOSTORAGE:
        for h in HOURS:
            for td in TYPICAL_DAYS:
                cf = c_p_t.get((j, h, td), 1.0)
                model.add_linear_constraint(F_t[j, h, td] - F[j] * cf <= 0)

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
                        balance_expr += Storage_out.get((s, l, h, td), 0) - Storage_in.get((s, l, h, td), 0)

                demand = End_uses.get((l, h, td), 0)
                if hasattr(balance_expr, 'is_expression'):
                    model.add_linear_constraint(balance_expr - demand == 0)

    # Resources
    avail = data['parameters']['avail'].to_dict()
    t_op = data['parameters']['t_op'].to_dict()
    for i in RESOURCES:
        if i in avail:
            if pd.isna(avail[i]) or avail[i] == float('inf'):
                print(f"DEBUG: Skipping resource '{i}' with availability {avail[i]}")
                continue
            annual_consumption = sum(F_t[i, h, td] * t_op.get((h, td), 1.0) for h in HOURS for td in TYPICAL_DAYS)
            model.add_linear_constraint(annual_consumption - avail[i] <= 0)

    # Storage
    if STORAGE_TECH:
        storage_eff_in = data['parameters']['storage_eff_in'].to_dict()
        storage_eff_out = data['parameters']['storage_eff_out'].to_dict()
        storage_losses = data['parameters'].get('storage_losses', pd.Series()).to_dict()
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
                    model.add_linear_constraint(Storage_level[j, t] - (Storage_level[j, last_period] * (1.0 - loss_rate) + t_op_val * (storage_input - storage_output)) == 0)
                else:
                    model.add_linear_constraint(Storage_level[j, t] - (Storage_level[j, t-1] * (1.0 - loss_rate) + t_op_val * (storage_input - storage_output)) == 0)
            
            for t in PERIODS:
                model.add_linear_constraint(Storage_level[j, t] - F[j] <= 0)

    print("  Constraints added.")

    # 5. Define objective function
    print("  Adding cost and GWP constraints and objective...")
    c_inv = data['parameters']['c_inv'].to_dict()
    c_maint = data['parameters']['c_maint'].to_dict()
    c_op = data['parameters']['c_op'].to_dict()
    lifetime = data['parameters']['lifetime'].to_dict()
    i_rate = data['parameters']['i_rate']

    investment_total = sum(i_rate * (1 + i_rate)**lifetime[j] / ((1 + i_rate)**lifetime[j] - 1) * c_inv[j] * F[j] for j in ALL_TECH)
    maintenance_total = sum(c_maint[j] * F[j] for j in ALL_TECH)
    operating_total = sum(c_op[i] * sum(F_t[i, h, td] * t_op.get((h,td), 1.0) for h in HOURS for td in TYPICAL_DAYS) for i in RESOURCES if i in c_op)
    model.add_linear_constraint(TotalCost - (investment_total + maintenance_total + operating_total) == 0)

    gwp_constr_param = data['parameters']['gwp_constr'].to_dict()
    gwp_op_param = data['parameters']['gwp_op'].to_dict()
    gwp_limit_param = data['parameters'].get('gwp_limit', float('inf'))
    gwp_constr_total = sum(gwp_constr_param.get(j, 0) * F[j] for j in ALL_TECH)
    gwp_op_total = sum(gwp_op_param[i] * sum(F_t[i, h, td] * t_op.get((h,td), 1.0) for h in HOURS for td in TYPICAL_DAYS) for i in RESOURCES if i in gwp_op_param)
    model.add_linear_constraint(TotalGWP - (gwp_constr_total + gwp_op_total) == 0)
    if gwp_limit_param < float('inf'):
        model.add_linear_constraint(TotalGWP - gwp_limit_param <= 0)
    
    model.set_objective(TotalCost, poi.ObjectiveSense.Minimize)
    print("  Objective function set.")

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
        print("\n✓ PyOptInterface full model ran successfully.")
    else:
        print("\n✗ Could not find the optimal solution.")
        
        # IIS computation is not straightforward with pyoptinterface's C-level integration
        print("\nCould not compute IIS due to pyoptinterface limitations.")


if __name__ == "__main__":
    build_and_run_full_model()
