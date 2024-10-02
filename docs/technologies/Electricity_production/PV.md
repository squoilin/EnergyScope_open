---
title: PV
---

# PV

## Global Photovoltaic Sector Overview

Over the preceding two decades, the global photovoltaic (PV) sector has
witnessed a profound escalation in capacity. Commencing from a modest
1,790 MW in 2001, it expanded to an impressive 584,000 MW by the end of
2019.[^1] This progression corresponds to an average annual growth rate
of approximately 40%. As of the onset of 2020, solar PVs contributed to
5.75% of the worldwide renewable electricity, representing a substantial
23% of the aggregate installed renewable energy capacity. Notably,
grid-connected PV systems dominate the market, accounting for over 99%
of the share, leaving off-grid systems, once a majority, now
representing a marginal 0.7%.

## Performance Metrics and Cost Implications

The efficiency of PV modules, as of recent 2020 data, reached
approximately 17%. However, advanCement Prod.s in multi-junction cell
technology have reported efficiencies exceeding 45%, although their
widespread implementation remains consElectric Trained due to elevated
production costs. From an economic perspective, initial capital outlay
remains the predominant deterrent to the sector’s growth. Despite this,
a downward trajectory in costs has been observed over recent years. In a
comparative analysis with alternative energy sources in Quebec, solar
remains less competitive than wind and hydroelectric
modalities. Nevertheless, projections indicate potential parity with
HydroQuébec’s residential rates within the forthcoming decade. Regarding
solar irradiance, Quebec registers an annual mean value ranging from
1,000 kWh/m^2^ to 1,350 kWh/m^2^.

## Comparative Analysis: Solar Capacity by Nation

In the context of 2018, China emerged as the foremost player in global
solar installations, commanding a capacity of 131 GW. Subsequent nations
in terms of capacity include the USA (51 GW), Japan (49 GW), and Germany
(42 GW). Within Canada, a cumulative output of 2.9 GW has been
documented, primarily attributed to initiatives in Ontario.[^2]

Evolution of PV production in Canada

The Electricity generation from solar technologies, goes from 572 GWh
produced in 2011 to to 4846 GWh in 2020.

```python exec="true" html="true"
import pandas as pd
import plotly.express as px

# Create the data frame
years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
generation = [572, 881, 1499, 2120, 2895, 4030, 3573, 3796, 4079, 4846]
data = pd.DataFrame({'years': years, 'generation': generation})

# Create the bar plot
fig = px.bar(
    data,
    x='years',
    y='generation',
    title="Solar Electricity Generation in Canada",
    labels={'years': 'Year', 'generation': 'Electricity Generation (GWh)'},
    text='generation'
)

# Customize the layout
fig.update_traces(marker_color='#FFD700', textposition='outside')
fig.update_layout(
    xaxis=dict(type='category', title='Year'),
    yaxis=dict(title='Electricity Generation (GWh)'),
    template='plotly_white'
)

print(fig.to_html(full_html=False, include_plotlyjs="cdn"))
```

