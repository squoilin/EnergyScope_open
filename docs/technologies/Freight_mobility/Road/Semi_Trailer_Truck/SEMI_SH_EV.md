---
title: Semi Electric SH
---

# Semi Electric SH

## Semi Trailer Truck - Short Haul Overview

The **Heavy-Duty Truck used for Short-Haul** journeys stands as a pillar
of the transport sector, specially configured to transport large volumes
of freight over relatively short distances. This category includes
tractor/semitrailer combinations with more than four tires, used for
operations within a 320 km range.

### Semi Trailer Truck Short-Haul Performance Metrics

- **Operational Range:** Used with a maximum operational range of up
  to 320 km.
- **Annual Performance (*d~annual~*):** Boasting
  an annual performance capability of 105,000 km.
- **Load Capacity (*n~lpv~*):** With a substantial
  average load capacity of 5.76 tonnes per vehicle.
- **Average Speed:** Operating at an average speed of 80 km/h,
  optimizing delivery times for short-haul logistics.
- **Capacity Factor:** A 15% capacity utilization factor is
  considered.
- **Reference Capacity:** The derived reference capacity of 460.27
  tonne-kilometers per hour (tkm/h).

The reference capacity is calculated as follows:

$$
ref_{capacity} = \dfrac{d_{annual} \cdot n_{lpv} \cdot average\\speed}{8760 \cdot 0.15}
$$

This calculation method accounts for the annual distance, average load
capacity, average speed, and the capacity utilization rate.

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

## ES Model Integration

All the parameters concerning the Semi Electric SH are listed in the
table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_SH_EV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='SEMI_SH_EV'))
```
