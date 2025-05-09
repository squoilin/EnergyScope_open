---
title: Car Diesel
---

# Car Diesel

## Car Definition

The **Car** category is defined as a vehicle featuring four wheels and
two axles, with a primary function of transporting passengers within
private transportation settings.

### Car Performance and Usage Metrics[^1]

The performance and usage metrics for cars are as follows:

- **Annual Distance (*d~annual~*):** Cars on
  average cover a distance of 14,602 km per year.
- **Average Occupancy Rate (*n~lpv~*):** The average
  occupancy rate for cars is determined to be 1.57 passengers per
  vehicle.
- **Utilization Factor:** The utilization factor for cars is
  established at 5%, correlating to an average daily use of 1 hour and
  15 minutes.
- **Reference Capacity:** This leads to a reference capacity of 52.34
  passenger-kilometers per hour (pkm/h), calculated using the formula:

$$
ref_{size} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where *c*~*p*~ denotes the capacity utilization percentage.

[^1]: «Canadian Vehicle Survey — 2009 Summary Report» (Ottawa, Canada:
Natural Resources Canada, 2009).

## Diesel

An internal combustion engine (ICE) is a type of heat engine where fuel
combustion takes place inside a chamber. This causes an increase in
temperature and pressure. This pressure is then applied directly to
pistons, rotors or a nozzle, which converts the thermal energy of
combustion into mechanical energy to move the vehicle. However, this
combustion generates numerous substances with potential impacts on human
health and the environment, including :

- Carbon Dioxide (CO~2~): a GHG contributing to climate change and ocean
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

## ES Model Parameters

All the parameters concerning the Car Diesel are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='CAR_DIESEL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='CAR_DIESEL'))
```
