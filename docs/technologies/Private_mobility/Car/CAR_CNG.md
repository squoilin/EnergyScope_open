---
title: Car CNG
---

# Car CNG

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

## CNG

Natural gas can be used in modified internal combustion engines.
Compressed natural gas does, however, require more storage space than
gasoline and diesel, since it is a gas rather than a liquid. A tank to
store natural gas generally requires extra space in the trunk of the car
or on the bed of the van. This space issue can, however, be resolved
during construction, by installing the tank under the bodywork.

Compressed Natural Gas (CNG), primarily methane stored at high pressure,
has an LHV of 35.8 \[MJ/m3\] and a density of 0.777 \[kg/m3\].

## ES Model Parameters

All the parameters concerning the Car CNG are listed in the table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='CAR_CNG'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='CAR_CNG'))
```
