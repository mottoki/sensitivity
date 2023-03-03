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

# Column names
cinp = "Input"
clb = "Lower Bound"
cub = "Upper Bound"
cdelb = "Delta Lower Bound"
cdeub = "Delta Upper Bound"
cbase = "Base Value"

# -------------------- Input --------------------------------------------
st.header('TORNADO CHART')
# Base value
col1, col2 = st.columns([1,1], gap="medium")
with col1:
    sbase = st.number_input('Base value', value=1.2,
        min_value=0.0, step=0.1)
with col2:
    userfontsize = st.number_input('Font Size', value=35,
        min_value=1, step=1)
st.markdown("""------------------------""")
st.markdown("**Sensitivity Input**")
col1, col2, col3 = st.columns([1,1,1], gap="medium")
with col1:
    # Number of sensitivities
    num_inp = st.number_input('Number of sensitivity cases', value=1, min_value=1, step=1)
with col2:
    # Lower and Upper bound selection
    selection_bound = [f'{clb} + {cub}', f'{clb} only', f'{cub} only']
    selbound = st.selectbox('Bound selection', selection_bound)
with col3:
    # Reorder selection
    if selbound == selection_bound[0]:
        num_col = 3
        selection_order = [f'{clb}: smallest to largest value',
            f'{clb}: largest to smallest value',
            f'{cub}: largest to smallest value',
            f'{cub}: smallest to largest value']
        colorder = st.selectbox('Reorder chart by', selection_order)
        if colorder == selection_order[0]:
            colsel = cdelb
            asc = True
        elif colorder == selection_order[1]:
            colsel = cdelb
            asc = False
        elif colorder == selection_order[2]:
            colsel = cdeub
            asc = True
        else:
            colsel = cdeub
            asc = False
    elif selbound == selection_bound[1]:
        num_col = 2
        selection_order = [f'{clb}: smallest to largest value',
            f'{clb}: largest to smallest value']
        colorder = st.selectbox('Reorder tornado chart by', selection_order)
        if colorder == selection_order[0]:
            colsel = cdelb
            asc = True
        else:
            colsel = cdelb
            asc = False
    else:
        num_col = 2
        selection_order = [f'{cub}: largest to smallest value',
            f'{cub}: smallest to largest value']
        colorder = st.selectbox('Reorder tornado chart by', selection_order)
        if colorder == selection_order[0]:
            colsel = cdeub
            asc = True
        else:
            colsel = cdeub
            asc = False

# Initialise dataframe
if selbound == selection_bound[0]:
    df = pd.DataFrame(columns=[cinp, clb, cub, cbase, cdelb, cdeub])
elif selbound == selection_bound[1]:
    df = pd.DataFrame(columns=[cinp, clb, cbase, cdelb])
else:
    df = pd.DataFrame(columns=[cinp, cub, cbase, cdeub])

# Sensitivity Input
cols = st.columns(3, gap="medium")
for i in range(num_inp):
    k = 0
    with cols[k]:
        sname = st.text_input(f'{cinp} {i+1}', key=f'{cinp}_{i}', value=f'Sensitivity input {i+1}')
        k += 1
    if selbound != selection_bound[2]:
        with cols[k]:
            slow = st.number_input(f'{clb} {i+1}', value=1.0, key=f'{clb}_{i}',
                min_value=0.0, step=0.1)
            k += 1
    if selbound != selection_bound[1]:
        with cols[k]:
            supp = st.number_input(f'{cub} {i+1}', value=1.5, key=f'{cub}_{i}',
                min_value=0.0, step=0.1)
    # Calculate Delta & Create dataframe
    if selbound == selection_bound[0]:
        dellow = sbase - slow
        delupp = -(sbase - supp)
        df.loc[len(df)] = [sname, slow, supp, sbase, dellow, delupp]
    elif selbound == selection_bound[1]:
        dellow = sbase - slow
        df.loc[len(df)] = [sname, slow, sbase, dellow]
    else:
        delupp = -(sbase - supp)
        df.loc[len(df)] = [sname, supp, sbase, delupp]
# Reorder by lower bound values
df = df.reindex(df[colsel].abs().sort_values(ascending=asc).index)
st.markdown("""------------------------""")

# ---------------------- Figure ------------------------------------------
fig = go.Figure()
# Lower bound figure
if selbound != selection_bound[2]:
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
        hoverinfo='skip',
        # texttemplate = "%{x:,s}(M$) "
        ))
# Upper bound figure
if selbound != selection_bound[1]:
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
        hoverinfo='skip',
        # texttemplate = "%{x:,s}(M$) "
        ))
fig.update_layout(
    height=500,
    margin=dict(t=50,l=10,b=10,r=10),
    title_text="Tornado chart",
    title_font_family="sans-serif",
    #legend_title_text=’Financials’,
    title_font_size = 45,
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
        tickfont_size=userfontsize
        ),
    xaxis=dict(
        tickfont_size=userfontsize
        ),
    font=dict(size=userfontsize),
    bargap=0.30)

st.plotly_chart(fig, use_container_width=True, theme="streamlit")
