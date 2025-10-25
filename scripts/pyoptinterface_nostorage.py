"""
PyOptInterface model WITHOUT storage - to test.
"""
import pyoptinterface as poi
from pyoptinterface import gurobi
import pandas as pd
from energyscope.linopy_backend.data_loader_full import create_full_dataset

data = create_full_dataset()
print("Data loaded.")

# Extract sets
TECHNOLOGIES = data['sets']['TECHNOLOGIES']
STORAGE_TECH = data['sets']['STORAGE_TECH']
RESOURCES = data['sets']['RESOURCES']
LAYERS = data['sets']['LAYERS']
HOURS = data['sets']['HOURS']
TYPICAL_DAYS = data['sets']['TYPICAL_DAYS']
PERIODS = data['sets']['PERIODS']
T_H_TD = data['sets']['T_H_TD']
END_USES_TYPES = data['sets']['END_USES_TYPES']
TECHNOLOGIES_OF_END_USES_CATEGORY = data['sets'].get('TECHNOLOGIES_OF_END_USES_CATEGORY', {})

# Exclude storage from ALL_TECH
ALL_TECH = TECHNOLOGIES  # NO STORAGE!
TECH_NOSTORAGE = [t for t in ALL_TECH if t not in STORAGE_TECH]
ENTITIES_WITH_F_T = RESOURCES + TECH_NOSTORAGE

print(f"ALL_TECH: {len(ALL_TECH)}")
print(f"STORAGE_TECH: {len(STORAGE_TECH)}")
print(f"ENTITIES_WITH_F_T: {len(ENTITIES_WITH_F_T)}")

# Parameters
f_max = data['parameters']['f_max'].to_dict()
f_min = data['parameters']['f_min'].to_dict()
layers_in_out = data['parameters']['layers_in_out'].to_dict()
t_op = data['parameters']['t_op'].to_dict()
c_p_t = data['parameters']['c_p_t'].to_dict()
c_inv = data['parameters']['c_inv'].to_dict()
c_maint = data['parameters']['c_maint'].to_dict()
c_op = data['parameters']['c_op'].to_dict()
lifetime = data['parameters']['lifetime'].to_dict()
i_rate = data['parameters']['i_rate']
avail = data['parameters']['avail'].to_dict()
loss_network = data['parameters'].get('loss_network', {})
if isinstance(loss_network, pd.Series):
    loss_network = loss_network.to_dict()

electricity_time_series = data['parameters']['electricity_time_series'].to_dict()
heating_time_series = data['parameters']['heating_time_series'].to_dict()
mob_pass_time_series = data['parameters'].get('mob_pass_time_series', {})
mob_freight_time_series = data['parameters'].get('mob_freight_time_series', {})

end_uses_input = {}
if 'end_uses_demand_year' in data['parameters']:
    eud_year = data['parameters']['end_uses_demand_year']
    if eud_year.index.nlevels > 1:
        for eu in eud_year.index.get_level_values(0).unique():
            end_uses_input[eu] = eud_year.loc[eu].sum()
total_time = sum(t_op.values())

# Create model
model = gurobi.Model()

# Variables (NO STORAGE!)
F = {tech: model.add_variable(lb=f_min.get(tech, 0), ub=f_max.get(tech, float('inf')), name=f"F_{tech}") for tech in ALL_TECH}
F_t = {(entity, h, td): model.add_variable(lb=0, name=f"F_t_{entity}_{h}_{td}") for entity in ENTITIES_WITH_F_T for h in HOURS for td in TYPICAL_DAYS}
End_uses = {(l, h, td): model.add_variable(lb=0, name=f"End_uses_{l}_{h}_{td}") for l in LAYERS for h in HOURS for td in TYPICAL_DAYS}
Share_heat_dhn = model.add_variable(lb=0, ub=1, name="Share_heat_dhn")
Share_mobility_public = model.add_variable(lb=0, ub=1, name="Share_mobility_public")
Share_freight_train = model.add_variable(lb=0, ub=1, name="Share_freight_train")
Share_freight_road = model.add_variable(lb=0, ub=1, name="Share_freight_road")
Share_freight_boat = model.add_variable(lb=0, ub=1, name="Share_freight_boat")
Network_losses = {(eut, h, td): model.add_variable(lb=0, name=f"Network_losses_{eut}_{h}_{td}") for eut in END_USES_TYPES for h in HOURS for td in TYPICAL_DAYS}

