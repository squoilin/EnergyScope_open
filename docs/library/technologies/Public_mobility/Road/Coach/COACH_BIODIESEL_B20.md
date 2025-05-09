---
title: Coach BioDiesel 20%
---

# Coach BioDiesel 20%

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

## B20 Biodiesel

B20 Biodiesel is a blend that includes 20% biodiesel with 80% petroleum
diesel. It offers a balance between the environmental benefits of
biodiesel and the cost of traditional diesel. This blend aids in
decreasing greenhouse gas emissions while utilizing existing diesel
infrastructure. Only blends of biodiesel and petroleum diesel containing
7% vol. or less of biodiesel can be used in diesel engines without
modification. Pure biodiesel (B100) requires engine modifications to
avoid maintenance and performance problems.

### Model Remarks:

The model treats vehicles that use biodiesel and those that use
traditional diesel as equivalent in technical aspects. It is worth
noting that in the current version of QC EnergyScope, biodiesel is
treated the same as diesel and will require modification in a future
version.

## ES Model Parameters

All the parameters concerning the Coach BioDiesel 20% are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='COACH_BIODIESEL_B20'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='COACH_BIODIESEL_B20'))
```
