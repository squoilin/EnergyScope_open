---
title: PV Residential (CH)
---

# PV Residential

## Introduction

This technology was incorporated by Fischer (2023)[^1] to represent Residential PV.

This technology should only be used in CH EnergyScope.

## ES Model Parameters

All the parameters concerning the PV Residential are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PV_LV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PV_LV'))
```

[^1]: Fischer, L. (
2023). [Integrating Alpine Photovoltaic Technology into EnergyScope: A Case Study of Switzerland’s Energy System.](https://infoscience.epfl.ch/record/302978?ln=en)
Infoscience.
