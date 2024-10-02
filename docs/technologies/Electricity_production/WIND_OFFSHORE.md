---
title: Wind Offshore
---

# Offshore Wind Energy

## Introduction

Offshore wind energy harnesses the power of wind above the seas and
oceans to generate electricity. It capitalizes on the more consistent
and stronger wind speeds over water compared to land. The technical
aspects of offshore wind energy are distinct and sometimes more advanced
than their onshore counterparts:

- **Turbine Size and Height**: Offshore wind turbines are typically
  larger than onshore ones. As of 2021, the most common offshore
  turbines being installed have capacities of 8-10 MW, though newer
  models can even exceed 12 MW. The rotor diameter of these turbines
  can be over 150 meters, and with hub heights of over 100 meters,
  these turbines can harness wind from higher altitudes where it’s
  more consistent.

- **Foundation Types**: Offshore wind turbines use various foundation
  types depending on water depth, including monopiles, gravity-based
  structures, floating platforms, and jacket foundations.

- **Capacity Factor**: Due to the consistency of oceanic winds,
  offshore wind farms generally have a higher capacity factor compared
  to onshore farms. While onshore wind farms have capacity factors
  typically in the 20-40% range, offshore wind farms can achieve
  40-60%, meaning they produce electricity more consistently over
  time.

- **Transmission**: Transmitting the generated electricity to the grid
  on land requires undersea cables, which can be a significant part of
  the project’s costs. These cables need to be adequately insulated
  and protected from marine life and ship anchors.

## Global Deployment

As of 2023, offshore wind has seen rapid growth, especially in regions
like Europe and Asia. Europe has led the global deployment with
countries like the UK, Denmark, and Germany installing significant
capacities. China has also aggressively expanded its offshore wind
installations. The global offshore wind capacity surpassed 64.3 GW in
2022, with projections to reach 380 GW by 2030, highlighting the
increasing trust and investment in this technology.[^1]

## Use in Quebec and Canada

### Quebec

As of 2021, Quebec has predominantly relied on its vast hydropower
resources for electricity. However, there has been growing interest in
diversifying its renewable energy portfolio, including looking into the
potential for offshore wind. The St. Lawrence River presents a potential
avenue for deployment. However, specific projects and detailed
feasibility studies would be required to assess the exact potential and
challenges, including environmental and socio-economic considerations.
As of 2023, Quebec has not yet ventured into offshore wind projects.

### Canada

Canada’s venture into offshore wind energy has been limited, but there’s
potential, especially off the Atlantic coasts of Newfoundland and Nova
Scotia. The country has abundant wind resources, and while onshore wind
has been the primary focus, offshore offers an opportunity to tap into
stronger and more consistent winds. As of 2021, Canada does not have any
large-scale offshore wind farms in operation, but some early-stage
projects and studies are underway, signaling a potential shift towards
embracing this technology in the coming years.[^4]

The country’s first offshore wind project, the Wind Energy Institute of
Canada (WEICan) Wind R&D Park in Prince Edward Island, commenced
operations in 1981.[^2] Nevertheless, Canada boasts vast offshore wind
potential along its coastlines, including the Atlantic, Pacific, and
Arctic regions.

In a 2021 research assessment, the offshore wind energy potential for
Canada was quantified at approximately 2,333 GW. This capacity is
distributed across various maritime regions: the Atlantic Ocean
encompasses the majority with an estimated 1,341 GW, the St. Lawrence
Bay accounts for 280 GW, and the Hudson Bay contributes an additional
316 GW.[^3]

## Monthly production

The electricity production from windfarms reaches the peak in winter,
while the output in summer is merely half of the maximal value
approximately.

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
    title="Monthly Capacity Factor for Wind Onshore in Quebec and Averaged Monthly Capacity Factor for Block Island Wind (Prince), 2017-2021",
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

## ES Model Parameters

All the parameters concerning the **WIND_OFFSHORE** are listed in the
table below. Detailed information on the data is available in the
section Parameters.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='WIND_OFFSHORE'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib',filter_entry='WIND_OFFSHORE'))
```

[^1]:  Global Wind Energy Council (
GWEC) - [Global Offshore Wind Report 2023](https://gwec.net/gwecs-global-offshore-wind-report-2023/)
[^2]:  Quebec Ministry of Energy and Natural Resources - [facilities](https://www.weican.ca/facilities)
[^3]:  [Offshore wind can power Canada](https://www.sciencedirect.com/science/article/pii/S0360544221016704?via%3Dihub)
[^4]:  [Government of Canada](https://www.canada.ca/en/natural-resources-canada/news/2023/05/building-offshore-renewables-in-newfoundland-and-labrador-and-nova-scotia.html)
