## import libraries
import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd

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

def summary():
    st.subheader("Data Summary:")
    st.write("Summary of coronavirus infection cases in Nigeria.")

    df = states_csv
    cases_no = df['CASES'].sum()
    active_no = df['ACTIVE'].sum()
    deaths_no = df['DEATHS'].sum()
    recovered_no = df['RECOVERED'].sum()

    st.markdown(
        """
        Total Confirmed Cases | Total Active Cases | Total Discharged | Total Deaths
        ----------------|--------------|------------|----------
        {0}             | {1}          | {2}        | {3} 
        """.format(cases_no, active_no, recovered_no, deaths_no)
    )
    st.text("")
    st.text("")

def table():
    ## sub header
    st.subheader("COVID-19 Cases by States:")

    # display table data
    st.table(states_csv[["STATE", "CASES", "DEATHS", "RECOVERED", "ACTIVE"]])

def map(sidebar_basemap_option):
    basemap = sidebar_basemap_option.lower()

    ## sub header
    st.subheader("COVID-19 Cases by States:")
    st.write("Total number of confirmed cases over time.")

    ## rename lat, long column names
    states_csv.rename(columns={'LAT':'lat', 'LONG':'lon'}, inplace=True)
    
    ## display map
    px.set_mapbox_access_token("pk.eyJ1Ijoia2FtcGFyaWEiLCJhIjoiY2s3OHMyaWlhMGk5azNsbnl3MnJweWdjYyJ9.4K1LcrByr-9dxInw2Iy7lw")
    fig = px.scatter_mapbox(states_csv, lat="lat", lon="lon", size="CASES", zoom=5)
    fig.update_layout(margin=dict(l=5, r=0, t=5, b=0), mapbox={'style':basemap})
    st.plotly_chart(fig)

def charts(sidebar_trend_option):
    if sidebar_trend_option == 'Cases':
        total_cases_overtime()
        new_cases_overtime()
    elif sidebar_trend_option == 'Deaths':
        total_deaths_overtime()
        new_deaths_overtime()
    elif sidebar_trend_option == 'Discharged':
        total_discharged_overtime()
        new_discharged_overtime()
    else:
        cases_overtime()
        new_records_overtime()
        cases_status_chart()

def cases_status_chart():
    st.subheader("Case By Status:")
    st.write("Status of total confirmed cases till date.")

    df = states_csv
    active_no = df['ACTIVE'].sum()
    deaths_no = df['DEATHS'].sum()
    recovered_no = df['RECOVERED'].sum()

    data = go.Pie(
        labels = ['ACTIVE', 'DEATHS', 'DISCHARGED'], 
        values = [active_no, deaths_no, recovered_no],
        hoverinfo='label+percent', 
        textinfo='value', 
        textfont=dict(size=20),
        marker=dict(colors = ['#636efa', '#ef553b', '#00cc96'], 
            line=dict(color='#FFF', width=1)
        )
    )

    fig = go.Figure(data = [data])
    fig.update_layout(legend_orientation='h', margin=dict(l=5, r=0, t=5, b=0))
    st.plotly_chart(fig)

## cases over time chart
def cases_overtime():
    st.subheader("Daily Totals:")
    st.write("Total numbers of cases, discharges and deaths.")
    df = dailyupdates_csv
    confirmed = go.Line(x = pd.to_datetime(df['DATE']), y = df['TOTAL CONFIRMED'], name = 'TOTAL CONFIRMED CASES')
    recovered = go.Line(x = pd.to_datetime(df['DATE']), y = df['RECOVERED'], name = 'TOTAL DISCHARGED')
    deaths = go.Line( x = pd.to_datetime(df['DATE']), y = df['DEATHS'], name = 'TOTAL DEATHS')
    fig = go.Figure(data=[confirmed, deaths, recovered])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)

## cases over time chart
def new_records_overtime():
    st.subheader("Daily Changes:")
    st.write("Daily changes in numbers of cases, discharges and deaths.")
    df = dailyupdates_csv
    confirmed = go.Line(x = pd.to_datetime(df['DATE']), y = df['NEW CASES'], name = 'DAILY CONFIRMED CASES')
    recovered = go.Line(x = pd.to_datetime(df['DATE']), y = df['DAILY RECOVERED'], name = 'DAILY DISCHARGED')
    deaths = go.Line(x = pd.to_datetime(df['DATE']), y = df['DAILY DEATHS'], name = 'DAILY DEATHS')
    fig = go.Figure(data=[confirmed, deaths, recovered])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)

## total cases overtime charts
def total_cases_overtime():
    st.subheader("Total Confirmed Cases:")
    st.write("Total number of confirmed cases over time.")
    df = dailyupdates_csv
    data = go.Line(x = pd.to_datetime(df['DATE']), y = df['TOTAL CONFIRMED'], name = 'TOTAL CONFIRMED')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)

## total deaths overtime charts
def total_deaths_overtime():
    st.subheader("Total Deaths:")
    st.write("Total number of recorded deaths over time.")
    df = dailyupdates_csv
    data = go.Line(x = pd.to_datetime(df['DATE']), y = df['DEATHS'], name = 'TOTAL DEATHS')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)

## total discharged overtime charts
def total_discharged_overtime():
    st.subheader("Total Discharged:")
    st.write("Total number of discharged cases over time.")
    df = dailyupdates_csv
    data = go.Line(x = pd.to_datetime(df['DATE']), y = df['RECOVERED'], name = 'TOTAL DISCHARGED')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)

## new cases overtime charts
def new_cases_overtime():
    st.subheader("Daily Confirmed Cases:")
    st.write("Number of daily confirmed cases over time.")
    df = dailyupdates_csv.sort_values(by='DATE', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['DATE']), y = df['NEW CASES'], name = 'NEW CASES')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)

## new discharged over time
def new_discharged_overtime():
    st.subheader("Daily Discharged:")
    st.write("Number of daily discharged cases over time.")
    df = dailyupdates_csv.sort_values(by='DATE', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['DATE']), y = df['DAILY RECOVERED'], name = 'DAILY DISCHARGED')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)

## new deaths over time
def new_deaths_overtime():
    st.subheader("Daily Deaths:")
    st.write("Number of daily recorded deaths over time.")
    df = dailyupdates_csv.sort_values(by='DATE', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['DATE']), y = df['DAILY DEATHS'], name = 'DAILY DEATHS')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)