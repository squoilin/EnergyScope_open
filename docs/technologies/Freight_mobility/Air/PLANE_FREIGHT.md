---
title: Plane Freight
---

# Plane Freight

## Overview

Plane freight, also known as air cargo, involves the transportation of goods by aircraft. This mode of transportation is
essential for the rapid delivery of high-value, time-sensitive, or perishable goods across long distances. Air freight
is a crucial component of the global logistics and supply chain network, connecting markets and enabling international
trade.

## Benefits

- **Speed**: Air freight is the fastest mode of transportation for long-distance shipping, significantly reducing
  delivery times.
- **Reliability**: Offers high levels of reliability and punctuality, with fixed schedules and less risk of delays
  compared to sea or land transport.
- **Global Reach**: Connects to a vast network of international destinations, enabling global trade and market access.
- **Security**: Provides enhanced security measures and reduces the risk of theft or damage.

## Applications

- **High-Value Goods**: Transportation of electronics, pharmaceuticals, and luxury items.
- **Time-Sensitive Deliveries**: Delivery of perishable goods, express parcels, and critical supplies.
- **Emergency Shipments**: Transportation of urgent and relief supplies during emergencies and natural disasters.

## Challenges

- **Cost**: Air freight is generally more expensive than other modes of transport due to fuel costs, handling fees, and
  airport charges.
- **Capacity Limits**: Aircraft have limited cargo space and weight capacity compared to ships and trains.
- **Environmental Impact**: Air transportation has a higher carbon footprint per ton-mile compared to sea and land
  transport, contributing to greenhouse gas emissions.
- **Regulatory Compliance**: Requires adherence to stringent international regulations and security protocols.

## Modelization

The reference size of and air freighter was computed based on FedEx[^1] [^2] data, since Fedex was in 2021 the largest
air transporter.

$$
ref_{size}=\dfrac{\text{billion Cargo Tonne Kilometers (CTK)}}{\text{# of aircraft} * 8760 [h]}
$$

The average fleet cost is estimated to be **51 MUSD** per aircraft.

The maintenance cost are set to **5%** of the investment costs.

## ES Model Parameters

All the parameters concerning the Plane Freight are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PLANE_FREIGHT'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PLANE_FREIGHT'))
```

[^1]: Doran, Michael. 2022. « FedEx Tops IATA World Cargo Carrier Rankings In 2021 ». Simple
Flying. https://simpleflying.com/fedex-tops-world-cargo-rankings-2021/ (21 novembre 2023).

[^2]: Jeffrey, Rebecca. 2023. « Top 25 Air Cargo Carriers: Cargo Airlines Tackle Tough Times ». Air Cargo
News. https://www.aircargonews.net/data/top-25-air-cargo-carriers-cargo-airlines-tackle-tough-times/ (21 novembre 2023).
