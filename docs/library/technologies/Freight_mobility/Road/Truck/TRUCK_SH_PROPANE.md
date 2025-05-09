---
title: Truck Propane SH
---

# Truck Propane SH

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

## Propane

An internal combustion engine (ICE) is a type of heat engine where fuel
combustion takes place inside a chamber. This causes an increase in
temperature and pressure. This pressure is then applied directly to
pistons, rotors or a nozzle, which converts the thermal energy of
combustion into mechanical energy to move the vehicle. Propane-powered
vehicles operate like gasoline-powered ones. There are two types of
propane fuel injection system: vapor injection and liquid injection. In
both cases, propane is stored as a liquid in a tank at relatively low
pressure. Liquid injection technology enables more precise control of
fuel delivery, improving engine performance and efficiency.

## ES Model Integration

All the parameters concerning the Truck Propane SH are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_SH_PROPANE'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_SH_PROPANE'))
```
