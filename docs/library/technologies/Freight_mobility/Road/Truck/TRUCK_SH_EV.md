---
title: Truck Electric SH
---

# Truck Electric SH

## Medium-Duty Truck - Short Haul Overview

The **Medium-Duty Truck for Short-Haul** operations represents a class
of robust vehicles engineered for transporting substantial loads over
moderate distances. These trucks are single units with more than four
tires, designed with a maximum range of up to 320 km, making them ideal
for regional distribution tasks.

### Medium-Duty Truck Short-Haul Performance Metrics

- **Operational Range:** Capable of covering distances up to 320 km,
  tailored for short-haul logistics.
- **Annual Mileage (*d~annual~*):** The truck
  class maintains a yearly operational distance of 26,600 km.
- **Load Capacity (*n~lpv~*):** With an average load
  capacity of 0.98 tonnes per vehicle.
- **Capacity Factor:** A 10% capacity utilization factor is applied,
  as detailed by Schnidrig[^1].
- **Reference Capacity:** Achieving a reference capacity of 29.76
  tonne-kilometers per hour (tkm/h), these trucks are optimally
  configured for regional distribution networks.

The formula used to calculate the reference capacity is as follows:

$$
ref_{capacity} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot 0.10}
$$

This equation considers the annual distance covered, the average load
capacity, and the capacity utilization rate, emphasizing the trucks’
utility and efficiency in short-haul transportation tasks.

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

All the parameters concerning the Truck Electric SH are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_SH_EV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_SH_EV'))
```
