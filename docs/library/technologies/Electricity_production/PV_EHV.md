---
title: PV Alpine (CH)
---

# PV Alpine

## Introduction

This technology was incorporated by Fischer (2023)[^1] to represent the planned alpine PV parks in the Swiss Alps.

Due to a favorable weather at high altitude, Alpine PV present a better exposition especially during winter months.

This technology should only be used in CH EnergyScope

```python exec="true" html="true"
import pandas as pd
import plotly.express as px

# Data for non-alpine PV
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
c_p_t_non_alpine = [0.053, 0.094, 0.12, 0.153, 0.156, 0.157, 0.164, 0.156, 0.128, 0.088, 0.052, 0.036]
df_non_alpine = pd.DataFrame({"Month": pd.Categorical(months, categories=months, ordered=True),
                              "PV_Type": "Non-Alpine",
                              "c_p_t": c_p_t_non_alpine})

# Data for alpine PV
c_p_t_alpine = [0.286, 0.303, 0.223, 0.174, 0.134, 0.112, 0.121, 0.146, 0.148, 0.163, 0.166, 0.173]
df_alpine = pd.DataFrame({"Month": pd.Categorical(months, categories=months, ordered=True),
                          "PV_Type": "Alpine",
                          "c_p_t": c_p_t_alpine})

# Combine the data frames
df_combined = pd.concat([df_non_alpine, df_alpine])

# Reshape the data for plotting
df_combined_melted = pd.melt(df_combined, id_vars=["Month", "PV_Type"], var_name="Metric", value_name="Value")

# Create the grouped bar plot using Plotly
fig = px.bar(
    df_combined_melted,
    x="Month",
    y="Value",
    color="PV_Type",
    barmode="group",
    labels={"Value": "Capacity Factor [%]", "PV_Type": "PV Type"},
    title="Monthly Capacity Factor for Alpine and Non-Alpine PV in the Swiss Alps",
    color_discrete_map={'Alpine': '#2E8B57', 'Non-Alpine': '#ADD8E6'}
)

# Customize the layout
fig.update_layout(
    yaxis=dict(title="Capacity Factor [%]", tickformat=".0%"),
    xaxis=dict(title="Month"),
    legend=dict(title="PV Type"),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

print(fig.to_html(full_html=False, include_plotlyjs="cdn"))
```

## ES Model Parameters

All the parameters concerning the PV Alpine are listed in the table
below.

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PV_EHV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PV_EHV'))
```

[^1]: Fischer, L. (
2023). [Integrating Alpine Photovoltaic Technology into EnergyScope: A Case Study of Switzerland’s Energy System.](https://infoscience.epfl.ch/record/302978?ln=en)
Infoscience.
