# Parameters

## end_uses_demand_year {END_USES_INPUT, SECTORS}
**Description:**  
Yearly end-use demand by type and sector.

**Domain:**  
`END_USES_INPUT x SECTORS`

**Bounds:**  
`>= 0`, default `0`

**Units:**  
[GWh/year]

**Usage:**  
Input to compute `end_uses_input`.

---

## end_uses_input {i in END_USES_INPUT}
**Description:**  
Total yearly demand for each end-use type, aggregated over all sectors.

**Definition:**  
`end_uses_input[i] = sum {s in SECTORS} end_uses_demand_year[i,s]`

**Bounds:**  
Derived from `end_uses_demand_year`

**Units:**  
[GWh/year]

---

## i_rate
**Description:**  
Discount rate (real).

**Bounds:**  
`> 0`

**Units:**  
Dimensionless

**Role:**  
Used in annualization factor calculation for technologies.

---

## share_mobility_public_min, share_mobility_public_max
**Description:**  
Minimum and maximum share limits for public mobility as a fraction of total mobility.

**Bounds:**  
`>= 0`, `<= 1`

**Units:**  
Dimensionless fraction

---

## share_freight_train_min, share_freight_train_max
**Description:**  
Min/max penetration limits for train in freight transportation.

**Bounds:**  
`>= 0`, `<= 1`

**Units:**  
Dimensionless fraction

---

## share_heat_dhn_min, share_heat_dhn_max
**Description:**  
Min/max penetration for DHN in low-temperature heating.

**Bounds:**  
`>= 0`, `<= 1`

**Units:**  
Dimensionless fraction

---

## t_op {PERIODS}
**Description:**  
Duration of each period.

**Domain:**  
`PERIODS`

**Units:**  
[h]

---

## lighting_month {PERIODS}, heating_month {PERIODS}
**Description:**  
Monthly distribution factors for lighting and space heating demand.

**Bounds:**  
`>= 0`, `<= 1` for each period, summing to 1 across all periods.

**Units:**  
Dimensionless fraction

---

## layers_in_out {RESOURCES union TECHNOLOGIES diff STORAGE_TECH, LAYERS}
**Description:**  
Input-output mapping of resources/technologies to layers.  
Represents how resources and technologies feed into or draw from certain layers.

**Units:**  
[GWh/GW or analogous, depends on context]

---

## ref_size {TECHNOLOGIES}
**Description:**  
Reference size for each technology’s capacity.

**Bounds:**  
`>= 0`

**Units:**  
[GW], [GWh] for storage tech

---

## c_inv {TECHNOLOGIES}, c_maint {TECHNOLOGIES}
**Description:**  
Investment and O&M cost per unit reference size.

**Bounds:**  
`>= 0`

**Units:**  
`c_inv`: [MCHF/GW or MCHF/GWh for storage]  
`c_maint`: [MCHF/GW/year or MCHF/GWh for storage]

---

## lifetime {TECHNOLOGIES}
**Description:**  
Lifetime of each technology.

**Bounds:**  
`>= 0`

**Units:**  
[years]

---

## f_max {TECHNOLOGIES}, f_min {TECHNOLOGIES}
**Description:**  
Max/min feasible installed capacity for each technology.

**Bounds:**  
`>= 0`

**Units:**  
[GW], [GWh for storage]

---

## fmax_perc {TECHNOLOGIES}, fmin_perc {TECHNOLOGIES}
**Description:**  
Max/min percentage constraints on output share.

**Bounds:**  
`>= 0`, `<= 1`, default `fmax_perc=1`, `fmin_perc=0`

**Units:**  
Fraction of total output

---

## c_p_t {TECHNOLOGIES, PERIODS}, c_p {TECHNOLOGIES}
**Description:**  
Capacity factors defining seasonal and annual availability.

**Bounds:**  
`>= 0`, `<= 1`, defaults: `c_p_t=1`, `c_p=1`

**Units:**  
Dimensionless

---

## tau {TECHNOLOGIES}
**Description:**  
Annualization factor for cost calculation.  
`tau[i] = i_rate * (1 + i_rate)^lifetime[i] / ((1 + i_rate)^lifetime[i] - 1)`

**Units:**  
Dimensionless

---

## gwp_constr {TECHNOLOGIES}
**Description:**  
GWP emissions associated with technology construction.

**Bounds:**  
`>= 0`

**Units:**  
[ktCO2-eq./GW]

---

## total_time
**Description:**  
Sum of all `t_op[t]`.  
`total_time = sum {t in PERIODS} t_op[t]`

**Units:**  
[h]

---

## c_op {RESOURCES, PERIODS}
**Description:**  
Cost of resources per period.

**Bounds:**  
`>= 0`

**Units:**  
[MCHF/GWh]

---

## avail {RESOURCES}
**Description:**  
Yearly availability of resources.

**Bounds:**  
`>= 0`

**Units:**  
[GWh/year]

---

## gwp_op {RESOURCES}
**Description:**  
GWP emissions associated with resource use.

**Bounds:**  
`>= 0`

**Units:**  
[ktCO2-eq./GWh]

---

## storage_eff_in {STORAGE_TECH, LAYERS}, storage_eff_out {STORAGE_TECH, LAYERS}
**Description:**  
Efficiencies of input to and output from storage.

**Bounds:**  
`>= 0`, `<= 1`

**Units:**  
Dimensionless

---

## loss_coeff {END_USES_TYPES}
**Description:**  
Loss coefficients in networks (e.g., electricity grid, DHN).

**Bounds:**  
`>= 0`, default `0`

**Units:**  
Fractional loss

---

## peak_dhn_factor
**Description:**  
Factor associated with peak DHN conditions.

**Units:**  
Dimensionless

---

This completes the parameters section. Refer to **Variables** for decision variables and their roles in the model.