import streamlit as st

from energyscope.datasets import parametrize_params
from energyscope.energyscope import Energyscope
from energyscope.models import infrastructure_ch_2050
from energyscope.plots import plot_sankey, plot_parametrisation, plot_comparison
from energyscope.result import postprocessing

st.header("Multirun: Parametrize Technology")

# Add input fields for the technology and min/max values
technology = st.text_input("Enter Technology", value="PV_LV")
col1, col2, col3 = st.columns(3)
with col1:
    min_val = st.number_input("Enter Minimal Capacity", min_value=0, value=0)
with col2:
    max_val = st.number_input("Enter Maximal Capacity", min_value=0, value=50)
with col3: # Number of runs input
    n_steps = st.number_input("Number of runs", min_value=1, max_value=10, step=1, value=6)


# Update the params list with the input values
params = [
    {'param': 'f_min', 'min_val': min_val, 'max_val': max_val, 'index0': technology},
    {'param': 'f_max', 'min_val': min_val, 'max_val': max_val, 'index0': technology}
]


# Your function call (assuming it's defined elsewhere in your code)
seq_data = parametrize_params(params=params, n_steps=n_steps)

# Display the generated sequence data (optional)
seq_data

es_model_ch = Energyscope(model=infrastructure_ch_2050)

# Run n optimizations based on parameter changed in seq_data
results_ch_n = es_model_ch.calc_sequence(seq_data)
# Postcompute KPIs
KPI_ch_n = postprocessing(results_ch_n)

"### Comparison"
col1, col2 = st.columns(2)
with col1:
    run1 = st.number_input("First run", min_value=1, max_value=n_steps, step=1, value=1)
with col2:
    run2 = st.number_input("Second run", min_value=1, max_value=n_steps, step=1, value=n_steps)

# %%
# Generate the Sankey diagram using the processed results
fig1 = plot_sankey(KPI_ch_n, run_id=run1)
fig2 = plot_sankey(KPI_ch_n, run_id=run2)

# Display the generated Sankey diagram in the output
f"#### Run {run1}"
fig1
f"#### Run {run2}"
fig2

# %%
# Select which results you want to display from the postprocessing dataframe df_annual and which aggregation you want (Category,Category_n, Sector)
st.plotly_chart(plot_parametrisation(results=KPI_ch_n, variable="Annual_Prod", category="Sector",
                                      labels={'Annual_Prod': 'Annual Production  [GWh]'}))

st.plotly_chart(plot_comparison(results=results_ch_n, variable='C_inv_an', category='Sector',
                                run1=run1, run2=run2, 
                                labels={'C_inv_an': 'Annual Investment Costs [MCHF]'}))

st.plotly_chart(plot_comparison(results=results_ch_n, variable='Annual_Prod', category='Category_2',
                                run1=run1, run2=run2,
                                labels={'Annual_Prod': 'Annual Production'}))
