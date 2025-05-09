---
title: H2 NG CCGT CCS
---

# H~2~ NG CCGT CCS

## Overview

Hydrogen and Natural Gas Combined Cycle Gas Turbine with Carbon Capture and Storage (H~2~ NG CCGT CCS) technology
combines hydrogen (H~2~) and natural gas (NG) as fuels in a combined cycle gas turbine (CCGT) system with the
integration of carbon capture and storage (CCS). This approach aims to reduce carbon emissions significantly while
providing efficient and reliable electricity generation.

## Process Description

1. **Fuel Blending**: Hydrogen and natural gas are blended in specific proportions and supplied to the gas turbine.
2. **Combustion**: The blended fuel is combusted in a gas turbine, producing high-temperature, high-pressure gases.
3. **Gas Turbine Operation**: The expanding gases drive the gas turbine, generating electricity.
4. **Heat Recovery Steam Generator (HRSG)**: Exhaust gases from the gas turbine pass through a heat recovery steam
   generator, producing steam.
5. **Steam Turbine Operation**: The steam produced is used to drive a steam turbine, generating additional electricity.
6. **Combined Cycle Efficiency**: The integration of gas and steam turbines enhances overall efficiency by utilizing the
   waste heat from the gas turbine to generate more power.
7. **Carbon Capture and Storage (CCS)**: CO~2~ emissions from the combustion process are captured and transported to a
   storage site where they are securely stored underground.

## Benefits

- **Significant Emissions Reduction**: Combining hydrogen with natural gas and integrating CCS drastically reduces CO~2~
  emissions.
- **High Efficiency**: Combined cycle configuration provides higher efficiency compared to simple cycle gas turbines.
- **Incremental Transition**: Allows for a gradual transition from natural gas to hydrogen, leveraging existing
  infrastructure.
- **Fuel Flexibility**: Can operate with varying proportions of hydrogen and natural gas, providing operational
  flexibility.
- **Carbon Neutral Potential**: With CCS, the system can potentially achieve near-zero carbon emissions.

## Applications

- **Utility Power Generation**: Used in large-scale power plants to provide reliable and efficient electricity to the
  grid.
- **Industrial Power**: Suitable for industrial facilities requiring both electricity and process steam.
- **Renewable Integration**: Can complement renewable energy sources by providing flexible and dispatchable power.

## Challenges

- **Hydrogen Source and Emissions**: The primary source of hydrogen is often grey hydrogen, which has associated CO~2~
  emissions. A transition to green hydrogen (produced from renewable energy) is necessary to maximize environmental
  benefits.
- **Lower Efficiency Compared to Fuel Cells**: Combustion-based systems are generally less efficient than hydrogen fuel
  cells, which directly convert chemical energy into electricity.
- **High Costs**: The addition of CCS technology increases capital and operational costs and reduces efficiency.
- **Technological Adaptation**: Modifications needed to handle hydrogen's unique combustion properties and material
  compatibility, as well as integrating CCS systems.

## Future Outlook

Advancements in hydrogen production technologies, such as electrolysis using renewable energy, improvements in gas
turbine designs, and cost reductions in CCS technology are expected to enhance the feasibility of H~2~ NG CCGT CCS
systems. This technology offers a pathway to significantly reduce carbon emissions while maintaining reliability and
efficiency in power generation. As the energy sector transitions to low-carbon solutions, H~2~ NG CCGT CCS systems are
poised to play a crucial role in achieving climate goals.

## ES Model Parameters

All the parameters concerning the Combine Cycle Gas Turbine H2 & NG CC are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='H2_NG_CCGT_CCS'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='H2_NG_CCGT_CCS'))
```
