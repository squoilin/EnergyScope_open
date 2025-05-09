---
title: Coach Hybrid Diesel
---

# Hybrid Diesel Coach

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

## Hybrid Diesel

A hybrid vehicle integrates an internal combustion engine with an
electric motor. Unlike plug-in hybrids, this type of vehicle relies on a
battery and an electric motor to capture kinetic energy during vehicle
operation.

The hybrid vehicle features a lithium battery that is smaller compared
to those found in fully electric vehicles, aimed at decreasing fuel
consumption. However, the increased weight of hybrid vehicles may lead
to higher fuel use.

## ES Model Parameters

All the parameters concerning the Hybrid Diesel Coach are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='COACH_HY_DIESEL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='COACH_HY_DIESEL'))
```
