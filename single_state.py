## import libraries
import streamlit as st
import numpy as np
import pandas as pd

import plotly
import plotly.graph_objects as go
import plotly.express as px

from load_data import load_data

## load data
data = load_data()
states_csv = data[0]
dailyupdates_csv = data[1]
states_daily_cases_csv = data[2]
states_daily_deaths_csv = data[3]
states_daily_recovered_csv = data[4]
states_geojson = data[5]

def fetch_state_charts(state):
    st.subheader(state + " Data:")
    summary_chart(state)
    infections_chart(state)
    recovered_chart(state)
    deaths_chart(state)
 
def summary_chart(state):
    pass

def infections_chart(state):
    ## daily infections
    df = states_daily_cases_csv.sort_values(by='Date', ascending=False)
    data = go.Bar(
        x = pd.to_datetime(df['Date']),
        y = df[state],
        name = state
    )
    fig = go.Figure(data=[data])
    fig.update_layout(title_text="Total Infections:")
    st.plotly_chart(fig)

def recovered_chart(state):
    ## daily recovered
    df = states_daily_recovered_csv.sort_values(by='Date', ascending=False)
    data = go.Bar(
        x = pd.to_datetime(df['Date']),
        y = df[state],
        name = state
    )
    fig = go.Figure(data=[data])
    fig.update_layout(title_text="Total Recovered:")
    st.plotly_chart(fig)

def deaths_chart(state):
    ## daily deaths
    df = states_daily_deaths_csv.sort_values(by='Date', ascending=False)
    data = go.Bar(
        x = pd.to_datetime(df['Date']),
        y = df[state],
        name = state
    )
    fig = go.Figure(data=[data])
    fig.update_layout(title_text="Total Deaths:")
    st.plotly_chart(fig)