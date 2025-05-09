---
title: Truck Diesel SH
---

# Truck Diesel SH

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

## Diesel

An internal combustion engine (ICE) is a type of heat engine where fuel
combustion takes place inside a chamber. This causes an increase in
temperature and pressure. This pressure is then applied directly to
pistons, rotors or a nozzle, which converts the thermal energy of
combustion into mechanical energy to move the vehicle. However, this
combustion generates numerous substances with potential impacts on human
health and the environment, including :

- Carbon Dioxide (CO2): a GHG contributing to climate change and ocean
  acidification.

- Nitrogen Oxides (NOx): precursors to the formation of photochemical
  ozone (smog), which promotes respiratory problems, and causes, among
  other things, the acidification of terrestrial and aquatic
  environments and the eutrophication of the marine environment.

- Particle Matter (PM): potentially causing respiratory problems when
  inhaled.

- Carbon Monoxide (CO): considered toxic to humans and animals.

Diesel engines, which also run on biodiesel and synthetic fuels, do not
require spark plugs but rely on fuel vapour compression to trigger
combustion.

Diesel fuel has an LHV of 11.83 \[kWh/kg\], making it a common choice
for heavy-duty transportation due to its high energy density and
efficiency.

## ES Model Integration

All the parameters concerning the Truck Diesel SH are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_SH_DIESEL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_SH_DIESEL'))
```
