---
title: Transformer EHV-HV
---

# Transformer EH

## Introduction

Extra High to High Voltage Transformer, more information on the
modelization [here](https://gitlab.com/ipese/on-the-role-of-energy-infrastructure-in-the-energy-transition/-/tree/main/03_Infrastructure-Documentation/01_Electricity-infrastructure?ref_type=heads).

## ES Model Parameters

All the parameters concerning the Transformer EH are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='TRAFO_EH'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='TRAFO_EH'))
```
