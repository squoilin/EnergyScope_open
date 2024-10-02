import streamlit as st

from energyscope.energyscope import Energyscope
from energyscope.models import infrastructure_ch_2050, infrastructure_qc_2020, lca_ch_2050, lca_qc_2020
from energyscope.plots import plot_sankey
from energyscope.result import postprocessing
st.set_page_config(layout="wide")
st.header("Symposium Streamlit")

## Select and Load Model
models = {
    'Infrastructure Switzerland 2050': infrastructure_ch_2050,
    'Infrastructure Quebec 2020': infrastructure_qc_2020,
    'LCA Switzerland 2050': lca_ch_2050,
    'LCA Quebec 2020': lca_qc_2020,
}

option = st.selectbox('Which model do you want to use?', models.keys())

with st.status('Loading model...') as status:
    model = models[option]

    es_model = Energyscope(model=model)

    ## Single optimization
    # Solve the models
    status.update(label="Solving the model...")
    results = es_model.calc()

    # Postcompute KPIs
    status.update(label="Postprocessing results...")
    KPI = postprocessing(results)

    ## Sankey diagram
    status.update(label="Generating sankey...")
    # Generate the Sankey diagram using the processed results
    fig = plot_sankey(KPI)

    status.update(label="Solved", state="complete")

# Display the generated Sankey diagram in the output
fig
