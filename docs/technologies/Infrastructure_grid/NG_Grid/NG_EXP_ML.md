---
title: NG Exp MP-LP
---

# NG Exp. ML

## Introduction

Natural Gas Expansion from Medium Pressure to Low Pressure, more information on the
modelization [here](https://gitlab.com/ipese/on-the-role-of-energy-infrastructure-in-the-energy-transition/-/tree/main/03_Infrastructure-Documentation/02_Gas-Infrastructure?ref_type=heads).

## ES Model Parameters

All the parameters concerning the NG Exp. ML are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='NG_EXP_ML'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='NG_EXP_ML'))
```
