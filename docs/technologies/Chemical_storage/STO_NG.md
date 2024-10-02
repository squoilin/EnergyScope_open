---
title: Storage to NG
---

# Usage of Stored NG

## Introduction

This technology represents the release of stored Natural Gas. This is the reverted technology of [NG Storage](NG_STO.md)

NG is a
commodity that can be stored for an indefinite period of time in storage
facilities for later consumption, e.g. for electricity production in
peak periods, or directly used in vehicles, cooking etc. Two possible
ways for storing natural gas: salt cavern and depleted natural gas
reservoir. With respect to Switzerland, salt cavern is taken into
consideration, with capex of 0.009euro/KWh and maintenance cost 2% of
investment cost. It could also be stored in existed pipelines, high
pressure tanks etc.

## ES Model Parameters

All the parameters concerning the Storage NG are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='STO_NG'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='STO_NG'))
```