Shares_mobility_passenger = {}
if 'MOBILITY_PASSENGER' in TECHNOLOGIES_OF_END_USES_CATEGORY:
    for tech in TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_PASSENGER']:
        if tech not in STORAGE_TECH:  # Skip storage techs
            Shares_mobility_passenger[tech] = model.add_variable(lb=0, name=f"Shares_mob_pass_{tech}")

Shares_mobility_freight = {}
if 'MOBILITY_FREIGHT' in TECHNOLOGIES_OF_END_USES_CATEGORY:
    for tech in TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_FREIGHT']:
        if tech not in STORAGE_TECH:  # Skip storage techs
            Shares_mobility_freight[tech] = model.add_variable(lb=0, name=f"Shares_mob_freight_{tech}")

TotalCost = model.add_variable(lb=0, name="TotalCost")
TotalGWP = model.add_variable(lb=0, name="TotalGWP")

print("Variables created (NO STORAGE).")

# Add constraints (copy from full model but simplified)
# ... (freight shares, network losses, end-uses, layer balance, etc.)
# [Abbreviated for space - using same logic as before]

model.add_linear_constraint(Share_freight_train + Share_freight_road + Share_freight_boat == 1)

for eut in END_USES_TYPES:
    loss_pct = loss_network.get(eut, 0)
    for h in HOURS:
        for td in TYPICAL_DAYS:
            production = sum(layers_in_out.get((entity, eut), 0) * F_t[entity, h, td] for entity in ENTITIES_WITH_F_T if layers_in_out.get((entity, eut), 0) > 0)
            model.add_linear_constraint(Network_losses[eut, h, td] == production * loss_pct)

for l in LAYERS:
    for h in HOURS:
        for td in TYPICAL_DAYS:
            t_op_val = t_op.get((h, td), 1.0)
            if l == "ELECTRICITY":
                base = end_uses_input.get("ELECTRICITY", 0) / total_time if total_time > 0 else 0
                lighting = end_uses_input.get("LIGHTING", 0) * electricity_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                model.add_linear_constraint(End_uses[l, h, td] == base + lighting)
            elif l == "HEAT_LOW_T_DHN":
                hw = end_uses_input.get("HEAT_LOW_T_HW", 0) / total_time if total_time > 0 else 0
                sh = end_uses_input.get("HEAT_LOW_T_SH", 0) * heating_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                model.add_linear_constraint(End_uses[l, h, td] == (hw + sh) * Share_heat_dhn + Network_losses[l, h, td])
            elif l == "HEAT_LOW_T_DECEN":
                hw = end_uses_input.get("HEAT_LOW_T_HW", 0) / total_time if total_time > 0 else 0
                sh = end_uses_input.get("HEAT_LOW_T_SH", 0) * heating_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                model.add_linear_constraint(End_uses[l, h, td] == (hw + sh) * (1 - Share_heat_dhn))
            elif l == "MOB_PUBLIC":
                mob_pass = end_uses_input.get("MOBILITY_PASSENGER", 0) * mob_pass_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                model.add_linear_constraint(End_uses[l, h, td] == mob_pass * Share_mobility_public)
            elif l == "MOB_PRIVATE":
                mob_pass = end_uses_input.get("MOBILITY_PASSENGER", 0) * mob_pass_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                model.add_linear_constraint(End_uses[l, h, td] == mob_pass * (1 - Share_mobility_public))
            elif l == "MOB_FREIGHT_RAIL":
                mob_freight = end_uses_input.get("MOBILITY_FREIGHT", 0) * mob_freight_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                model.add_linear_constraint(End_uses[l, h, td] == mob_freight * Share_freight_train)
            elif l == "MOB_FREIGHT_ROAD":
                mob_freight = end_uses_input.get("MOBILITY_FREIGHT", 0) * mob_freight_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                model.add_linear_constraint(End_uses[l, h, td] == mob_freight * Share_freight_road)
            elif l == "MOB_FREIGHT_BOAT":
                mob_freight = end_uses_input.get("MOBILITY_FREIGHT", 0) * mob_freight_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                model.add_linear_constraint(End_uses[l, h, td] == mob_freight * Share_freight_boat)
            elif l == "HEAT_HIGH_T":
                ht_demand = end_uses_input.get("HEAT_HIGH_T", 0) / total_time if total_time > 0 else 0
                model.add_linear_constraint(End_uses[l, h, td] == ht_demand)
            else:
                model.add_linear_constraint(End_uses[l, h, td] == 0)

