---
title: Bus BioDiesel
---

# Bus BioDiesel

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

## B100 Biodiesel

B100 Biodiesel fuel is a diesel alternative derived entirely from
biomass. It runs on 100% biodiesel, contributing to carbon emissions
reductions in comparison to fossil fuels. Only blends of biodiesel and
petroleum diesel containing 7% vol. or less of biodiesel can be used in
diesel engines without modification. Pure biodiesel (B100) requires
engine modifications to avoid maintenance and performance problems.

### Model Remarks:

The model treats vehicles that use biodiesel and those that use
traditional diesel as equivalent in technical aspects. It is worth
noting that in the current version of QC EnergyScope, biodiesel is
treated the same as diesel and will require modification in a future
version.

## ES Model Parameters

All the parameters concerning the Bus BioDiesel are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='BUS_BIODIESEL_B100'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='BUS_BIODIESEL_B100'))
```
