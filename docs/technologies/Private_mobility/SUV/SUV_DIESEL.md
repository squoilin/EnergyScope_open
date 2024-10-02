---
title: SUV Diesel
---

# SUV Diesel

## SUV Class Definition

The **Sport Utility Vehicle (SUV) class** is a versatile category
encompassing four-wheeled, two-axle vehicles, originally designed for
cargo transportation but now primarily used for passenger mobility.

### SUV Technology Model

The SUV technology model encompasses light trucks, including:

- Pickup trucks
- Sport utility vehicles (SUVs)
- Minivans
- Vans
- Special purpose vehicles

These are modeled within the context of passenger transportation.

### Performance Metrics[^1]

The SUV class is characterized by specific annual performance metrics
and usage parameters:

- **Annual Distance (*d~annual~*):** The average
  distance covered annually by an SUV is 16,462 km.
- **Average Occupancy Rate (*n~lpv~*):** The mean
  number of passengers per vehicle is calculated to be 1.7.
- **Utilization Factor:** Set at 5%, this reflects an average daily
  use of 1 hour and 15 minutes per day.
- **Reference Capacity:** Calculated at 63.89 passenger-kilometers per
  hour (pkm/h), this metric is derived from the formula:

$$
ref_{size} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where *c*~*p*~ represents the capacity utilization percentage.

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

All the parameters concerning the SUV Diesel are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='SUV_DIESEL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='SUV_DIESEL'))
```
