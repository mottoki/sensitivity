import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

# ----------------- CONFIG -------------------------------------------
st.set_page_config(page_title='Sensitivity', page_icon=None, layout="wide")

hide_table_row_index = """
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

st.markdown(hide_table_row_index, unsafe_allow_html=True)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Input
st.subheader('TORNADO CHART')
sbase = st.number_input('Base value', value=1.2,
    min_value=0.0, max_value=10.0, step=0.1)
# col1, col2 = st.columns([1,2], gap="medium")
# with col1:
#     st.subheader('Sensitivity Inputs')
# with col2:
st.markdown("""------------------------""")
num_inp = st.number_input('Number of sensitivity cases', value=1, min_value=1, step=1)

col1, col2, col3 = st.columns(3, gap="medium")
cinp = "Input"
clb = "Lower Bound"
cub = "Upper Bound"
cdelb = "Delta Lower Bound"
cdeub = "Delta Upper Bound"
cbase = "Base value"
df = pd.DataFrame(columns=[cinp, clb, cub, cbase, cdelb, cdeub])
for i in range(num_inp):
    with col1:
        sname = st.text_input(f'{cinp} {i+1}', key=f'{cinp}_{i}', placeholder='e.g. Groundwater')
    with col2:
        slow = st.number_input(f'{clb} {i+1}', value=1.0, key=f'{clb}_{i}',
            min_value=0.0, max_value=10.0, step=0.1)
    with col3:
        supp = st.number_input(f'{cub} {i+1}', value=1.5, key=f'{cub}_{i}',
            min_value=0.0, max_value=10.0, step=0.1)
    # Calculate Delta
    dellow = sbase - slow
    delupp = -(sbase - supp)
    # Create dataframe
    df.loc[len(df)] = [sname, slow, supp, sbase, dellow, delupp]
# Reorder by lower bound values
df = df.reindex(df[cdelb].abs().sort_values().index)
# Figure
fig = go.Figure()
fig.add_trace(go.Bar(y=df[cinp], x=[-x for x in df[cdelb]],
                base=[x for x in df[cbase]],
                marker_color='crimson',
                name=clb,
                marker_line_color='red',
                orientation='h',
                marker_line_width=1.5,
                opacity= 0.7,
                text = [x for x in df[clb]],
                textposition='auto',
                # texttemplate = "%{x:,s}(M$) "
))
fig.add_trace(go.Bar(y=df[cinp], x=[x for x in df[cdeub]],
                base=[x for x in df[cbase]],
                marker_color='rgb(158,202,225)',
                name=cub,
                marker_line_color='rgb(8,48,107)',
                orientation='h',
                marker_line_width=1.5,
                opacity= 0.7,
                text = [x for x in df[cub]],
                textposition='auto',
                # texttemplate = "%{x:,s}(M$) "
))
fig.update_layout(
    height=500,
    margin=dict(t=50,l=10,b=10,r=10),
    title_text="Tornado chart",
    title_font_family="sans-serif",
    #legend_title_text=’Financials’,
    title_font_size = 35,
    title_font_color="darkblue",
    title_x=0.5 #to adjust the position along x-axis of the title
)
fig.update_layout(
    barmode='overlay',
    # xaxis_tickangle=-45,
    # legend=dict(
    #     x=0.80,
    #     y=0.01,
    #     bgcolor='rgba(255, 255, 255, 0)',
    #     bordercolor='rgba(255, 255, 255, 0)'
    #     ),
    yaxis=dict(
        # title='Input',
        # titlefont_size=18,
        tickfont_size=18
        ),
    xaxis=dict(
        tickfont_size=18
        ),
    font=dict(
        size=18),
    bargap=0.30)
# fig =  go.Figure()
# fig.add_trace(go.Bar(
#     x=df[clb],
#     y=df[cinp],
#     base=[x for x in df[cbase]],
#     orientation='h',
#     # hoverinfo='skip',
#     ))

# fig.add_trace(go.Bar(
#     x=df[cdeub],
#     y=df[cinp],
#     base=df[cbase],
#     orientation='h',
#     marker=dict(
#         color="rgba(21,  162,  91,  1)"),
#     hoverinfo='skip',
#     ))
# fig.update_layout(
#     title=dict(text="Tornado Chart"),
#     width=862,
#     height=680,
#     barmode="stack",
#     autosize=True,
#     showlegend=False,
#     )
# fig.update_yaxes(
#     autorange="reversed")

# fig.update_xaxes(
#     title_text = "Factor of Safety",
#     title_standoff = 10)

st.plotly_chart(fig, use_container_width=True, theme="streamlit")
