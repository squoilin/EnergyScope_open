---
title: Plane LH
---

# Plane Long Haul

# Plane Long-Haul (LH)

## Overview

Long-haul flights refer to air travel over long distances, typically more than 4,000 kilometers (2,500 miles). These
flights are crucial for connecting continents and distant regions, facilitating international travel, global trade, and
cultural exchange. Long-haul aviation is essential for the global economy, offering non-stop service between major
cities around the world.

## Benefits

- **Global Connectivity**: Provides direct connections between distant cities and countries, reducing travel time
  compared to connecting flights.
- **Economic Impact**: Supports international business, tourism, and trade, contributing significantly to the global
  economy.
- **Comfort and Amenities**: Long-haul flights are designed for passenger comfort, offering various in-flight services
  and amenities to enhance the travel experience.

## Applications

- **International Travel**: Enables travel for business, tourism, education, and family visits across continents.
- **Global Trade**: Facilitates the rapid movement of goods and materials between countries, supporting international
  supply

## Challenges

- **Environmental Impact**: Long-haul flights contribute significantly to greenhouse gas emissions and global warming,
  making sustainability a major concern.
- **Operational Costs**: High costs associated with fuel, aircraft maintenance, and airport fees impact the
  profitability of long-haul routes.
- **Infrastructure Requirements**: Major international airports need extensive infrastructure to handle the demands of
  long-haul operations, including long runways and advanced logistics.

## Future Outlook

The future of long-haul aviation will focus on enhancing sustainability and efficiency. Innovations in aircraft
technology, such as more fuel-efficient engines, lightweight materials, and the development of sustainable aviation
fuels, will help reduce the environmental impact. Additionally, improvements in air traffic management and airport
infrastructure will support the growth of long-haul travel.

## Modelization

### Bottom-Up

The plane considered is an average plane regrouping Wide-Body's aircraft from 2013.[^1]

| Aircraft      | Type | Fleet size | Daily utilization  h/day | Aircraft cost $×10^6 | Seats   |
|---------------|------|------------|--------------------------|----------------------|---------|
| **777-300ER** | WB2  | 450        | 11,7                     | 320,2                | 370     |
| **A330-300**  | WB2  | 300        | 10,8                     | 248,87               | 277     |
| **767-300**   | WB2  | 220        | 9,5                      | 185,8                | 261     |
| **757-200**   | WB2  | 180        | 9                        | 84,17                | 200     |
| **747-400**   | WB3+ | 150        | 10,2                     | 292,13               | 524     |
| **A340-300**  | WB3+ | 125        | 11,5                     | 243,58               | 277     |
| **Plane LH**  |      |            | **10,7**                 | **244,94**           | **320** |

With an average load factor of **83.3%** during the period 2015-2019[^2].
and an average cruising speed of **734 km/h**[^3].

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

\n
$C_{p,ac}$ is the utilization factor and has been computed to be **39.2%**[^1].

Note that this method is global and can not differentiate the shot-haul from long-haul.

## ES Model Parameters

All the parameters concerning the Plane Long Haul are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PLANE_LH'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PLANE_LH'))
```

[^1]: Fioriti, M., Vercella, V., & Viola, N. (2018). Cost-Estimating Model for Aircraft Maintenance. Journal of
Aircraft. [doi: 10.2514/1.C034664](https://doi.org/10.2514/1.C034664)

[^2]: Operating and financial statistics for major Canadian airlines, monthly. (2024, July 09). Retrieved
from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2310007901

[^3]: Page sur le parc aérien d'Air Canada. (2024, June 27). Retrieved
from https://www.aircanada.com/ca/fr/aco/home/fly/onboard/fleet.html#
