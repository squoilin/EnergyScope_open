---
title: Plane SH
---

# Plane Short-Haul (SH)

## Overview

Short-haul flights refer to air travel over relatively short distances, typically less than 1,500 kilometers (930
miles). These flights are crucial for connecting cities and regions, facilitating business travel, tourism, and cargo
transport. Short-haul aviation offers the convenience of quick travel times and frequent service, making it a popular
choice for many passengers and businesses.

## Process Description

- **Flight Operations**: Short-haul flights are operated by regional and domestic airlines using smaller aircraft
  designed for efficiency over short distances.
- **Airports**: These flights typically operate out of regional and domestic airports, which may have shorter runways
  and fewer facilities than major international hubs.
- **Passenger Service**: Short-haul flights often have quicker turnaround times and simpler boarding processes,
  enhancing convenience for passengers.

## Benefits

- **Convenience**: Provides quick and direct connections between cities and regions, reducing travel time compared to
  other modes of transport.
- **Frequency**: High frequency of flights allows for flexible travel planning and accommodates varying schedules.
- **Economic Impact**: Supports local economies by facilitating business travel, tourism, and regional trade.
- **Accessibility**: Improves accessibility to remote or less densely populated areas not well-served by other forms of
  transportation.

## Applications

- **Business Travel**: Enables efficient travel for business purposes, connecting regional offices, meetings, and
  conferences.
- **Tourism**: Supports the tourism industry by providing easy access to regional and domestic destinations.
- **Emergency Services**: Can be used for medical evacuations, disaster response, and other emergency services.

## Challenges

- **Environmental Impact**: Short-haul flights contribute to greenhouse gas emissions and air pollution, though less so
  than long-haul flights per trip.
- **Operational Costs**: High frequency of takeoffs and landings increases operational costs, including fuel,
  maintenance, and airport fees.
- **Infrastructure Strain**: Regional and domestic airports may face congestion and capacity issues during peak travel
  times.
- **Economic Viability**: Smaller aircraft have higher per-seat operating costs, which can impact the profitability of
  short-haul routes.

## Future Outlook

The future of short-haul aviation will likely focus on enhancing sustainability and efficiency. Technological
advancements in aircraft design, such as the development of electric and hybrid-electric planes, are expected to reduce
emissions and operational costs. Improvements in air traffic management and airport infrastructure should help alleviate
congestion.

## Modelization

### Bottom-Up

The plane considered is an average plane regrouping Narrow-Body's aircraft and Regional Jets from 2013.[^1]

| Aircraft     | Type | Fleet size | Daily utilization  h/day | Aircraft cost $×10^6 | Seats   |
|--------------|------|------------|--------------------------|----------------------|---------|
| **A320-200** | NB   | 890        | 8,4                      | 95,12                | 150     |
| **737-800**  | NB   | 650        | 9                        | 94,36                | 180     |
| **737-300**  | NB   | 75         | 6,3                      | 65,02                | 149     |
| **E-190**    | RJ   | 155        | 6,7                      | 46,2                 | 114     |
| **Plane SH** |      |            | **8,4**                  | **89,28**            | **158** |

With an average load factor of **83.3%** during the period 2015-2019[^2].
and an average cruising speed of 734 km/h[^3].

$$
ref_{size}= \text{Avg # of seats} \cdot \text{Load factor} \cdot \text{Average speed} \cdot \text{Ac utilization factor}
$$

### Top-Down

An other methods is consider the national statistics of Canada.

| *(thousands)                 | 2015        | 2016        | 2017        | 2018        | 2019        |
|------------------------------|-------------|-------------|-------------|-------------|-------------|
| Available seat-kilometres*   | 205 461 574 | 227 828 958 | 249 289 456 | 267 73 487  | 270 768 611 |
| Hours flown*  (HF)           | 1 985       | 2 43        | 2 160       | 2 270       | 2 277       |
| Passenger-kilometres*  (RPK) | 171 276 306 | 188 573 927 | 207 24 879  | 223 625 353 | 228 319 390 |
| Passengers*                  | 68 122      | 73 512      | 79 545      | 84 39       | 85 459      |
| Total operating revenues*    | 19 366 747  | 19 811 470  | 21 734 134  | 23 807 941  | 25 305 619  |
| Turbo fuel consumed*         | 6 545 65    | 6 994 641   | 7 587 721   | 7 932 156   | 8 102 149   |
| Fuel litre/RPK               | 0,0382      | 0,0371      | 0,0367      | 0,0355      | 0,0355      |

$$
\text{# Aircraft} = \dfrac{\sum HF [h]}{C_{p,ac} \cdot 8760[h] }
$$

$$
ref_{size} = \dfrac{\sum{RPK}[pkm]}{\text{# Aircraft}\cdot 8760[h]} = \dfrac{\sum RPK [pkm] \cdot C_{p,ac}}{\sum HF [h]}
$$

$C_{p,ac}$ is the utilization factor and has been computed to be **39.2%**[^1].

Note that this method is global and can not differentiate the shot-haul from long-haul.

## ES Model Parameters

All the parameters concerning the Plane Short Haul are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PLANE_SH'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PLANE_SH'))
```

[^1]: Fioriti, M., Vercella, V., & Viola, N. (2018). Cost-Estimating Model for Aircraft Maintenance. Journal of
Aircraft. [doi: 10.2514/1.C034664](https://doi.org/10.2514/1.C034664)

[^2]: Operating and financial statistics for major Canadian airlines, monthly. (2024, July 09). Retrieved
from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2310007901

[^3]: Page sur le parc aérien d'Air Canada. (2024, June 27). Retrieved
from https://www.aircanada.com/ca/fr/aco/home/fly/onboard/fleet.html#