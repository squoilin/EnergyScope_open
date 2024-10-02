---
title: Semi Hybrid Diesel SH
---

# Semi Hybrid Diesel SH

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

## Hybrid Diesel

A hybrid vehicle integrates an internal combustion engine with an
electric motor. Unlike plug-in hybrids, this type of vehicle relies on a
battery and an electric motor to capture kinetic energy during vehicle
operation.

The hybrid vehicle features a lithium battery that is smaller compared
to those found in fully electric vehicles, aimed at decreasing fuel
consumption. However, the increased weight of hybrid vehicles may lead
to higher fuel use.

## ES Model Integration

All the parameters concerning the Semi Hybrid Diesel SH are listed in
the table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_SH_HY_DIESEL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_SH_HY_DIESEL'))
```
