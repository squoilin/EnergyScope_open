---
title: Bus Hybrid Diesel
---

# Bus Hybrid Diesel

## Bus Technology Overview

The **Bus** technology category encompasses city buses designed
specifically for urban transportation.

### Bus Performance and Usage Metrics

The key performance and usage metrics for buses are outlined as follows:

- **Annual Distance (d~annual~):** City buses
  have an annual mileage of 56,000 km.
- **Average Occupancy Rate (*n*~*l**p**v*~):** The average
  occupancy rate is 14 passengers per vehicle, as reported by STM.
- **Utilization Factor:** The utilization factor is established at
  35%, resulting of an average speed of 18 (km/h) [^1].
- **Reference Capacity:** This yields a reference capacity of 63.89
  passenger-kilometers per hour (pkm/h), determined using the formula:

$$
ref_{size} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where c~p~ represents the capacity utilization percentage.

[^1]: The bus network and the schedules enlightened. (2023, October 24).
Retrieved from
<https://www.stm.info/en/info/networks/bus-network-and-schedules-enlightened>

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

All the parameters concerning the Bus Hybrid Diesel are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='BUS_HY_DIESEL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='BUS_HY_DIESEL'))
```
