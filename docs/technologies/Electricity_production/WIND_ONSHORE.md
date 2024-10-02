---
title: Wind Onshore
---

# Wind Onshore

## Introduction

Onshore wind energy is a widely adopted renewable technology that
harnesses the power of wind to generate electricity. This technology
involves the installation of wind turbines on land, typically in areas
with favorable wind conditions. Onshore wind turbines consist of tall
towers and large rotor blades, which work together to convert wind
energy into electrical power.

**Technical Aspects:**

- **Capacity Factor:** Onshore wind turbines typically have a capacity
  factor ranging from 20% to 40%, depending on wind conditions and
  turbine design. This factor represents the percentage of the
  turbine’s maximum capacity that it generates on average.

- **Wind Turbine Height:** Onshore wind turbines have tower heights
  that typically range from 70 to 120 meters above ground level. The
  height allows them to capture higher wind speeds at elevated
  altitudes.

- **Blade Length:** The rotor blades of onshore wind turbines can span
  30 to 80 meters or more. Longer blades capture more wind energy and
  increase the turbine’s efficiency.

## Global Deployment

Onshore wind energy has seen extensive global deployment and is one of
the most mature renewable energy technologies. According to the Global
Wind Energy Council (GWEC), the global onshore wind capacity reached
approximately 841.9 gigawatts (GW) by the end of 2022[^8]. Countries across
the world, including China, the United States, and Germany, have
embraced onshore wind power.

## Wind energy evolution in Switzerland

The 37 wind turbines installed in Switzerland, amounting to 75MW power
capacity, produced 122 GWh in 2018. It corresponds to the electricity
consumption of 36500 households, namely 0.2% of the total electricity
demand of Switzerland.

```python exec="true" html="true"
import pandas as pd
import plotly.express as px

# Data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
c_p_t = [0.325, 0.279, 0.282, 0.182, 0.176, 0.14, 0.149, 0.135, 0.162, 0.279, 0.313, 0.339]
prod = [round(75 * 122 / 207 * val, 3) for val in c_p_t]

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

## Use in Quebec

Quebec has significant potential for onshore wind energy due to its
diverse landscapes and wind resources. As of 2021, Quebec had 3.9 GW[^10] of
onshore wind power installed. The province has been actively developing
onshore wind farms as part of its renewable energy strategy. However,
the largest projects of onshore wind are currently developed in Ontario,
Alberta and British Columbia.[^9]

Quebec’s investment in onshore wind aligns with its commitment to
reducing greenhouse gas emissions and transitioning to cleaner energy
sources.

```python exec="true" html="true"
import pandas as pd
import plotly.express as px

# Data for the first plot
months1 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
c_p_t1 = [0.347, 0.385, 0.371, 0.353, 0.311, 0.282, 0.250, 0.229, 0.304, 0.349, 0.407, 0.394]
df1 = pd.DataFrame({"Month": pd.Categorical(months1, categories=months1, ordered=True), 
                    "Wind_Type": "Onshore", 
                    "c_p_t": c_p_t1})

# Data for the second plot
c_p_t2 = [0.494, 0.532, 0.468, 0.354, 0.288, 0.254, 0.268, 0.336, 0.480, 0.506, 0.528, 0.554]
df2 = pd.DataFrame({"Month": pd.Categorical(months1, categories=months1, ordered=True), 
                    "Wind_Type": "Offshore", 
                    "c_p_t": c_p_t2})

# Combine the data frames
df_combined = pd.concat([df1, df2])

# Reshape the data for plotting
df_combined_melted = pd.melt(df_combined, id_vars=["Month", "Wind_Type"], var_name="Metric", value_name="Value")

# Create the grouped bar plot using Plotly
fig = px.bar(
    df_combined_melted, 
    x="Month", 
    y="Value", 
    color="Wind_Type", 
    barmode="group",
    labels={"Value": "Capacity Factor [%]", "Wind_Type": "Wind Type"},
    title="Monthly Capacity Factor for Wind Onshore and Offshore in Quebec",
    color_discrete_map={'Offshore': '#003DA5', 'Onshore': '#D80621'}
)

