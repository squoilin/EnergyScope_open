---
title: Car Ethanol E85
---

# Car Ethanol E85

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

## E85 Ethanol

Gasoline can be blended with up to 10% vol. ethanol (E10 fuel) with no
significant effect on fuel efficiency or vehicle power. Some vehicles
are specifically designed to run on a blend containing up to 85% ethanol
(E85 fuel). A percentage of gasoline is required to start the vehicle,
as pure ethanol is difficult to ignite in cold weather. E-85 fuel cannot
be used in regular gasoline engines. However, if required, regular
gasoline can be used in engines designed for E85 fuel. Currently, E85
fuel is used by organizations with large fleets and is available at a
few service stations. E85-powered vehicles are generally fitted with
larger tanks by manufacturers to compensate for the lower energy content
of this fuel. A similar distance is therefore covered between two
consecutive fill-ups with a vehicle fuelled with E85 and one fuelled
with regular gasoline.

## ES Model Parameters

All the parameters concerning the Car Ethanol E85 are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='CAR_ETOH_E85'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='CAR_ETOH_E85'))
```
