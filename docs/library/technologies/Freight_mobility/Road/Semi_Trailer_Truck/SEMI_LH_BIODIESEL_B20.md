---
title: Semi BioDiesel 20% LH
---

# Semi BioDiesel 20% LH

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

## ES Model Integration

All the parameters concerning the Semi BioDiesel 20% LH are listed in
the table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_LH_BIODIESEL_B20'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_LH_BIODIESEL_B20'))
```
