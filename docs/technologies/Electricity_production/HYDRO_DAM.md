---
title: Hydro Dam
---

# Hydro Dam

## Introduction

## General

Hydropower or water power is power derived from the energy of falling or fast-running water, which may be harnessed for
useful purposes [^5]. A hydropower resource can be evaluated by its available power. Power is a function of the
hydraulic head and volumetric flow rate. The head is the energy per unit weight (or unit mass) of water. The static head
is proportional to the difference in height through which the water falls.
Dynamic head is related to the velocity of moving water. Each unit of water can do an amount of work equal to its weight
times the head. The power available from falling water can be calculated from the flow rate and density of water, the
height of fall, and the local acceleration due
to gravity:

$$
\dot{E}_{out} = \eta \rho g \dot{V} \Delta h
$$

where $\dot{E}_{out}$ denotes the output electricity, $\eta$ the conversional efficiency, $\rho g \dot{V}$ is the mass
flow, and $\Delta h$ represents the height difference of the inlet and outlet
flows.

## Global warming effects on water discharges in Switzerland

The hydraulic regime has an obvious impact on the behaviour of dams and their storage in the context of global warming,
shedding light on the study of the difference of water flows between current situation and the long-term horizon.
Snowmelt will occur earlier each year, and the gradual loss of glacier volume will lead to a decrease in inflows into
dams by 2100 [^1]. In addition, rainfall patterns will change depending on the region and more extreme weather events
are expected, leading to more water being evacuated from dams for safety reasons, and therefore not turbined.

To analyze the hydro discharges all over Switzerland, the PREVAH [^2] adopted a 200 x 200 m grid [^2] modeling approach
for three time horizons: the “present” (from 1980 to 2009), the “near future” (2021-2050) and the “far future” (
2070-2099). J.Dujardin [^3] developped a methodology to determine the monthly water inflows of run-of-Hydro River
plants, with the Confederation’s 2015 database of hydro power plants [^4] taking into consideration the geolocation of
the power plants.

Accroding to [^7], the flows measured in Switzerland will change little in the short term (2035), with the exception of
a few transient increases in the heavily glaciated regions. In the long term (2085), most Hydro Rivers are expected to
decrease slightly, with the exception of Ticino and Toce, where the decrease is expected to be around 10%. In the Alpine
space, warming is the main factor influencing the seasonal distribution of flows: the limit of snowfall will rise, while
the reserves of meltwater, as well as the volume and surface of glaciers will decrease little. The seasonal distribution
of flows (water regime) will change in most of Switzerland, with, in many regions, higher flows in winter and less in
summer. Even large Hydro Rivers will see their flows change in this direction. In many areas of the Plateau, the flood
period will move and/or lengthen. The Rhine region, for example, will see a second seasonal peak in winter, while in
many other areas, floods will increase in strength and frequency. On the Plateau, periods of low water will be much more
highlighted and will last longer (in summer), even for large Hydro Rivers. In the Alps, some of the low flows will no
longer occur in winter but at the end of summer.

The renewable water resources available in a given region include the water flowing into streams. The flows of these
Hydro Rivers are a function of the regional water balance, which takes into account rainfall, evaporation and changes in
water supplies:

$$
\text{WaterFlow} = \text{Precipitation} - \text{Evaporation} -\Delta \text{Reserve}
$$

# Hydroelectric Hydro Dam Reservoirs

## 1: Introduction

Hydroelectric dam reservoirs, pivotal components in the domain of
renewable energy, exemplify the conversion of stored gravitational
potential energy of water into electrical energy. Central technical
facets of this technology involve:

- **Hydro Dam Structure**: Encompassing materials such as concrete or
  embankments, dams obstruct Hydro River flow, generating a reservoir,
  and providing the requisite hydraulic head for potential energy.

- **Turbine Technology**: Predominantly employing Kaplan, Francis, or
  Pelton turbines, the specific choice depends on the hydraulic head
  and flow rate of the reservoir.

- **Capacity and Energy Generation**: Ranging from a few MW to several
  GW, depending on the size and hydraulic characteristics of the
  reservoir, with larger reservoirs facilitating dispatchable energy
  supply by controlling water release.

