---
title: Truck Electric LH
---

# Truck Electric LH

## Medium-Duty Truck - Long Haul Overview

The **Medium-Duty Truck - Long Haul** category includes single-unit
vehicles with more than four tires, designed for substantial range
capabilities exceeding 320 km. These trucks play a pivotal role in
nationwide logistics, capable of handling significant cargo loads over
long distances.

### Medium-Duty Truck Performance Metrics

- **Operational Range:** Designed for long-haul operations, these
  trucks have a range of over 320 km.
- **Annual Mileage (*d~annual~*):** They record
  an annual mileage of 37,000 km, demonstrating their reliability and
  endurance in logistics operations.
- **Average Load (*n~lpv~*):** With an average load
  capacity of 3.27 tonnes per vehicle, they are integral to the
  transportation of substantial goods across the country.
- **Capacity Factor:** Based on a 10% capacity utilization factor, as
  cited by Schnidrig[^1], this reflects the operational efficiency
  considering loading times and route distances.
- **Reference Capacity:** The calculated reference capacity of 138.12
  tonne-kilometers per hour (tkm/h) underscores their strategic
  importance in logistics and distribution networks.

The reference capacity is computed utilizing the formula:

$$
ref_{capacity} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where c~p~ represents the capacity utilization percentage.
This calculation takes into account the annual mileage, average load
capacity, and the capacity utilization factor, highlighting the
efficiency and utility of Medium-Duty Trucks in long-haul logistics.

[^1]:  Jonas Schnidrig, “Assessment of Green Mobility Scenarios on European Energy Systems” (EPFL, 2020).

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

## ES Model Integration

All the parameters concerning the Truck Electric LH are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_LH_EV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_LH_EV'))
```

Schnidrig, Jonas. 2020. “Assessment of Green Mobility Scenarios on
European Energy Systems.” PhD thesis, EPFL.
