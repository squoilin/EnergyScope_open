# Toy Model for EnergyScope - AMPL Version
# Simplified model for validating linopy implementation
# 5 technologies, 3 layers, 24 time periods

#########################
### SETS
#########################

set TECHNOLOGIES;
set STORAGE_TECH within TECHNOLOGIES;
set TECH_NOSTORAGE := TECHNOLOGIES diff STORAGE_TECH;
set LAYERS;
set PERIODS := 1..24;

#########################
### PARAMETERS
#########################

# Technology parameters
param f_max {TECHNOLOGIES} >= 0;
param f_min {TECHNOLOGIES} >= 0;
param c_inv {TECHNOLOGIES} >= 0;  # M€/GW or M€/GWh for storage
param c_maint {TECHNOLOGIES} >= 0;  # M€/GW/year
param lifetime {TECHNOLOGIES} >= 0;
param i_rate > 0;  # discount rate

# Layers in/out matrix
param layers_in_out {TECHNOLOGIES, LAYERS};

# Time-varying capacity factors
param c_p_t {TECHNOLOGIES, PERIODS} >= 0, <= 1 default 1;

# Demand
param demand {PERIODS} >= 0;

# Storage parameters
param storage_charge_eff {STORAGE_TECH} >= 0, <= 1 default 0.95;
param storage_discharge_eff {STORAGE_TECH} >= 0, <= 1 default 0.95;

# Operating costs for resources
param c_op_gas >= 0 default 50;  # M€/GWh
param c_op_grid >= 0 default 100;  # M€/GWh

#########################
### VARIABLES
#########################

# Installed capacity
var F {j in TECHNOLOGIES} >= f_min[j], <= f_max[j];

# Operation level
var F_t {TECH_NOSTORAGE, PERIODS} >= 0;

# Storage variables
var Storage_in {STORAGE_TECH, PERIODS} >= 0;
var Storage_out {STORAGE_TECH, PERIODS} >= 0;
var Storage_level {STORAGE_TECH, PERIODS} >= 0;

#########################
### CONSTRAINTS
#########################

# 1. Capacity limits
subject to capacity_limit {j in TECH_NOSTORAGE, t in PERIODS}:
    F_t[j,t] <= F[j] * c_p_t[j,t];

# 2. Energy balance (END_USE layer only - simplified)
subject to energy_balance {t in PERIODS}:
    sum {j in TECH_NOSTORAGE} (F_t[j,t] * layers_in_out[j,'END_USE'])
    + sum {s in STORAGE_TECH} (Storage_out[s,t] * storage_discharge_eff[s] 
                               - Storage_in[s,t] / storage_charge_eff[s])
    >= demand[t];

# 3. Electricity balance
subject to electricity_balance {t in PERIODS}:
    sum {j in TECH_NOSTORAGE} (F_t[j,t] * layers_in_out[j,'ELECTRICITY'])
    - sum {s in STORAGE_TECH} (Storage_in[s,t] - Storage_out[s,t])
    >= 0;

# 4. Storage level evolution
subject to storage_balance {s in STORAGE_TECH, t in PERIODS}:
    Storage_level[s,t] = 
        (if t = 1 then 0.5 * F[s] else Storage_level[s,t-1]) +
        Storage_in[s,t] * storage_charge_eff[s] -
        Storage_out[s,t] / storage_discharge_eff[s];

# 5. Storage capacity limit
subject to storage_capacity {s in STORAGE_TECH, t in PERIODS}:
    Storage_level[s,t] <= F[s];

# 6. Cyclic storage constraint
subject to storage_cyclic {s in STORAGE_TECH}:
    Storage_level[s,24] = 0.5 * F[s];

#########################
### OBJECTIVE
#########################

# Annualized investment cost (using capital recovery factor)
var Investment_cost = sum {j in TECHNOLOGIES} (
    F[j] * c_inv[j] * i_rate * (1 + i_rate) ^ lifetime[j] / 
    ((1 + i_rate) ^ lifetime[j] - 1)
);

# Maintenance cost (annual)
var Maintenance_cost = sum {j in TECHNOLOGIES} (F[j] * c_maint[j]);

# Operating cost (gas consumption by gas plant)
var Operating_cost = 
    sum {t in PERIODS} (
        F_t['GAS_PLANT',t] * abs(layers_in_out['GAS_PLANT','GAS']) * c_op_gas +
        F_t['GRID',t] * c_op_grid
    );

minimize TotalCost: Investment_cost + Maintenance_cost + Operating_cost;


