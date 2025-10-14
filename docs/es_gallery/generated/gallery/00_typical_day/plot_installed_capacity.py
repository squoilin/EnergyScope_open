# -*- coding: utf-8 -*-
"""
Installed  Capacity
===================================

This is a general example.
"""
#%% # This is a text block

import matplotlib.pyplot as plt
from energyscope.energyscope import Energyscope
from energyscope.models import infrastructure_ch_2050, Model
from energyscope.result import postprocessing

#%% Parameters
thresh = 1e-1
figsize = (10, 6)

#%%
# Create a model and calculate the results
es_infra_ch = Energyscope(model=infrastructure_ch_2050)
results_ch = es_infra_ch.calc()
results_ch = postprocessing(results_ch)

#%% Plot installed capacity
plt.figure(figsize=figsize)
F_Mult = results_ch.variables["F_Mult"]
F_mult = F_Mult[F_Mult.values[:,0]>thresh] # filter out values smaller than threshold
F_mult = F_mult.sort_values(by=F_Mult.columns[0], ascending=False) # sort by installed capacity

plt.bar(x=range(len(F_mult)),height=F_mult.values[:,0])
#plt.yscale('log')
plt.xticks(range(len(F_mult)), F_mult.index, rotation=90)

plt.ylabel('Installed capacity for Technologies [GW]\n and Storages [GWh]')
plt.xlim(-1, len(F_mult))
plt.ylim(0,20)
plt.show()