---
title: Semi Diesel LH
---

# Semi Diesel LH

## Semi Trailer Truck - Long Haul Overview

The **Heavy-Duty Truck used for Long-Haul** journeys stands as a pillar
of the transport sector, specially configured to transport large volumes
of freight over relatively long distances. This category includes
tractor/semitrailer combinations with more than four tires, used for
operations over 320 km range.

### Semi Trailer Truck Short-Haul Performance Metrics

- **Operational Range:** Used with a maximum operational range of over
  320 km.
- **Annual Performance (*d~annual~*):** Boasting
  an annual performance capability of 274,000 km.
- **Load Capacity (*n~lpv~*):** With a substantial
  average load capacity of 11.68 tonnes per vehicle.
- **Average Speed:** Operating at an average speed of 95 km/h,
  optimizing delivery times for short-haul logistics [^1].
- **Capacity Factor:** A 35% capacity utilization factor is
  considered.
- **Reference Capacity:** The derived reference capacity of 1,043.81
  tonne-kilometers per hour (tkm/h).

The reference capacity is calculated as follows:

$$
ref_{capacity} = \dfrac{d_{annual} \cdot n_{lpv} \cdot average\\speed}{8760 \cdot 0.35}
$$

This calculation method accounts for the annual distance, average load
capacity, average speed, and the capacity utilization rate.

[^1]: “Fact \#671: April 18, 2011 Average Truck Speeds.” (2023,
October 23). Retrieved from
<https://www.energy.gov/eere/vehicles/fact-671-april-18-2011-average-truck-speeds>

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

All the parameters concerning the Semi Diesel LH are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_LH_DIESEL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_LH_DIESEL'))
```
