---
title: Semi BioDiesel 20% SH
---

# Semi BioDiesel 20% SH

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

All the parameters concerning the Semi BioDiesel 20% SH are listed in
the table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_SH_BIODIESEL_B20'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_SH_BIODIESEL_B20'))
```
