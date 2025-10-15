# -*- coding: utf-8 -*-
"""
Plotly example
===================================

This is an example using plotly.
"""
#%% # This is a text block

import plotly.express as px
import numpy as np
# mkdocs_gallery_thumbnail_path = '_static/newplot.png'
# The comment above is to set the thumbnail picture from a previously saved figure.
# This is required for plotly figures.



df = px.data.gapminder().query("year == 2007")

# Create a sunburst chart using Plotly
fig = px.sunburst(df, path=['continent', 'country'], values='pop',
                         color='lifeExp', hover_data=['iso_alpha'],
                         color_continuous_scale='RdBu',
                         color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))

#fig.update_layout(title_text='Life expectancy of countries and continents')
fig.show(renderer="notebook")