---
title: H2 NG CCGT
---

# H~2~ NG CCGT

## Overview

Hydrogen and Natural Gas Combined Cycle Gas Turbine (H~2~ NG CCGT) technology combines the use of hydrogen (H~2~) and
natural gas (NG) as fuels in a combined cycle gas turbine (CCGT) system. This approach leverages the existing natural
gas infrastructure while progressively incorporating hydrogen to reduce carbon emissions and enhance the sustainability
of power generation.

## Process Description

1. **Fuel Blending**: Hydrogen and natural gas are blended in specific proportions and supplied to the gas turbine.
2. **Combustion**: The blended fuel is combusted in a gas turbine, producing high-temperature, high-pressure gases.
3. **Gas Turbine Operation**: The expanding gases drive the gas turbine, generating electricity.
4. **Heat Recovery Steam Generator (HRSG)**: Exhaust gases from the gas turbine pass through a heat recovery steam
   generator, producing steam.
5. **Steam Turbine Operation**: The steam produced is used to drive a steam turbine, generating additional electricity.
6. **Combined Cycle Efficiency**: The integration of gas and steam turbines enhances overall efficiency by utilizing the
   waste heat from the gas turbine to generate more power.

## Benefits

- **Reduced Emissions**: Blending hydrogen with natural gas reduces CO~2~ emissions compared to using natural gas alone.
- **High Efficiency**: Combined cycle configuration provides higher efficiency compared to simple cycle gas turbines.
- **Incremental Transition**: Allows for a gradual transition from natural gas to hydrogen, leveraging existing
  infrastructure.
- **Fuel Flexibility**: Can operate with varying proportions of hydrogen and natural gas, providing operational
  flexibility.

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
- **Cost**: High costs associated with hydrogen production and the adaptation of gas turbines for hydrogen use.
- **Technological Adaptation**: Modifications needed to handle hydrogen's unique combustion properties and material
  compatibility.

## Future Outlook

Advancements in hydrogen production technologies, such as electrolysis using renewable energy, and improvements in gas
turbine designs are expected to enhance the feasibility of H~2~ NG CCGT systems. This technology offers a transitional
pathway toward a more sustainable and low-carbon energy future by gradually increasing the use of hydrogen in power
generation. H~2~ NG CCGT systems hold significant potential for reducing emissions while maintaining reliability and
efficiency in the power generation sector.

## ES Model Parameters

All the parameters concerning the Combine Cycle Gas Turbine H2 & NG are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='H2_NG_CCGT'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='H2_NG_CCGT'))
```
