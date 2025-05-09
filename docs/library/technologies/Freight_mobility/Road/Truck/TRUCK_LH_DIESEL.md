---
title: Truck Diesel LH
---

# Truck Diesel LH

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

All the parameters concerning the Truck Diesel LH are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_LH_DIESEL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_LH_DIESEL'))
```

Moret, Stefano. 2017. “Strategic Energy Planning Under Uncertainty.” PhD
thesis, Lausanne, Switzerland: Ecole Polytechnique Fédérale de Lausanne.

Schnidrig, Jonas. 2020. “Assessment of Green Mobility Scenarios on
European Energy Systems.” PhD thesis, EPFL.
