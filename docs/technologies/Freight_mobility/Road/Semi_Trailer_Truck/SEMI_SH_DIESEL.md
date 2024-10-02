---
title: Semi Diesel SH
---

# Semi Diesel SH

## Semi Trailer Truck - Short Haul Overview

The **Heavy-Duty Truck used for Short-Haul** journeys stands as a pillar
of the transport sector, specially configured to transport large volumes
of freight over relatively short distances. This category includes
tractor/semitrailer combinations with more than four tires, used for
operations within a 320 km range.

### Semi Trailer Truck Short-Haul Performance Metrics

- **Operational Range:** Used with a maximum operational range of up
  to 320 km.
- **Annual Performance (*d~annual~*):** Boasting
  an annual performance capability of 105,000 km.
- **Load Capacity (*n~lpv~*):** With a substantial
  average load capacity of 5.76 tonnes per vehicle.
- **Average Speed:** Operating at an average speed of 80 km/h,
  optimizing delivery times for short-haul logistics.
- **Capacity Factor:** A 15% capacity utilization factor is
  considered.
- **Reference Capacity:** The derived reference capacity of 460.27
  tonne-kilometers per hour (tkm/h).

The reference capacity is calculated as follows:

$$
ref_{capacity} = \dfrac{d_{annual} \cdot n_{lpv} \cdot average\\speed}{8760 \cdot 0.15}
$$

This calculation method accounts for the annual distance, average load
capacity, average speed, and the capacity utilization rate.

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

All the parameters concerning the Semi Diesel SH are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_SH_DIESEL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_SH_DIESEL'))
```