- **Capacity Factor**: This quantifies the ratio of the actual
  electrical energy output over a specific duration to the potential
  energy output if the plant were operating at full capacity
  throughout the same interval. Hydroelectric dam reservoirs typically
  exhibit high capacity factors, often exceeding 50%, owing to their
  capacity to consistently generate electricity, subject to hydraulic
  conditions.

- **Environmental and Social Implications**: Involving considerations
  of local ecology, water usage, and potential displaCement Prod. of
  communities, thorough environmental and social impact assessments
  are indispensable.

## 2: Global Deployment

Hydroelectric dam reservoirs are ubiquitously deployed across the globe,
particularly in regions with ample hydrological resources. As of 2021,
hydroelectricity, predominantly sourced from dam reservoirs, comprised a
significant portion of global renewable energy, contributing to an
installed capacity of approximately 1,360 GW, representing a vital
component in worldwide renewable energy generation.

## 3: Use in Quebec and Canada

### Quebec

In Quebec, hydroelectric dam reservoirs are integral to the province’s
energy matrix. The James Bay Project, one of the world’s largest
hydroelectric systems, is a testament to the province’s commitment and
dependency on reservoir hydroelectricity.

Quebec has leveraged its hydrological resources effectively, channeling
the harnessed energy to not only cater to its domestic demands but also
to export electricity to neighboring provinces and the United States,
hence bolstering its economic framework through renewable energy trade.

### Canada

In a broader Canadian context, hydroelectric dam reservoirs represent a
cornerstone of the nation’s energy portfolio. Canada, harboring the
fourth-largest hydroelectric infrastructure globally, substantiated a
third-place positioning in annual hydroelectric production, registering
over 383 TWh in 2021.

Historically rooted in 1881, Canada’s hydroelectric odyssey has
witnessed the construction of at least 566 hydroelectric plants,
cumulatively contributing an installed power of 82,990 MW as of 2023.
The epochs between the 1950s and the 1990s witnessed a pronounced
acceleration in capacity enhanCement Prod., moderating towards the
latter part of the 2000s.

Over a recent five-year stretch, hydroelectric production has swelled by
an approximate 2,400 MW, chiefly attributable to the inception of
substantial plants such as Romaine-3 (395 MW) and Romaine-4 (245 MW) in
Quebec in 2017 and 2023 respectively, Keeyask (695 MW) in Manitoba in
2022, and Muskrat Falls (824 MW) in Newfoundland and Labrador in 2021.

The trajectory of Canada’s hydroelectric development, enriched by its
reservoir-based initiatives, underlines the role of comprehensive
planning, meticulous development, and socio-ecological adherence in
navigating future sustainable energy pathways.

## ES Model Parameters

All the parameters concerning the **HYDRO_DAM** are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='HYDRO_DAM'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='HYDRO_DAM'))
```

[^1]:  D. Finger, G. Heinrich, A. Gobiet, and A. Bauder, “Projections of
future water resources and their uncertainty in a glacierized
catchment in the Swiss Alps and the subsequent effects on hydropower
production during the 21st century,” Water Resources Research,
vol. 48, no. 2, pp. n/a–n/a, 2012.  
[^2]:  D. Viviroli, M. Zappa, J. Gurtz, and R. Weingartner, “An
introduction to the hydrological modelling system PREVAH and its
pre- and post-processing-tools,” Environmental Modelling & Software,
vol. 24, no. 10, pp. 1209–1222, Oct. 2009
[Online](http://www.sciencedirect.com/science/article/pii/S1364815209000875)  
[^3]:  J. Dujardin, “Catchment aggregation regime, zip file.” Mar-2016
[Online](https://wiki.epfl.ch/hydrodata/hydroregime).  
[^4]:  SFOE, “Statistique des aménagements hydroélectriques de la Suisse.
2013-2019,” Swiss Federal Office of Energy, 2019  
[^5]: Wikipedia [Wikipedia](https://en.wikipedia.org/wiki/Hydropower).
[^6]:  E.Burdet, “The role of power-to-gas and accumulation dams as
seasonal storage facilities for Switzerland’s energy transition”,
Master thesis, EPFL, 2019  
[^7]:  P. Varilek and U. Nöthiger-Koch, “Impacts des changements
climatiques sur les eaux et les ressources en eau,” p. 78.  
[^8]:  (Hubacher & Schädler 2010)  
[^9]:  Zappa et al, 2012
