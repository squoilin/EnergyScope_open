---
title: Coach Electric
---

# Coach Electric

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

All the parameters concerning the Coach Electric are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='COACH_EV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='COACH_EV'))
```
