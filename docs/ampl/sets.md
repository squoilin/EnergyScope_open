# Sets

## PERIODS
**Description:**  
Time periods over which the model is solved.

**Type:**  
Main input set.

**Usage:**  
Defines temporal resolution for parameters (e.g., `t_op`) and variables (e.g., `F_Mult_t`).

---

## SECTORS
**Description:**  
Sectors of the energy system (e.g., residential, commercial, industrial).

**Type:**  
Main input set.

**Usage:**  
Used for disaggregating end-use demands (`end_uses_demand_year`).

---

## END_USES_INPUT
**Description:**  
Types of end-use demand that are input to the model (e.g., lighting, heating, mobility).

**Type:**  
Main input set.

**Usage:**  
Combined with `SECTORS` to define `end_uses_demand_year` and subsequently `end_uses_input`.

---

## END_USES_CATEGORIES
**Description:**  
Categories of end-uses (e.g., electricity, heat, mobility).

**Type:**  
Main input set.

**Usage:**  
Used to group and classify end-use demand types.

---

## END_USES_TYPES_OF_CATEGORY {END_USES_CATEGORIES}
**Description:**  
For each end-use category, defines the specific end-use types belonging to it.

**Type:**  
Main input mapping.

**Usage:**  
Supports construction of `END_USES_TYPES`.

---

## RESOURCES
**Description:**  
Available energy resources (e.g., fuels like wood and fossils, electricity imports).

**Type:**  
Main input set.

**Usage:**  
Used to define resource availability, costs, and emission factors.

---

## BIOFUELS within RESOURCES
**Description:**  
Subset of `RESOURCES` representing imported biofuels.

**Type:**  
Subset of RESOURCES.

**Usage:**  
Used to differentiate between resource types and to build `LAYERS`.

---

## EXPORT within RESOURCES
**Description:**  
Subset of `RESOURCES` representing exported resources.

**Type:**  
Subset of RESOURCES.

**Usage:**  
Identifies resources that leave the system boundary.

---

## END_USES_TYPES
**Description:**  
Secondary set of all end-use types, constructed from `END_USES_CATEGORIES` and `END_USES_TYPES_OF_CATEGORY`.

**Definition:**  
`END_USES_TYPES := setof {i in END_USES_CATEGORIES, j in END_USES_TYPES_OF_CATEGORY[i]} j;`

**Usage:**  
Used for balancing and meeting demand.

---

## TECHNOLOGIES_OF_END_USES_TYPE {END_USES_TYPES}
**Description:**  
For each end-use type, defines the set of technologies that convert resources into that end-use.

**Type:**  
Main input mapping.

**Usage:**  
Defines the conversion layer in the model.

---

## STORAGE_TECH
**Description:**  
Set of storage technologies.

**Type:**  
Main input set.

**Usage:**  
Used to store and release energy, subject to efficiencies and capacity limits.

---

## INFRASTRUCTURE
**Description:**  
Infrastructure components (e.g., DHN, grids, intermediate conversion tech).

**Type:**  
Main input set.

**Usage:**  
Represents networks and infrastructure elements for distribution and conversion.

---

## LAYERS
**Description:**  
Secondary set representing layers of energy flows.  
`LAYERS := (RESOURCES diff BIOFUELS diff EXPORT) union END_USES_TYPES;`

**Usage:**  
Used to balance resources and products in the system.

---

## TECHNOLOGIES
**Description:**  
All technologies considered in the model, including end-use technologies, storage, and infrastructure.  
`TECHNOLOGIES := (setof {i in END_USES_TYPES, j in TECHNOLOGIES_OF_END_USES_TYPE[i]} j) union STORAGE_TECH union INFRASTRUCTURE;`

**Usage:**  
Central set for technology-related parameters and decision variables.

---

## TECHNOLOGIES_OF_END_USES_CATEGORY {i in END_USES_CATEGORIES} within TECHNOLOGIES
**Description:**  
Subset of `TECHNOLOGIES` by end-use category.

**Definition:**  
`TECHNOLOGIES_OF_END_USES_CATEGORY[i] := setof {j in END_USES_TYPES_OF_CATEGORY[i], k in TECHNOLOGIES_OF_END_USES_TYPE[j]} k;`

---

## COGEN within TECHNOLOGIES
**Description:**  
Set of cogeneration technologies.

---

## BOILERS within TECHNOLOGIES
**Description:**  
Set of boiler technologies.

---

This completes the sets section. Refer to **Parameters** and **Variables** for details on model inputs and decision variables.