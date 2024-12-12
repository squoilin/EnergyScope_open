# Parameters

## avail
**Description:**  
Yearly availability of resources.

**Definition:**  
`avail {RESOURCES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[GWh/year]

**Usage:**  
Defines the annual resource availability for each resource type.

---

## c_inv
**Description:**  
Investment cost per unit reference size for each technology.

**Definition:**  
`c_inv {TECHNOLOGIES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[MCHF/GW or MCHF/GWh for STORAGE_TECH]

**Usage:**  
Used to calculate total investment costs for technologies.

---

## c_maint
**Description:**  
Operation and maintenance (O&M) cost per unit reference size for each technology.

**Definition:**  
`c_maint {TECHNOLOGIES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[MCHF/GW/year or MCHF/GWh for STORAGE_TECH]

**Usage:**  
Used to calculate total O&M costs for technologies.

---

## c_op
**Description:**  
Operational cost of resources per period.

**Definition:**  
`c_op {RESOURCES, PERIODS} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[MCHF/GWh]

**Usage:**  
Defines the operational cost for each resource in each period.

---

## c_p
**Description:**  
Annual capacity factor of each technology.

**Definition:**  
`c_p {TECHNOLOGIES} >= 0, <= 1 default 1;`

**Bounds:**  
`>= 0`, `<= 1`, default `1`

**Units:**  
Dimensionless

**Usage:**  
Determines the annual operational capacity of technologies.

---

## c_p_t
**Description:**  
Monthly capacity factor of each technology.

**Definition:**  
`c_p_t {TECHNOLOGIES, PERIODS} >= 0, <= 1 default 1;`

**Bounds:**  
`>= 0`, `<= 1`, default `1`

**Units:**  
Dimensionless

**Usage:**  
Determines the operational capacity of technologies on a monthly basis.

---

## end_uses_demand_year
**Description:**  
Yearly end-use demand by type and sector.

**Definition:**  
`end_uses_demand_year {END_USES_INPUT, SECTORS} >= 0 default 0;`

**Bounds:**  
`>= 0`, default `0`

**Units:**  
[GWh/year]

**Usage:**  
Input to compute `end_uses_input`.

---

## end_uses_input
**Description:**  
Total yearly demand for each end-use type, aggregated over all sectors.

**Definition:**  
`end_uses_input {i in END_USES_INPUT} := sum {s in SECTORS} (end_uses_demand_year[i,s]);`

**Bounds:**  
Derived from `end_uses_demand_year`

**Units:**  
[GWh/year]

**Usage:**  
Aggregates sectoral demands to provide total end-use demands.

---

## f_max
**Description:**  
Maximum feasible installed capacity for each technology.

**Definition:**  
`f_max {TECHNOLOGIES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[GW], [GWh for STORAGE_TECH]

**Usage:**  
Defines the upper operational limits for technology capacities.

---

## f_min
**Description:**  
Minimum feasible installed capacity for each technology.

**Definition:**  
`f_min {TECHNOLOGIES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[GW], [GWh for STORAGE_TECH]

**Usage:**  
Defines the lower operational limits for technology capacities.

---

## fmax_perc
**Description:**  
Maximum percentage of total output a technology can produce.

**Definition:**  
`fmax_perc {TECHNOLOGIES} >= 0, <= 1 default 1;`

**Bounds:**  
`>= 0`, `<= 1`, default `1`

**Units:**  
Fraction of total output

**Usage:**  
Limits the maximum share of total output a technology can produce.

---

## fmin_perc
**Description:**  
Minimum percentage of total output a technology must produce.

**Definition:**  
`fmin_perc {TECHNOLOGIES} >= 0, <= 1 default 0;`

**Bounds:**  
`>= 0`, `<= 1`, default `0`

**Units:**  
Fraction of total output

**Usage:**  
Sets the minimum share of total output a technology must produce.

---

## gwp_constr
**Description:**  
Global Warming Potential (GWP) emissions associated with the construction of technologies.

**Definition:**  
`gwp_constr {TECHNOLOGIES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[ktCO2-eq./GW]

**Usage:**  
Accounts for GWP emissions from constructing technologies.

---

## gwp_op
**Description:**  
GWP emissions associated with the operational use of resources.

**Definition:**  
`gwp_op {RESOURCES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[ktCO2-eq./GWh]

**Usage:**  
Calculates emissions from resource utilization annually.

---

## heating_month
**Description:**  
Monthly distribution factor for space heating demand.

**Definition:**  
`heating_month {PERIODS} >= 0, <= 1;`

**Bounds:**  
`>= 0`, `<= 1` for each period, summing to 1 across all periods.

**Units:**  
Dimensionless fraction

**Usage:**  
Distributes annual space heating demand across monthly periods.

---

## i_rate
**Description:**  
Discount rate (real).

**Definition:**  
`i_rate > 0;`

**Bounds:**  
`> 0`

**Units:**  
Dimensionless

**Role:**  
Used in annualization factor calculation for technologies.

---

## layers_in_out
**Description:**  
Input-output mapping of resources and technologies to layers.

**Definition:**  
`layers_in_out {RESOURCES union TECHNOLOGIES diff STORAGE_TECH, LAYERS};`

**Units:**  
[GWh/GW or analogous, depends on context]

**Usage:**  
Defines the relationships between resources, technologies, and energy layers.

---

## lighting_month
**Description:**  
Monthly distribution factor for lighting demand.

**Definition:**  
`lighting_month {PERIODS} >= 0, <= 1;`

**Bounds:**  
`>= 0`, `<= 1` for each period, summing to 1 across all periods.

**Units:**  
Dimensionless fraction

**Usage:**  
Distributes annual lighting demand across monthly periods.

---

## lifetime
**Description:**  
Lifetime of each technology.

**Definition:**  
`lifetime {TECHNOLOGIES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[years]

**Usage:**  
Determines the operational lifespan for technologies, influencing depreciation and replacement.

---

## loss_coeff
**Description:**  
Loss coefficients in networks (e.g., electricity grid, DHN).

**Definition:**  
`loss_coeff {END_USES_TYPES} >= 0 default 0;`

**Bounds:**  
`>= 0`, default `0`

**Units:**  
Fractional loss

**Usage:**  
Models energy losses within specific end-use networks.

---

## peak_dhn_factor
**Description:**  
Factor associated with peak District Heating Network (DHN) conditions.

**Definition:**  
`peak_dhn_factor >= 0;`

**Units:**  
Dimensionless

**Usage:**  
Adjusts for peak demand scenarios in District Heating Networks (DHN).

---

## share_freight_train_max
**Description:**  
Maximum penetration limit for train usage in freight transportation.

**Definition:**  
`share_freight_train_max >= 0, <= 1;`

**Bounds:**  
`>= 0`, `<= 1`

**Units:**  
Dimensionless fraction

**Usage:**  
Sets the upper allowable range for train usage in freight transport.

---

## share_freight_train_min
**Description:**  
Minimum penetration limit for train usage in freight transportation.

**Definition:**  
`share_freight_train_min >= 0, <= 1;`

**Bounds:**  
`>= 0`, `<= 1`

**Units:**  
Dimensionless fraction

**Usage:**  
Sets the lower allowable range for train usage in freight transport.

---

## share_heat_dhn_max
**Description:**  
Maximum penetration limit for DHN in low-temperature heating.

**Definition:**  
`share_heat_dhn_max >= 0, <= 1;`

**Bounds:**  
`>= 0`, `<= 1`

**Units:**  
Dimensionless fraction

**Usage:**  
Limits the upper share of DHN in providing low-temperature heating.

---

## share_heat_dhn_min
**Description:**  
Minimum penetration limit for DHN in low-temperature heating.

**Definition:**  
`share_heat_dhn_min >= 0, <= 1;`

**Bounds:**  
`>= 0`, `<= 1`

**Units:**  
Dimensionless fraction

**Usage:**  
Limits the lower share of DHN in providing low-temperature heating.

---

## share_mobility_public_max
**Description:**  
Maximum share limit for public mobility as a fraction of total mobility.

**Definition:**  
`share_mobility_public_max >= 0, <= 1;`

**Bounds:**  
`>= 0`, `<= 1`

**Units:**  
Dimensionless fraction

**Usage:**  
Constrains the upper proportion of mobility attributed to public transportation.

---

## share_mobility_public_min
**Description:**  
Minimum share limit for public mobility as a fraction of total mobility.

**Definition:**  
`share_mobility_public_min >= 0, <= 1;`

**Bounds:**  
`>= 0`, `<= 1`

**Units:**  
Dimensionless fraction

**Usage:**  
Constrains the lower proportion of mobility attributed to public transportation.

---

## tau
**Description:**  
Annualization factor for cost calculation.

**Definition:**  
`tau {TECHNOLOGIES} := i_rate * (1 + i_rate)^{lifetime[i]} / ((1 + i_rate)^{lifetime[i]} - 1);`

**Units:**  
Dimensionless

**Usage:**  
Converts capital costs into an equivalent uniform annual expense, considering discounting over the technology’s lifetime.

---

## total_time
**Description:**  
Total duration of all periods.

**Definition:**  
`total_time := sum {t in PERIODS} (t_op[t]);`

**Units:**  
[h]

**Usage:**  
Aggregates the duration of all periods for simplifying equations.

---

## t_op
**Description:**  
Duration of each period.

**Definition:**  
`t_op {PERIODS};`

**Bounds:**  
Defined per period.

**Units:**  
[h]

**Usage:**  
Defines the length of each time period in hours.

---

This completes the **Parameters** section. Refer to **Sets** and **Variables** for foundational context and inputs.