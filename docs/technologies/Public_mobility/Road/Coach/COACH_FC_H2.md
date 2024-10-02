---
title: Coach Hydrogen FC
---

# Coach Hydrogen FC

## Intercity Coach Bus Description

The **Intercity Coach Bus** is designed for high-capacity, long-distance
passenger transportation, providing a crucial link between cities with a
focus on comfort and efficiency.

### Intercity Coach Bus Performance Metrics

- **Capacity:** It is equipped to carry 15 or more passengers.
- **Annual Distance (d~annual~):** The coach
  operates over an impressive annual distance of 140,000 km.
- **Average Occupancy Rate (*n*~*l**p**v*~):** With an
  average occupancy of 40 passengers per vehicle.
- **Capacity Factor:** Assuming a 20% capacity utilization.
- **Reference Capacity:** Consequently, a reference capacity of
  3,196.35 passenger-kilometers per hour (pkm/h) is calculated.

The reference capacity is computed using the formula:

$$
ref_{size} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where c~p~ represents the capacity utilization percentage.
This calculation takes into account the annual distance covered, the
average number of passengers, and the capacity utilization factor to
provide a clear picture of the Intercity Coach Bus’s performance and
contribution to public transport infrastructure.

## Hydrogen Fuel Cell

A hydrogen fuel cell operates by combining hydrogen and oxygen atoms to
form water, releasing energy in the process. This energy can be
converted into electricity and heat. One type of hydrogen fuel cell,
known as a Proton Exchange Membrane (PEM) cell, uses a solid polymer
membrane that allows protons to pass through, while blocking electrons.
The membrane is coated with catalysts to accelerate the reaction.
Hydrogen molecules are fed to the anode, where they dissociate into
protons and electrons. The protons pass through the membrane to the
cathode, while the electrons circulate in an external circuit,
generating a voltage. At the cathode, oxygen molecules react with
protons and electrons to form water vapor, which is released from the
fuel cell. Overall, the operation of a hydrogen fuel cell relies on the
chemical affinity between hydrogen and oxygen, with the PEM cells being
one specific type of fuel cell.

## ES Model Parameters

All the parameters concerning the Hydrogen Fuel Cell Coach are listed in
the table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='COACH_FC_H2'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='COACH_FC_H2'))
```
