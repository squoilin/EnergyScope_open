# Variables

## C_inv
**Description:**  
Total investment cost for each technology.

**Definition:**  
`C_inv {TECHNOLOGIES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[MCHF]

**Usage:**  
Represents the capital expenditure for deploying technologies.

---

## C_maint
**Description:**  
Total O&M cost for each technology (excluding resource costs).

**Definition:**  
`C_maint {TECHNOLOGIES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[MCHF/year]

**Usage:**  
Captures the ongoing maintenance and operational expenses for technologies.

---

## C_op
**Description:**  
Total operational (resource) cost for each resource.

**Definition:**  
`C_op {RESOURCES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[MCHF/year]

**Usage:**  
Aggregates the operational costs associated with resource usage.

---

## End_Uses
**Description:**  
Total demand met for each type of end-use in each period.

**Definition:**  
`End_Uses {LAYERS, PERIODS} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[GW] (or corresponding unit to layers_in_out)

**Usage:**  
Represents the actual energy consumed by end-uses in each period.

---

## F_Mult
**Description:**  
Installed capacity factor relative to reference size.

**Definition:**  
`F_Mult {TECHNOLOGIES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
Dimensionless multiplier (size factor)

**Usage:**  
Scales the reference size to determine actual installed capacities.

---

## F_Mult_t
**Description:**  
Operational factor in each period, scaled by capacity factor and reference size.

**Definition:**  
`F_Mult_t {RESOURCES union TECHNOLOGIES, PERIODS} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
Dimensionless multiplier

**Usage:**  
Determines the operational level of resources and technologies in each period.

---

## GWP_constr
**Description:**  
Total emissions associated with constructed technologies.

**Definition:**  
`GWP_constr {TECHNOLOGIES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[ktCO2-eq.]

**Usage:**  
Calculates the emissions resulting from the construction of technologies.

---

## GWP_op
**Description:**  
Total yearly emissions of resources.

**Definition:**  
`GWP_op {RESOURCES} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[ktCO2-eq./year]

**Usage:**  
Aggregates emissions from resource utilization annually.

---

## Losses
**Description:**  
Losses in the network for specific end-uses and periods.

**Definition:**  
`Losses {END_USES_TYPES, PERIODS} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[GW] or analogous

**Usage:**  
Models energy losses within end-use networks over time.

---

## Number_Of_Units
**Description:**  
Number of discrete units installed for each technology.

**Definition:**  
`Number_Of_Units {TECHNOLOGIES} integer;`

**Type:**  
Integer variable

**Bounds:**  
`>= 0`

**Units:**  
Dimensionless (count of units)

**Usage:**  
Represents the count of installed technology units based on reference size.

---

## Share_Freight_Train
**Description:**  
Share of freight mobility by train.

**Definition:**  
`Share_Freight_Train >= share_freight_train_min, <= share_freight_train_max;`

**Bounds:**  
`>= share_freight_train_min`, `<= share_freight_train_max`

**Units:**  
Fraction

**Usage:**  
Determines the proportion of freight transport handled by trains.

---

## Share_Heat_Dhn
**Description:**  
Share of low-temperature heating demand from DHN.

**Definition:**  
`Share_Heat_Dhn >= share_heat_dhn_min, <= share_heat_dhn_max;`

**Bounds:**  
`>= share_heat_dhn_min`, `<= share_heat_dhn_max`

**Units:**  
Fraction

**Usage:**  
Allocates the portion of low-temperature heating to District Heating Networks.

---

## Share_Mobility_Public
**Description:**  
Share of public mobility out of total mobility.

**Definition:**  
`Share_Mobility_Public >= share_mobility_public_min, <= share_mobility_public_max;`

**Bounds:**  
`>= share_mobility_public_min`, `<= share_mobility_public_max`

**Units:**  
Fraction

**Usage:**  
Determines the allocation of mobility demand to public transportation.

---

## Storage_In
**Description:**  
Power input to storage in a given period.

**Definition:**  
`Storage_In {STORAGE_TECH, LAYERS, PERIODS} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[GW]

**Usage:**  
Models the energy input into storage technologies over time.

---

## Storage_Out
**Description:**  
Power output from storage in a given period.

**Definition:**  
`Storage_Out {STORAGE_TECH, LAYERS, PERIODS} >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[GW]

**Usage:**  
Models the energy output from storage technologies over time.

---

## TotalCost
**Description:**  
Total cost in the system (including investment, O&M, resource costs).

**Definition:**  
`TotalCost >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[MCHF/year or analogous]

**Usage:**  
Aggregates all costs incurred within the system annually.

---

## TotalGWP
**Description:**  
Total Global Warming Potential (GWP) emissions in the system.

**Definition:**  
`TotalGWP >= 0;`

**Bounds:**  
`>= 0`

**Units:**  
[ktCO2-eq./year]

**Usage:**  
Aggregates all emissions contributing to global warming potential annually.

---

## Y_Solar_Backup
**Description:**  
Binary variable indicating the technology chosen as backup for solar.

**Definition:**  
`Y_Solar_Backup {TECHNOLOGIES} binary;`

**Type:**  
Binary

**Units:**  
Dimensionless (0 or 1)

**Usage:**  
Identifies which decentralized technology serves as a backup for solar energy.

---
