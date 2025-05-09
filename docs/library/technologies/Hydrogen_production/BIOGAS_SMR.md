---
title: Biogas Steam Methane Reforming
---

# Biogas Steam Methane Reforming

## Introduction

In the Steam Methane Reforming (SMR)
process, depicted in Figure 1a, natural gas is combined with
high-pressure steam and introduced into reforming tubes containing
catalysts conducive to the reforming reactions. These reactions are
inherently endothermic, necessitating the integration of a furnace
within the reforming section to provide the essential thermal energy.
The fuel for this furnace is sourced from natural gas and the purge
stream from the Pressure Swing Adsorption (PSA) unit.

For systems equipped with carbon capture technology, an additional CO~2~
removal unit is imperative to isolate and liquefy the CO~2~ present in the
flue gas stream emanating from the furnace.[^1]

In this case the input gas is not natural gas but biogas.[^2]

<figure markdown="span">
  ![Layout of the SR reference case (SR: steam reforming; HX: heat exchanger; BG: biogas; SH: superheater; EV: evaporator; LT: low temperature; WGS: water gas shift; HT: high temperature; SEP: water separator CMP: compressor; PSA: pressure swing adsorption).source:(2)](../../assets/BIOGAS_SMR.png)
  <figcaption>Layout of the SR reference case (SR: steam reforming; HX: heat exchanger; BG: biogas; SH: superheater; EV: evaporator; LT: low temperature; WGS: water gas shift; HT: high temperature; SEP: water separator CMP: compressor; PSA: pressure swing adsorption).source:(2)</figcaption>
</figure>

## ES Model Parameters

All the parameters concerning the Biogas Steam Methane Reforming are
listed in the table below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='BIOGAS_SMR'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='BIOGAS_SMR'))
```

[^1]: Khojasteh Salkuyeh, Yaser, et al. “Techno-economic analysis and
life cycle assessment of hydrogen production from natural gas using
current and emerging technologies.” Int. J. Hydrogen Energy, vol. 42,
no. 30, 27 July 2017, pp. 18894-909,
www.sciencedirect.com/science/article/pii/S0360319917322036.

[^2]: Marcoberardino, Gioele Di, et al. “Green Hydrogen Production from
Raw Biogas: A Techno-Economic Investigation of Conventional Processes
Using Pressure Swing Adsorption Unit.” Processes, vol. 6, no. 3, 25
Feb. 2018, p. 19, www.mdpi.com/2227-9717/6/3/19.
