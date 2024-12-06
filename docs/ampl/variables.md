# Variables

## End_Uses {LAYERS, PERIODS}
**Description:**  
Total demand met for each type of end-use in each period.

**Domain:**  
`LAYERS x PERIODS`

**Bounds:**  
`>= 0`

**Units:**  
[GW] (or corresponding unit to layers_in_out)

---

## Number_Of_Units {TECHNOLOGIES}
**Description:**  
Number of discrete units installed for each technology.

**Type:**  
Integer variable

**Bounds:**  
`>= 0`

**Units:**  
Dimensionless (count of units)

---

## F_Mult {TECHNOLOGIES}
**Description:**  
Installed capacity factor relative to reference size.

**Bounds:**  
`>= 0`

**Units:**  
Dimensionless multiplier (size factor)

---

## F_Mult_t {RESOURCES union TECHNOLOGIES, PERIODS}
**Description:**  
Operational factor in each period, scaled by capacity factor and reference size.

**Bounds:**  
`>= 0`

**Units:**  
Dimensionless multiplier

---

## C_inv {TECHNOLOGIES}
**Description:**  
Total investment cost for each technology.

**Bounds:**  
`>= 0`

**Units:**  
[MCHF]

---

## C_maint {TECHNOLOGIES}
**Description:**  
Total O&M cost for each technology (excluding resource costs).

**Bounds:**  
`>= 0`

**Units:**  
[MCHF/year]

---

## C_op {RESOURCES}
**Description:**  
Total operational (resource) cost for each resource.

**Bounds:**  
`>= 0`

**Units:**  
[MCHF/year]

---

## Storage_In {i in STORAGE_TECH, LAYERS, PERIODS}
**Description:**  
Power input to storage in a given period.

**Bounds:**  
`>= 0`

**Units:**  
[GW]

---

## Storage_Out {i in STORAGE_TECH, LAYERS, PERIODS}
**Description:**  
Power output from storage in a given period.

**Bounds:**  
`>= 0`

**Units:**  
[GW]

---

## Share_Mobility_Public
**Description:**  
Share of public mobility out of total mobility.

**Bounds:**  
`>= share_mobility_public_min`, `<= share_mobility_public_max`

**Units:**  
Fraction

---

## Share_Freight_Train
**Description:**  
Share of freight mobility by train.

**Bounds:**  
`>= share_freight_train_min`, `<= share_freight_train_max`

**Units:**  
Fraction

---

## Share_Heat_Dhn
**Description:**  
Share of low-temperature heating demand from DHN.

**Bounds:**  
`>= share_heat_dhn_min`, `<= share_heat_dhn_max`

**Units:**  
Fraction

---

## Y_Solar_Backup {TECHNOLOGIES}
**Description:**  
Binary variable indicating the technology chosen as backup for solar.

**Type:**  
Binary

**Units:**  
Dimensionless (0 or 1)

---

## Losses {END_USES_TYPES, PERIODS}
**Description:**  
Losses in the network for specific end-uses and periods.

**Bounds:**  
`>= 0`

**Units:**  
[GW] or analogous

---

## GWP_constr {TECHNOLOGIES}
**Description:**  
Total emissions associated with constructed technologies.

**Bounds:**  
`>= 0`

**Units:**  
[ktCO2-eq.]

---

## GWP_op {RESOURCES}
**Description:**  
Total yearly emissions of resources.

**Bounds:**  
`>= 0`

**Units:**  
[ktCO2-eq./year]

---

## TotalGWP
**Description:**  
Total global warming potential emissions in the system.

**Bounds:**  
`>= 0`

**Units:**  
[ktCO2-eq./year]

---

## TotalCost
**Description:**  
Total cost in the system (including investment, O&M, resource costs).

**Bounds:**  
`>= 0`

**Units:**  
[MCHF/year or analogous]

---

This completes the variables section. Refer back to **Sets** and **Parameters** for foundational context and inputs.