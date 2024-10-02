---
title: SUV Electric
---

# SUV Electric

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

## Battery Electrical Vehicle

A 100% electric vehicle is powered solely by electricity. This
electricity is used to supply an inverter with direct current which,
using the principle of electromagnetism, converts electricity into
mechanical energy and moves the vehicle. As the vehicle is not connected
to the electrical grid while on the move, it is necessary to ensure its
power supply by other means. To do this, BEVs store electricity in an
on-board rechargeable battery.

Among the battery types presented, lithium batteries are the ones found
in electric vehicles currently on the market. Lithium batteries offer
the ability to store more electricity (i.e., have greater energy
density) in a smaller volume than traditional batteries, such as
lead-acid and nickel-metal-hydride batteries. Lithium batteries are also
lighter than conventional batteries.

## ES Model Parameters

All the parameters concerning the SUV Electric are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SUV_EV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SUV_EV'))
```