# Customize the layout
fig.update_layout(
    yaxis=dict(title="Capacity Factor [%]", tickformat=".0%"),
    xaxis=dict(title="Month"),
    legend=dict(title="Wind Type"),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

print(fig.to_html(full_html=False, include_plotlyjs="cdn"))
```

## Use in Canada

Onshore wind energy plays a crucial role in Canada’s renewable energy
landscape. The country had approximately 15.2 GW of onshore wind
capacity by the end of 2022. Provinces like Ontario, Alberta, and Quebec
have been leaders in onshore wind development.[^11]

The Canadian government has set ambitious targets for expanding onshore
wind capacity as part of its efforts to reduce carbon emissions and
promote sustainable energy sources. Supportive policies and incentives
have further encouraged the growth of onshore wind projects across the
country.

```python exec="true" html="true"
import pandas as pd
import plotly.express as px

# Data for Quebec
years_quebec = [
    2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
    2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022
]
installed_cap_quebec = [
    207, 316.5, 417, 517.5, 650.8, 654.9, 827.733333333333, 1143.55,
    1837.26666666667, 2544.63125, 2958.97857142857, 3298.78333333333, 3298.78333333333,
    3696.4, 3696.4, 3776.4, 3806.95, 3806.95
]
inst_cap_gw_quebec = [cap / 1000 for cap in installed_cap_quebec]
df_quebec = pd.DataFrame({'Year': years_quebec, 'Installed_Capacity_GW': inst_cap_gw_quebec, 'Location': 'Quebec'})

# Data for Canada
years_canada = list(range(2005, 2022 + 1))
installed_cap_canada = [
    680, 1460, 1846, 2349, 3304, 3969, 5258, 6204, 7814, 9685, 11204, 11902, 12250,
    12818, 13413, 13558, 14304, 15200
]
inst_cap_gw_canada = [(can - que) / 1000 for can, que in zip(installed_cap_canada, installed_cap_quebec)]
df_canada = pd.DataFrame({'Year': years_canada, 'Installed_Capacity_GW': inst_cap_gw_canada, 'Location': 'Rest of Canada'})

# Combine the data frames
df_combined = pd.concat([df_canada, df_quebec])

# Create the stacked bar plot using Plotly
fig = px.bar(
    df_combined, 
    x='Year', 
    y='Installed_Capacity_GW', 
    color='Location', 
    title='Wind Generation Capacity by Year in Canada and Quebec',
    labels={'Installed_Capacity_GW': 'Installed Capacity (GW)', 'Year': 'Year'},
    color_discrete_map={'Quebec': '#003DA5', 'Rest of Canada': '#D80621'}
)

# Customize the layout
fig.update_layout(
    xaxis=dict(title='Year'),
    yaxis=dict(title='Installed Capacity (GW)'),
    template='plotly_white'
)

print(fig.to_html(full_html=False, include_plotlyjs="cdn"))
```

## ES Model Parameters

All the parameters concerning the **WIND_ONSHORE** are listed in the
table below. Detailed information on the data is available in the
section Parameters.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='WIND_ONSHORE'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='WIND_ONSHORE'))
```

[^1]. Confédération Suisse
[^2]:  Suisse éole,
<https://www.suisse-eole.ch/fr/energie-eolienne/statistiques/>
[^3]:  Swiss Energyscope
[^4]:  Basis of wind energy <https://www.awea.org/wind-101/basics-of-wind-energy>
[^5]:  Swiss Federal Office for the Environment. Energiestrategies 2050,
Tech. rep, Bern Swtizerland, Sept 2012

[^6]: “Projected Costs of Generating Electricity 2020 Analysis.” n.d. *IEA*.
https://www.iea.org/reports/projected-costs-of-generating-electricity-2020.
Accessed July 17, 2023.

[^7]: “Wind Turbines: The Bigger, the Better.” n.d. *Energy.gov*.
https://www.energy.gov/eere/articles/wind-turbines-bigger-better.
Accessed August 8, 2023.

[^8]: Global Wind Energy Council (
GWEC) - [Global Offshore Wind Report 2023](https://gwec.net/gwecs-global-offshore-wind-report-2023/)
[^9]: [Airswift - Top 5 wind energy projects in Canada](https://www.airswift.com/blog/wind-energy-canada)
[^10]:  Quebec Ministry of Energy and Natural Resources
[^11]:  Government of Canada
