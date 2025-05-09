---
title: SUV Hydrogen FC
---

# SUV Hydrogen FC

## SUV Class Definition

The **Sport Utility Vehicle (SUV) class** is a versatile category
encompassing four-wheeled, two-axle vehicles, originally designed for
cargo transportation but now primarily used for passenger mobility.

### SUV Technology Model

The SUV technology model encompasses light trucks, including:

- Pickup trucks
- Sport utility vehicles (SUVs)
- Minivans
- Vans
- Special purpose vehicles

These are modeled within the context of passenger transportation.

### Performance Metrics[^1]

The SUV class is characterized by specific annual performance metrics
and usage parameters:

- **Annual Distance (*d~annual~*):** The average
  distance covered annually by an SUV is 16,462 km.
- **Average Occupancy Rate (*n~lpv~*):** The mean
  number of passengers per vehicle is calculated to be 1.7.
- **Utilization Factor:** Set at 5%, this reflects an average daily
  use of 1 hour and 15 minutes per day.
- **Reference Capacity:** Calculated at 63.89 passenger-kilometers per
  hour (pkm/h), this metric is derived from the formula:

$$
ref_{size} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where *c*~*p*~ represents the capacity utilization percentage.

[^1]: «Canadian Vehicle Survey — 2009 Summary Report» (Ottawa, Canada:
Natural Resources Canada, 2009).

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

All the parameters concerning the SUV Hydrogen FC are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SUV_FC_H2'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SUV_FC_H2'))
```
