---
title: Semi Hydrogen FC SH
---

# Semi Hydrogen FC SH

## Semi Trailer Truck - Short Haul Overview

The **Heavy-Duty Truck used for Short-Haul** journeys stands as a pillar
of the transport sector, specially configured to transport large volumes
of freight over relatively short distances. This category includes
tractor/semitrailer combinations with more than four tires, used for
operations within a 320 km range.

### Semi Trailer Truck Short-Haul Performance Metrics

- **Operational Range:** Used with a maximum operational range of up
  to 320 km.
- **Annual Performance (*d~annual~*):** Boasting
  an annual performance capability of 105,000 km.
- **Load Capacity (*n~lpv~*):** With a substantial
  average load capacity of 5.76 tonnes per vehicle.
- **Average Speed:** Operating at an average speed of 80 km/h,
  optimizing delivery times for short-haul logistics.
- **Capacity Factor:** A 15% capacity utilization factor is
  considered.
- **Reference Capacity:** The derived reference capacity of 460.27
  tonne-kilometers per hour (tkm/h).

The reference capacity is calculated as follows:

$$
ref_{capacity} = \dfrac{d_{annual} \cdot n_{lpv} \cdot average\\speed}{8760 \cdot 0.15}
$$

This calculation method accounts for the annual distance, average load
capacity, average speed, and the capacity utilization rate.

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

All the parameters concerning the Semi Hydrogen FC SH are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_SH_FC_H2'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_SH_FC_H2'))
```
