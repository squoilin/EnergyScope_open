# -*- coding: utf-8 -*-
"""
Installed  Capacity
===================================

This is an example using the core model.
"""
#%% # This is a text block

import matplotlib.pyplot as plt
from energyscope.energyscope import Energyscope
from energyscope.models import core
#%% Parameters
thresh = 1
figsize = (10, 6)

#%%
# Create a model and calculate the results
es_core = Energyscope(model=core)
results = es_core.calc()

#%% Plot installed capacity
F = results.variables["F"]
storages = results.sets['STORAGE_TECH']["STORAGE_TECH"].values

F_storage = F[F.index.get_level_values(0).isin(storages)]
F_tech = F[~F.index.get_level_values(0).isin(storages)]

# Sort by size
F_storage = F_storage.sort_values(by=F_storage.columns[0], ascending=False)
F_storage = F_storage[F_storage.values[:,0]>thresh]
F_tech = F_tech[F_tech.values[:,0]>thresh]
F_tech = F_tech.sort_values(by=F_tech.columns[0], ascending=False)


# Calculate subplot widths proportional to number of bars
n_tech = len(F_tech)
n_storage = len(F_storage)
total = n_tech + n_storage
widths = [n_tech, n_storage] if total > 0 else [1, 1]

fig, axes = plt.subplots(1, 2, figsize=figsize, gridspec_kw={'width_ratios': widths})

# Technologies subplot (left)
axes[0].bar(x=range(n_tech), height=F_tech.values[:, 0])
axes[0].set_xticks(range(n_tech))
axes[0].set_xticklabels(F_tech.index, rotation=90)
axes[0].set_ylabel('Installed Capacity of Conversion Technologies [GW]')
axes[0].set_xlim(-1, n_tech)
axes[0].set_title('Conversion Technologies', fontsize=20)

# Storages subplot (right)
axes[1].bar(x=range(n_storage), height=F_storage.values[:, 0], color='orange')
axes[1].set_xticks(range(n_storage))
axes[1].set_xticklabels(F_storage.index, rotation=90)
axes[1].set_ylabel('Installed Capacity of Storages [GWh]')
axes[1].set_xlim(-1, n_storage)
axes[1].set_title('Storages', fontsize=20)

plt.tight_layout()
plt.show()