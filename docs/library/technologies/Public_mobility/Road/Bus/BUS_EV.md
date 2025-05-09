---
title: Bus Electric
---

# Bus Electric

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

## Battery Electrical Vehicle

A 100% electric vehicle is powered solely by electricity. This
electricity is used to supply an inverter with direct current which,
using the principle of electromagnetism, converts electricity into
mechanical energy and moves the vehicle. As the vehicle is not connected
to the electrical grid while on the move, it is necessary to ensure its
power supply by other means. To do this, BEVs store electricity in an
on-board rechargeable battery.

Among the battery types presented, lithium batteries are the ones found
in electric vehicles currently on the market. Lithium batteries offer
the ability to store more electricity (i.e., have greater energy
density) in a smaller volume than traditional batteries, such as
lead-acid and nickel-metal-hydride batteries. Lithium batteries are also
lighter than conventional batteries.

## ES Model Parameters

All the parameters concerning the Bus Electric are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='BUS_EV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='BUS_EV'))
```