for l in LAYERS:
    for h in HOURS:
        for td in TYPICAL_DAYS:
            balance_expr = sum(layers_in_out.get((entity, l), 0) * F_t[entity, h, td] for entity in ENTITIES_WITH_F_T)
            model.add_linear_constraint(balance_expr == End_uses[l, h, td])

for j in TECH_NOSTORAGE:
    for h in HOURS:
        for td in TYPICAL_DAYS:
            cf = c_p_t.get((j, h, td), 1.0)
            model.add_linear_constraint(F_t[j, h, td] <= F[j] * cf)

if 'MOBILITY_PASSENGER' in TECHNOLOGIES_OF_END_USES_CATEGORY and Shares_mobility_passenger:
    for j in TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_PASSENGER']:
        if j in TECH_NOSTORAGE:
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    t_op_val = t_op.get((h, td), 1.0)
                    mob_pass_demand = end_uses_input.get("MOBILITY_PASSENGER", 0) * mob_pass_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    model.add_linear_constraint(F_t[j, h, td] == Shares_mobility_passenger[j] * mob_pass_demand)

if 'MOBILITY_FREIGHT' in TECHNOLOGIES_OF_END_USES_CATEGORY and Shares_mobility_freight:
    for j in TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_FREIGHT']:
        if j in TECH_NOSTORAGE:
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    t_op_val = t_op.get((h, td), 1.0)
                    mob_freight_demand = end_uses_input.get("MOBILITY_FREIGHT", 0) * mob_freight_time_series.get((h, td), 0) / t_op_val if t_op_val > 0 else 0
                    model.add_linear_constraint(F_t[j, h, td] == Shares_mobility_freight[j] * mob_freight_demand)

for i in RESOURCES:
    if i in avail and not (pd.isna(avail[i]) or avail[i] == float('inf')):
        annual_consumption = sum(F_t[i, h, td] * t_op.get((h, td), 1.0) for h in HOURS for td in TYPICAL_DAYS)
        model.add_linear_constraint(annual_consumption <= avail[i])

c_grid_extra = data['parameters'].get('c_grid_extra', 0)
if 'GRID' in ALL_TECH and c_grid_extra > 0:
    grid_tech = ['WIND_ONSHORE', 'WIND_OFFSHORE', 'PV']
    grid_f = sum(F[t] for t in grid_tech if t in F)
    grid_f_min = sum(f_min.get(t, 0) for t in grid_tech if t in f_min)
    model.add_linear_constraint(F['GRID'] == 1 + (c_grid_extra / c_inv.get('GRID', 1)) * (grid_f - grid_f_min))

if 'DHN' in ALL_TECH:
    dhn_capacity = sum(layers_in_out.get((j, "HEAT_LOW_T_DHN"), 0) * F[j] for j in TECH_NOSTORAGE if layers_in_out.get((j, "HEAT_LOW_T_DHN"), 0) > 0)
    model.add_linear_constraint(F['DHN'] == dhn_capacity)

if 'EFFICIENCY' in ALL_TECH:
    model.add_linear_constraint(F['EFFICIENCY'] == 1 / (1 + i_rate))

print("Constraints added.")

# Cost
investment_total = sum(i_rate * (1 + i_rate)**lifetime.get(j, 0) / ((1 + i_rate)**lifetime.get(j, 0) - 1) * c_inv.get(j, 0) * F[j] for j in ALL_TECH if j in c_inv and j in lifetime and lifetime.get(j, 0) > 0)
maintenance_total = sum(c_maint.get(j, 0) * F[j] for j in ALL_TECH)
operating_total = sum(c_op.get(i, 0) * sum(F_t[i, h, td] * t_op.get((h,td), 1.0) for h in HOURS for td in TYPICAL_DAYS) for i in RESOURCES if i in c_op)
model.add_linear_constraint(TotalCost == investment_total + maintenance_total + operating_total)

model.set_objective(TotalCost, poi.ObjectiveSense.Minimize)

print("Solving...")
model.optimize()

status = model.get_model_attribute(poi.ModelAttribute.TerminationStatus)
print(f"\nStatus: {status}")
if status == poi.TerminationStatusCode.OPTIMAL:
    obj_val = model.get_model_attribute(poi.ModelAttribute.ObjectiveValue)
    print(f"Objective: {obj_val:.2f}")
else:
    print("INFEASIBLE!")

