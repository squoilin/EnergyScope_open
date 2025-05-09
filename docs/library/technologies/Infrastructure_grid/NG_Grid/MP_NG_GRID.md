---
title: NG Grid MP
---

# NG Grid MP

## Introduction

Natural Gas Grid at Medium Pressure, more information on the
modelization [here](https://gitlab.com/ipese/on-the-role-of-energy-infrastructure-in-the-energy-transition/-/tree/main/03_Infrastructure-Documentation/02_Gas-Infrastructure?ref_type=heads).

## ES Model Parameters

All the parameters concerning the NG Grid MP are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='MP_NG_GRID'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='MP_NG_GRID'))
```
