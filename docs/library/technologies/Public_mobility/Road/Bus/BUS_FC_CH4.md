---
title: Bus Methane FC
---

# Bus Methane FC

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

## Methane Fuel Cell

Methane fuel cell vehicles leverage the chemical energy of methane, CH4,
to generate electricity through a fuel cell. These vehicles operate on
the principle of converting methane directly into electrical energy,
which then powers the vehicle’s electric motor.

## ES Model Parameters

All the parameters concerning the Bus Methane FC are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='BUS_FC_CH4'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='BUS_FC_CH4'))
```
