---
title: Coach Gasoline
---

# Coach Gasoline

## Intercity Coach Bus Description

The **Intercity Coach Bus** is designed for high-capacity, long-distance
passenger transportation, providing a crucial link between cities with a
focus on comfort and efficiency.

### Intercity Coach Bus Performance Metrics

- **Capacity:** It is equipped to carry 15 or more passengers.
- **Annual Distance (d~annual~):** The coach
  operates over an impressive annual distance of 140,000 km.
- **Average Occupancy Rate (*n*~*l**p**v*~):** With an
  average occupancy of 40 passengers per vehicle.
- **Capacity Factor:** Assuming a 20% capacity utilization.
- **Reference Capacity:** Consequently, a reference capacity of
  3,196.35 passenger-kilometers per hour (pkm/h) is calculated.

The reference capacity is computed using the formula:

$$
ref_{size} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where c~p~ represents the capacity utilization percentage.
This calculation takes into account the annual distance covered, the
average number of passengers, and the capacity utilization factor to
provide a clear picture of the Intercity Coach Bus’s performance and
contribution to public transport infrastructure.

## Gasoline

An internal combustion engine (ICE) is a type of heat engine where fuel
combustion takes place inside a chamber. This causes an increase in
temperature and pressure. This pressure is then applied directly to
pistons, rotors or a nozzle, which converts the thermal energy of
combustion into mechanical energy to move the vehicle. However, this
combustion generates numerous substances with potential impacts on human
health and the environment, including : - Carbon dioxide (CO~2~): a GHG
contributing to climate change and ocean acidification. - Nitrogen
oxides (NOx): precursors to the formation of photochemical ozone (smog),
which promotes respiratory problems, and causes, among other things, the
acidification of terrestrial and aquatic environments and the
eutrophication of the marine environment. - Fine particles (PM):
potentially causing respiratory problems when inhaled. - Carbon monoxide
(CO): considered toxic to humans and animals.

All gasoline engines use spark plugs to ignite the air-fuel mixture.
Although these engines are commonly referred to as “gasoline engines”,
they can also run on propane, methanol, ethanol, natural gas or
hydrogen.

## ES Model Parameters

All the parameters concerning the Coach Gasoline are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='COACH_GASOLINE'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='COACH_GASOLINE'))
```
