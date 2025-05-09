---
title: Car Electric
---

# Car Electric

## Car Definition

The **Car** category is defined as a vehicle featuring four wheels and
two axles, with a primary function of transporting passengers within
private transportation settings.

### Car Performance and Usage Metrics[^1]

The performance and usage metrics for cars are as follows:

- **Annual Distance (*d~annual~*):** Cars on
  average cover a distance of 14,602 km per year.
- **Average Occupancy Rate (*n~lpv~*):** The average
  occupancy rate for cars is determined to be 1.57 passengers per
  vehicle.
- **Utilization Factor:** The utilization factor for cars is
  established at 5%, correlating to an average daily use of 1 hour and
  15 minutes.
- **Reference Capacity:** This leads to a reference capacity of 52.34
  passenger-kilometers per hour (pkm/h), calculated using the formula:

$$
ref_{size} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where *c*~*p*~ denotes the capacity utilization percentage.

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

All the parameters concerning the Car Electric are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='CAR_EV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='CAR_EV'))
```
