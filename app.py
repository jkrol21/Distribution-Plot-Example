import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.title("Distribution Plot Examples")

## Create a series of data for histogram
sel_1, sel_2, sel_3 = st.columns([5,5,1])
with sel_1:
    values_range = st.slider("Range of values", 0, 100, (0, 100))
    values_range = range(values_range[0], values_range[1])
with sel_2:
    n_observations = st.slider("Number of Observations", 1, 10000, 10)

with st.columns([1,10])[0]:
    n_bins = st.selectbox("Number of bins", list(range(1, 101)))

series_discrete = pd.Series(random.choices(values_range, k=n_observations))

col1, col2 = st.columns([1,1])
with col1:
    st.markdown("#### Plotly Histogram Function")
    fig = px.histogram(series_discrete, nbins=n_bins)
    fig.update_layout(
                dict(bargap=0.1, hovermode="x"),
                showlegend=False

            )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Equidistant Bin Intervals")

    min_value, max_value = series_discrete.min(), series_discrete.max()
    interval_length = (max_value - min_value) / n_bins
    bin_cutoffs = [min_value + (i * interval_length) for i in range(n_bins)] + [max_value * 1.00001]
    discrete_dist = series_discrete.reset_index().rename(columns={"index": "value"})
    discrete_dist["n"] = 1
    discrete_dist["bin"] = pd.cut(series_discrete, bin_cutoffs, right=False, precision=2)

    # count occurrences of each bin
    discrete_dist = discrete_dist.groupby("bin").agg({'n': 'sum'}).reset_index()
    discrete_dist["bin"] = discrete_dist["bin"].astype("str")
    fig = px.bar(discrete_dist,
                 x="bin",
                 y='n',
                 )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")

    st.plotly_chart(fig, use_container_width=True)
