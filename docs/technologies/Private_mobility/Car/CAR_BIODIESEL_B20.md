---
title: Car BioDiesel 20%
---

# Car BioDiesel 20%

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

All the parameters concerning the Car BioDiesel 20% are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='CAR_BIODIESEL_B20'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='CAR_BIODIESEL_B20'))
```
