---
title: Bus CNG
---

# Bus CNG

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

## CNG

Natural gas can be used in modified internal combustion engines.
Compressed natural gas does, however, require more storage space than
gasoline and diesel, since it is a gas rather than a liquid. A tank to
store natural gas generally requires extra space in the trunk of the car
or on the bed of the van. This space issue can, however, be resolved
during construction, by installing the tank under the bodywork.

Compressed Natural Gas (CNG), primarily methane stored at high pressure,
has an LHV of 35.8 \[MJ/m3\] and a density of 0.777 \[kg/m3\].

## ES Model Parameters

All the parameters concerning the Bus CNG are listed in the table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='BUS_CNG'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='BUS_CNG'))
```