Source: [https://www.irena.org/Energy-Transition/Technology/Solar-energy](https://www.irena.org/Energy-Transition/Technology/Solar-energy)

## Analyzing the Solar PV Potential

Exploiting solar energy has inherent variabilities, largely attributed
to diurnal cycles, meteorological conditions, and seasonal changes.
Within the context of Quebec, the intermittent nature of solar
insolation presents unique challenges for grid-integrated PV systems.
Studies indicate that the annual use factor of such systems in southern
Quebec approximates 16-17%. Intriguingly, this surpasses the figures
reported from established solar energy producers, including Germany and
Japan. Quebec’s northern latitude means it receives less solar radiation
compared to countries closer to the equator. However, the province’s
vast area offers significant potential for large-scale solar farms.

### Residential Potential[^4]

For Quebec, with a mean daily insolation of 4.33 kWh/m^2^ for latitude tilt:

* Ground Floor Area: 172 km^2^
* Yearly Electricity Production: 11 TWh
* Yearly Electricity Use: 37.8 TWh
* Electricity Production/Use: 29%
* GHG emissions intensity: 0.0088 kg/kWh
* Yearly GHG emissions reductions: 0.095 Megatonnes

### Commercial and Institutional Potential[^4]

For Quebec, with a mean daily insolation of 4.33 kWh/m^2^ for latitude tilt:

+ Ground Floor Area: 44.6 km^2^
+ Yearly Electricity Production: 3.8 TWh
+ Yearly Electricity Use: 35 TWh
+ Electricity Production/Use: 11%
+ GHG emissions intensity: 0.0088 kg/kWh
+ Yearly GHG emissionsreductions: 0.033 Megatonnes

These figures indicate that building-integrated photovoltaics (BIPV) have a
significant potential in Quebec, both in the residential and commercial
sectors, contributing to a substantial reduction in greenhouse gas
emissions.

In particular, areas in southern Quebec receive sufficient sunlight to
make PV installations economically viable, especially during the summer
months. According to HydroQuébec[^3] the south of the province receives
around 1200 \[kWh/kW\] in one year.
The potential of urban rooftops in cities like Montreal can also
contribute significantly to the province’s solar production.

## Monthly production

Quebec’s solar energy production varies seasonally, with longer daylight
hours in the summer contributing to higher outputs. The winter months,
with shorter days and potential snow cover, can reduce the efficiency of
PV installations.

```python exec="true" html="true"
import pandas as pd
import plotly.express as px

# Data
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
c_p_t = [0.101, 0.141, 0.168, 0.160, 0.157, 0.155, 0.157, 0.151, 0.130, 0.103, 0.076, 0.080]
df = pd.DataFrame({'Month': months, 'Capacity Factor': c_p_t})

# Create the bar plot
fig = px.bar(
    df, 
    x='Month', 
    y='Capacity Factor', 
    title="Monthly Capacity Factor of PV for Quebec Province", 
    labels={'Month': 'Month', 'Capacity Factor': 'Capacity Factor'},
    text='Capacity Factor'
)

# Customize the layout
fig.update_traces(marker_color='#FFD700', textposition='outside')
fig.update_layout(
    xaxis=dict(title='Month', tickangle=45),
    yaxis=dict(title='Capacity Factor'),
    template='plotly_white'
)

print(fig.to_html(full_html=False, include_plotlyjs="cdn"))
```

## Parameters

This section presents all the parameters used for the **PV** in the ES
model, including the raw data sources and necessary hypothesis, as
well as key calculation. It should be noticed that some parameters used
in the model are not deterministic, implying the necessity of taking
into consideration the uncertainty. The corresponding uncertainty range
for each parameter stems either from a broad literature review, or
denoted by expert assumptions (see the following parameters).

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_params(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PV'))
```

## References

```python exec="on"
from bibdatamanagement import *

print(MdDisplay.print_md_sources(bib_file_path='docs/assets/ES_Canada_3.bib', filter_entry='PV'))
```

[^1]: International Energy Agency (IEA).
2019. [Renewables 2019: Analysis and forecast 2024](https://www.iea.org/reports/renewables-2019).

[^2]: [HydroQuébec, L’ÉNERGIE SOLAIRE PHOTOVOLTAÏQUE](https://www.hydroquebec.com/data/developpement-durable/pdf/fiche-solaire-2021.pdf)

[^3]: L’énergie solaire photovoltaïque : est-ce rentable au Québec ? (2024, July 03). Retrieved
from [https://www.hydroquebec.com/solaire](https://www.hydroquebec.com/solaire)

[^4]: Pelland & Poissant.
2006. [An Evaluation of the Potential of Building Integrated Photovoltaics in Canada](https://ressources-naturelles.canada.ca/sites/www.nrcan.gc.ca/files/canmetenergy/files/pubs/2006-047_OP-J_411-SOLRES_BIPV_new.pdf):
