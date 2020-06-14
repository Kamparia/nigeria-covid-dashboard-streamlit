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
states_geojson = data[5]

mapbox_access_token = "pk.eyJ1Ijoia2FtcGFyaWEiLCJhIjoiY2s3OHMyaWlhMGk5azNsbnl3MnJweWdjYyJ9.4K1LcrByr-9dxInw2Iy7lw"

def choropleth_map(data_class, sidebar_basemap_option):
    data_class = data_class.upper()

    ## basemap style
    if sidebar_basemap_option == "Default":
        basemap = "carto-positron"
    else:
        basemap = sidebar_basemap_option.lower()

    ## sub header
    st.subheader("Choropleth Map:")
    st.write("Total number of confirmed cases over time.")

    fig = px.choropleth_mapbox(states_csv, geojson=states_geojson, 
            locations="STATE", color=data_class, 
            range_color=(0, 1), featureidkey="properties.STATE",
            hover_name="STATE", hover_data=["CONFIRMED", "DEATHS", "DISCHARGED"],
            mapbox_style=basemap, zoom=5, center={"lat":9.114900, "lon":8.486995}, opacity=0.5
        )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
    st.plotly_chart(fig)


def point_size_map(data_class, sidebar_basemap_option):
    data_class = data_class.upper()

    ## basemap style
    if sidebar_basemap_option == "Default":
        basemap = "carto-positron"
    else:
        basemap = sidebar_basemap_option.lower()

    ## sub header
    st.subheader("Cases by State Map:")
    st.write("Total number of confirmed cases over time.")    

    ## display map
    px.set_mapbox_access_token(mapbox_access_token)
    fig = px.scatter_mapbox(states_csv, lat="lat", lon="lon", 
            size="CONFIRMED", mapbox_style=basemap, zoom=5, 
            center={"lat":9.114900, "lon":8.486995},
            hover_name="STATE", hover_data=["CONFIRMED", "DEATHS", "DISCHARGED"],
        )

    fig.update_layout(margin=dict(l=5, r=0, t=5, b=0))
    st.plotly_chart(fig)    


def get_color_scale_values(data_class):
    df = states_csv

    if data_class == "deaths":
        data_class = "DEATHS"
    elif data_class == "discharged":
        data_class == "DISCHARGED"
    else:
        data_class == "CONFIRMED"

    max_value = df[data_class].max()
    min_value = df[data_class].min()

