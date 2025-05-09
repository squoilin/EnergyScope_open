---
title: Gasification H2
---

# Biomass Gasification to H~2~

## Introduction

Gasification is a thermochemical conversion process to extract energy
from biomass. It converts a carbonaceous solid into a producer gas (wood
gas in the case of wood feedstock) thanks to a gasification agent. The
producer gas is a mixture of H~2~, CO, CO~2~ and N~2~ while the gasification
agent can be air, steam or oxygen. There are different configurations of
gasification technologies such as fluidized bed, entrained flow
or fixed bed. Based on the configuration, the obtained mixture and the
level of impurities will be different. The derived producer gas need to
be cleaned by several processes to obtain pure hydrogen. A water gas
shift unit is used to increase the H~2~ yield and to lower the CO content.
A RME scrubber is used to remove the significant amount of tars
impurities. Then, an amine scrubber allows to separate CO~2~ from the
gaseous stream. Finally, a pressure swing adsorption process is used to
separate hydrogen from the remaining gas components in order to get high
purity hydrogen.

## ES Model Parameters

All the parameters concerning the Gasif. H~2~ are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='GASIFICATION_H2'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='GASIFICATION_H2'))
```
