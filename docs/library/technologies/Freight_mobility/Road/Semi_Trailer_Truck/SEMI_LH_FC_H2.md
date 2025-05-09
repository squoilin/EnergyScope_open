---
title: Semi Hydrogen FC LH
---

# Semi Hydrogen FC LH

## Semi Trailer Truck - Long Haul Overview

The **Heavy-Duty Truck used for Long-Haul** journeys stands as a pillar
of the transport sector, specially configured to transport large volumes
of freight over relatively long distances. This category includes
tractor/semitrailer combinations with more than four tires, used for
operations over 320 km range.

### Semi Trailer Truck Short-Haul Performance Metrics

- **Operational Range:** Used with a maximum operational range of over
  320 km.
- **Annual Performance (*d~annual~*):** Boasting
  an annual performance capability of 274,000 km.
- **Load Capacity (*n~lpv~*):** With a substantial
  average load capacity of 11.68 tonnes per vehicle.
- **Average Speed:** Operating at an average speed of 95 km/h,
  optimizing delivery times for short-haul logistics [^1].
- **Capacity Factor:** A 35% capacity utilization factor is
  considered.
- **Reference Capacity:** The derived reference capacity of 1,043.81
  tonne-kilometers per hour (tkm/h).

The reference capacity is calculated as follows:

$$
ref_{capacity} = \dfrac{d_{annual} \cdot n_{lpv} \cdot average\\speed}{8760 \cdot 0.35}
$$

This calculation method accounts for the annual distance, average load
capacity, average speed, and the capacity utilization rate.

[^1]: “Fact \#671: April 18, 2011 Average Truck Speeds.” (2023,
October 23). Retrieved from
<https://www.energy.gov/eere/vehicles/fact-671-april-18-2011-average-truck-speeds>

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

## ES Model Integration

All the parameters concerning the Semi Hydrogen FC LH are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_LH_FC_H2'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_LH_FC_H2'))
```
