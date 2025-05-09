---
title: LCV Methane FC
---

# LCV Methane FC

## Light Commercial Vehicle Class Overview

The **Light Commercial Vehicle** class encompasses four-wheeled,
two-axle vehicles, primarily designed for goods transportation. These
vehicles are notable for their adaptability to a range of cargo needs,
demonstrating versatility in the light-duty commercial sector.

### Light Commercial Vehicle Performance Metrics

- **Operational Distance (*d~annual~*):** On an
  annual basis, these vehicles are capable of covering a distance of
  38,600 km.
- **Average Cargo Weight (*n~lpv~*):** They support an
  average cargo weight of 0.19 tonnes per vehicle, accommodating the
  transportation needs of various goods.
- **Capacity Factor:** A 10% capacity utilization factor is applied to
  account for frequent stops and loading times, which are
  characteristic of their operational environment.
- **Reference Efficiency:** This results in a reference efficiency of
  8.37 tonne-kilometers per hour (tkm/h), underlining their essential
  role in fulfilling light-duty commercial transportation tasks.

The reference efficiency is calculated as follows:

$$
ref_{efficiency} = \dfrac{d_{annual} \cdot n_{lpv}}{8760 \cdot c_p}
$$

Where c~p~ represents the capacity utilization percentage.
This formula reflects the annual operational distance, the average cargo
weight, and the capacity utilization factor, offering a clear
perspective on the efficiency and utility of Light Commercial Vehicles
in commercial transportation.

## Methane Fuel Cell

Methane fuel cell vehicles leverage the chemical energy of methane, CH4,
to generate electricity through a fuel cell. These vehicles operate on
the principle of converting methane directly into electrical energy,
which then powers the vehicle’s electric motor.

## ES Model Integration

All the parameters concerning the LCV Methane FC are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='LCV_FC_CH4'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='LCV_FC_CH4'))
```
