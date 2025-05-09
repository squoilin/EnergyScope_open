---
title: School Bus Electric
---

# School Bus Electric

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

## Battery Electrical Vehicle

A 100% electric vehicle is powered solely by electricity. This
electricity is used to supply an inverter with direct current which,
using the principle of electromagnetism, converts electricity into
mechanical energy and moves the vehicle. As the vehicle is not connected
to the electrical grid while on the move, it is necessary to ensure its
power supply by other means. To do this, BEVs store electricity in an
on-board rechargeable battery.

Among the battery types presented, lithium batteries are the ones found
in electric vehicles currently on the market. Lithium batteries offer
the ability to store more electricity (i.e., have greater energy
density) in a smaller volume than traditional batteries, such as
lead-acid and nickel-metal-hydride batteries. Lithium batteries are also
lighter than conventional batteries.

## ES Model Parameters

All the parameters concerning the School Bus Electric are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='SCHOOLBUS_EV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='SCHOOLBUS_EV'))
```
