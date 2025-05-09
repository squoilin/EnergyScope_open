---
title: Truck CNG LH
---

# Truck CNG LH

## Medium-Duty Truck - Long Haul Overview

The **Medium-Duty Truck - Long Haul** category includes single-unit
vehicles with more than four tires, designed for substantial range
capabilities exceeding 320 km. These trucks play a pivotal role in
nationwide logistics, capable of handling significant cargo loads over
long distances.

### Medium-Duty Truck Performance Metrics

- **Operational Range:** Designed for long-haul operations, these
  trucks have a range of over 320 km.
- **Annual Mileage (*d~annual~*):** They record
  an annual mileage of 37,000 km, demonstrating their reliability and
  endurance in logistics operations.
- **Average Load (*n~lpv~*):** With an average load
  capacity of 3.27 tonnes per vehicle, they are integral to the
  transportation of substantial goods across the country.
- **Capacity Factor:** Based on a 10% capacity utilization factor, as
  cited by Schnidrig[^1], this reflects the operational efficiency
  considering loading times and route distances.
- **Reference Capacity:** The calculated reference capacity of 138.12
  tonne-kilometers per hour (tkm/h) underscores their strategic
  importance in logistics and distribution networks.

The reference capacity is computed utilizing the formula:

$$
ref_{capacity} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where c~p~ represents the capacity utilization percentage.
This calculation takes into account the annual mileage, average load
capacity, and the capacity utilization factor, highlighting the
efficiency and utility of Medium-Duty Trucks in long-haul logistics.

[^1]:  Jonas Schnidrig, “Assessment of Green Mobility Scenarios on European Energy Systems” (EPFL, 2020).

## CNG

Natural gas can be used in modified internal combustion engines.
Compressed natural gas does, however, require more storage space than
gasoline and diesel, since it is a gas rather than a liquid. A tank to
store natural gas generally requires extra space in the trunk of the car
or on the bed of the van. This space issue can, however, be resolved
during construction, by installing the tank under the bodywork.

Compressed Natural Gas (CNG), primarily methane stored at high pressure,
has an LHV of 35.8 \[MJ/m3\] and a density of 0.777 \[kg/m3\].

## ES Model Integration

All the parameters concerning the Truck CNG LH are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_LH_CNG'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='TRUCK_LH_CNG'))
```

Moret, Stefano. 2017. “Strategic Energy Planning Under Uncertainty.” PhD
thesis, Lausanne, Switzerland: Ecole Polytechnique Fédérale de Lausanne.

Schnidrig, Jonas. 2020. “Assessment of Green Mobility Scenarios on
European Energy Systems.” PhD thesis, EPFL.
