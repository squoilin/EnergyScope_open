---
title: NG to Storage
---

# NG Storage

## Introduction

Natural gas, is a commodity that can be stored for an indefinite period
of time in storage facilities for later consumption, e.g. for
electricity production in peak periods, or directly used in vehicles,
cooking etc. Two possible ways for storing natural gas: salt cavern and depleted natural gas reservoir.

### Switzerland

With respect to Switzerland, salt cavern
is taken into consideration, with capex of 0.009 EUR/KWh and maintenance cost 2% of investment cost. It could also be
stored in existed pipelines, high pressure tanks etc.

### Quebec

Quebec has 2 depleted field reservoirs with a total volume of 5 Billion cubic feet[^1], 142 million m^3^.

### Canada

Underground natural gas storage facilities in Canada are located in five provinces: Alberta, British Columbia (B.C.),
Ontario, Quebec, and Saskatchewan. The combined capacity of all underground storage facilities in Canada is 949 Bcf. The
majority of this capacity (548 Bcf) is located in Alberta, followed by Ontario with 248 Bcf[^1].

## ES Model Parameters

In Energyscope, the depleted gas reservoir storage of natural gas is
taken into consideration, despite a slight difference of the cost for
cavern storage (CAPEX 0.012 EUR/kWh).

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='NG_STO'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='NG_STO'))
```

[^1]: [CER – Market Snapshot: Where does Canada store natural gas?](https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/market-snapshots/2018/market-snapshot-where-does-canada-store-natural-gas.html)(
2018)
