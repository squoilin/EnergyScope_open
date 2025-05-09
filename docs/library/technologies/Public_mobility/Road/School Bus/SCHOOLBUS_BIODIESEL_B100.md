---
title: School Bus BioDiesel
---

# School Bus BioDiesel

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

## B100 Biodiesel

B100 Biodiesel fuel is a diesel alternative derived entirely from
biomass. It runs on 100% biodiesel, contributing to carbon emissions
reductions in comparison to fossil fuels. Only blends of biodiesel and
petroleum diesel containing 7% vol. or less of biodiesel can be used in
diesel engines without modification. Pure biodiesel (B100) requires
engine modifications to avoid maintenance and performance problems.

### Model Remarks:

The model treats vehicles that use biodiesel and those that use
traditional diesel as equivalent in technical aspects. It is worth
noting that in the current version of QC EnergyScope, biodiesel is
treated the same as diesel and will require modification in a future
version.

## ES Model Parameters

All the parameters concerning the School Bus BioDiesel are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='SCHOOLBUS_BIODIESEL_B100'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='SCHOOLBUS_BIODIESEL_B100'))
```
