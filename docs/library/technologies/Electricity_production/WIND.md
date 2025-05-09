---
title: Introduction
---

# WIND

## Introduction

Wind energy (or wind power) refers to the process of electricity
production using the wind, or air flows that occur naturally in the
earth’s atmosphere. Modern wind turbines are used to capture kinetic
energy from the wind and generate electricity.

There are three main types of wind energy [^4]:

- Utility-scale wind: Wind turbines that range in size from 100KW to
  several megawatts, where the electricity is delivered to the power
  grid and distributed to the end user by electric utilities or power
  system operators.
- Distributed or “small” wind: Single small wind turbines below 100KW
  that are used to directly power a home, farm or small business and
  are not connected to the grid.
- Offshore wind: Wind turbines that are erected in large bodies of
  water, usually on the continental shelf. Offshore wind turbines are
  larger than land-based turbines and can generate more power.

As an inland country, the offshore wind is not considered for
Switzerland.

## Wind energy evolution in Switzerland

The 37 wind turbines installed in Switzerland, amounting to 75MW power
capacity, produced 122 GWh in 2018. It corresponds to the electricity
consumption of 36500 households, namely 0.2% of the total electricity
demand of Switzerland.

## Monthly production

The electricity production from windfarms reaches the peak in winter,
while the output in summer is merely half of the maximal value
approximately.

```python exec="true" html="true"
import pandas as pd
import plotly.express as px

# Data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
c_p_t = [0.325, 0.279, 0.282, 0.182, 0.176, 0.14, 0.149, 0.135, 0.162, 0.279, 0.313, 0.339]
prod = [75 * 122 / 207 * val for val in c_p_t]

df = pd.DataFrame({'Month': months, 'Production': prod})

# Create the bar plot
fig = px.bar(
    df, 
    x='Month', 
    y='Production', 
    title="Monthly power production from WIND panels in Switzerland, 2018 [4]", 
    labels={'Month': 'Month', 'Production': 'Energy (GWh)'},
    text='Production'
)

# Customize the layout
fig.update_traces(marker_color='red', textposition='outside')
fig.update_layout(
    xaxis=dict(title='Month'),
    yaxis=dict(title='Energy (GWh)'),
    template='plotly_white'
)

print(fig.to_html(full_html=False, include_plotlyjs="cdn"))
```

## ES Model Parameters

All the parameters concerning the **WIND** are listed in the table
below. Detailed information on the data is available in the section
Parameters.

## References

1. Confédération Suisse
2. Suisse éole,
   <https://www.suisse-eole.ch/fr/energie-eolienne/statistiques/>
3. Swiss Energyscope
   [^4]:  Basic <https://www.awea.org/wind-101/basics-of-wind-energy>
5. Swiss Federal Office for the Environment. Energiestrategies 2050,
   Tech. rep, Bern Swtizerland, Sept 2012
