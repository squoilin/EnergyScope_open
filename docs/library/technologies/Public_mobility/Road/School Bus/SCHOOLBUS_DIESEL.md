---
title: School Bus Diesel
---

# School Bus Diesel

## School Bus Overview

The **School Bus** is engineered to transport 15 or more passengers,
serving primarily in the conveyance of students to and from educational
institutions.

### School Bus Performance Metrics

- **Annual Distance (d~annual~):** The school
  bus covers an annual distance of 24,000 km.
- **Average Occupancy Rate (*n*~*l**p**v*~):** It boasts an
  average loading capacity accommodating 47 passengers per vehicle.
- **Utilization Window:** The vehicle is utilized for 5.26 hours per
  day, translating to a 22% capacity utilization, according to the
  study by Duran and Walkowicz[^1].
- **Reference Capacity:** The reference capacity, derived from these
  parameters, is calculated to be 585.31 passenger-kilometers per hour
  (pkm/h), utilizing the formula:

$$
ref_{size} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where c~p~ represents the capacity utilization percentage.
Where the denominator reflects the total hours in a year multiplied by
the capacity utilization factor.

[^1]: Adam Duran and Kevin Walkowicz, “A Statistical
Characterization of School Bus Drive Cycles Collected via Onboard
Logging Systems,” SAE International Journal of Commercial Vehicles
6, no. 2 (September 24, 2013): 400-406,
<https://doi.org/10.4271/2013-01-2400>.

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

All the parameters concerning the School Bus Diesel are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SCHOOLBUS_DIESEL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SCHOOLBUS_DIESEL'))
```
