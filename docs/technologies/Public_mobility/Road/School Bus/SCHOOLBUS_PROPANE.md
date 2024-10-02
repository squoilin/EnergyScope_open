---
title: School Bus Propane
---

# School Bus Propane

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

## ES Model Parameters

All the parameters concerning the School Bus Propane are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='SCHOOLBUS_PROPANE'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='SCHOOLBUS_PROPANE'))
```
