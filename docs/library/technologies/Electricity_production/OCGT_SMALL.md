---
title: OCGT 100MW
---

# OCGT Small

## Overview

Small Open Cycle Gas Turbine (OCGT) systems (100MW) are a type of gas turbine power plant where air is compressed, mixed
with fuel, and combusted. The resulting high-temperature gases expand through a turbine to generate electricity. Unlike
combined cycle systems, OCGTs do not utilize waste heat for additional power generation, making them simpler but less
efficient.

## Process Description

1. **Air Compression**: Ambient air is drawn into the compressor where it is compressed to a high pressure.
2. **Fuel Injection**: The compressed air is mixed with fuel (natural gas or other suitable fuels) and injected into the
   combustion chamber.
3. **Combustion**: The fuel-air mixture is combusted at high temperatures, producing high-pressure, high-temperature
   gases.
4. **Turbine Expansion**: The hot gases expand through the turbine, driving it to generate electricity.
5. **Exhaust**: After passing through the turbine, the exhaust gases are released into the atmosphere.

## Benefits

- **Simple Design**: Fewer components and systems compared to combined cycle plants, leading to lower capital costs and
  easier maintenance.
- **Quick Start-Up**: Can reach full power output quickly, making OCGTs suitable for peaking power and emergency power
  applications.
- **Fuel Flexibility**: Capable of operating on a variety of fuels, including natural gas, diesel, and synthetic fuels.
- **Scalability**: Suitable for small to medium power generation needs, including remote and off-grid applications.

## Applications

- **Peaking Power Plants**: Used to meet peak electricity demand due to their ability to start up quickly.
- **Emergency Power**: Provides backup power for critical infrastructure during outages.
- **Remote Power Generation**: Ideal for locations without access to a stable power grid.
- **Industrial Power**: Supplies power for industrial facilities with fluctuating power needs.

## Challenges

- **Lower Efficiency**: OCGTs have lower thermal efficiency compared to combined cycle gas turbines (CCGTs) because
  waste heat is not recovered for additional power generation.
- **Higher Emissions**: Without waste heat recovery, OCGTs tend to have higher emissions per unit of electricity
  generated.
- **Fuel Costs**: Operating costs can be high due to fuel consumption, especially when using more expensive or less
  efficient fuels.

## Future Outlook

Improvements in turbine technology, materials, and fuel efficiency are expected to enhance the performance of OCGTs. As
a flexible and reliable power generation option, OCGTs will continue to play a vital role in providing peaking power,
emergency power, and support for renewable energy integration. Additionally, the potential integration of cleaner fuels
such as hydrogen could further reduce emissions and enhance the sustainability of OCGT systems.

## ES Model Parameters

All the parameters concerning the OCGT Small are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='OCGT_SMALL'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='OCGT_SMALL'))
```
