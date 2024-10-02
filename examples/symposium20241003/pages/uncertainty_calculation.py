import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from energyscope.datasets import gen_sobol_sequence
from energyscope.energyscope import Energyscope
from energyscope.models import infrastructure_ch_2050
from energyscope.result import postprocessing

st.header("Uncertainty calculation")

#  Manual setting of the parameters 
"### Parameters"
"#### NEW_HYDRO_DAM"
new_hydro_dam_col1, new_hydro_dam_col2 = st.columns(2)
with new_hydro_dam_col1:
    new_hydro_dam_lower_bound = st.number_input("lower_bound", min_value=0.0, step=0.01, value=0.0,
                                                key="new_hydro_dam_lower_bound")
with new_hydro_dam_col2:
    new_hydro_dam_upper_bound = st.number_input("upper_bound", min_value=0.0, step=0.01, value=0.44,
                                                key="new_hydro_dam_upper_bound")

"#### NEW_HYDRO_RIVER"
new_hydro_river_col1, new_hydro_river_col2 = st.columns(2)
with new_hydro_river_col1:
    new_hydro_river_lower_bound = st.number_input("lower_bound", min_value=0.0, step=0.01, value=0.0,
                                                  key="new_hydro_river_lower_bound")
with new_hydro_river_col2:
    new_hydro_river_upper_bound = st.number_input("upper_bound", min_value=0.0, step=0.01, value=0.85,
                                                  key="new_hydro_river_upper_bound")

parameters = [
    {'name': 'NEW_HYDRO_DAM', 'lower_bound': new_hydro_dam_lower_bound, 'upper_bound': new_hydro_dam_upper_bound},
    {'name': 'NEW_HYDRO_RIVER', 'lower_bound': new_hydro_river_lower_bound, 'upper_bound': new_hydro_river_upper_bound},
]

seq, prob = gen_sobol_sequence(parameters=parameters, trajectories=2)

df = pd.DataFrame(seq, columns=prob['names']).T
df.columns = ['value' + str(x) for x in list(df.columns) if not str(x) == "nan"]
df = df.reset_index(names=['index0'])
df['param'] = 'c_inv'

df['index1'] = np.nan
df['index2'] = np.nan
df['index3'] = np.nan
df

## Setup runs
es_model_ch = Energyscope(model=infrastructure_ch_2050)
results_ch_n = es_model_ch.calc_sequence(df)

### Calculate KPIs
# Postcompute KPIs
KPI_ch_n = postprocessing(results_ch_n, df_monthly=True)

### Plot Parity
"### Infrastructure"
df_annual = KPI_ch_n.postprocessing['df_annual']
df_annual = df_annual.loc[:, ['F_Mult']]
df_annual = df_annual.reset_index()

df_annual = pd.pivot_table(df_annual, values='F_Mult', index=['Run'], columns='level_0')
df_annual.sample(5)
cols = ['PV_LV', 'WIND', 'NEW_HYDRO_DAM', 'NEW_HYDRO_RIVER']
fig = sns.pairplot(df_annual[cols].fillna(0)[cols], diag_kind="kde")
st.pyplot(fig)
