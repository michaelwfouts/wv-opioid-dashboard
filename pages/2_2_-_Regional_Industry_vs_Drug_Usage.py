import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import math
from urllib.request import urlopen
import json

# Set the page title
st.set_page_config(
    page_title="Industry vs Drug Usage",
    page_icon="🚧",
    layout="centered",
)

# ----------------------------------------
# TITLE AND INTRO BLOCKS

# write a title
st.write("# Employment in Regional Industries vs. Opioid Dispensing Rate")

# make a divider
st.markdown("""---""")

# write a description
st.write("Description goes here")

# make a divider
st.markdown("""---""")

# ----------------------------------------
# PARAMETER SELECTION BLOCK

# write a header for the block
st.write("Which year and industry are you interested in?")

# make a dropdown menu to select year
year_to_filter = st.selectbox(
    'Select Year:',
    ["2019", "2020"]
)

# make a dropdown menu to select industry
industry_to_filter = st.selectbox(
    'Select Industry:',
    ["Construction and Extraction", "Farming, Fishing, and Forestry", "Installation, Maintenance, and Repair", "Production"]
)

# read in data from the dataset
df_employ_const_ext = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs- Construction&Extraction .csv')
df_employ_farm_fish_forest = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Farm&Fish&Forest.csv')
df_employ_install_mainten_repair = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Install&Mainten&Repair.csv')
df_employ_prod = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Production.csv')
df_drug_usage = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Opioid Dispensing Rate per 100.csv')


# get pertinent info depending on selected year and industry
if year_to_filter == "2019" and industry_to_filter == "Construction and Extraction":
    data_employ = df_employ_const_ext["2019"].head(55)
    data_drug_usage = df_drug_usage["2019"].head(55)

elif year_to_filter == "2019" and industry_to_filter == "Farming, Fishing, and Forestry":
    data_employ = df_employ_farm_fish_forest["2019"].head(55)
    data_drug_usage = df_drug_usage["2019"].head(55)

elif year_to_filter == "2019" and industry_to_filter == "Installation, Maintenance, and Repair":
    data_employ = df_employ_install_mainten_repair["2019"].head(55)
    data_drug_usage = df_drug_usage["2019"].head(55)

elif year_to_filter == "2019" and industry_to_filter == "Production":
    data_employ = df_employ_prod["2019"].head(55)
    data_drug_usage = df_drug_usage["2019"].head(55)

elif year_to_filter == "2020" and industry_to_filter == "Construction and Extraction":
    data_employ = df_employ_const_ext["2020"].head(55)
    data_drug_usage = df_drug_usage["2020"].head(55)

elif year_to_filter == "2020" and industry_to_filter == "Farming, Fishing, and Forestry":
    data_employ = df_employ_farm_fish_forest["2020"].head(55)
    data_drug_usage = df_drug_usage["2020"].head(55)

elif year_to_filter == "2020" and industry_to_filter == "Installation, Maintenance, and Repair":
    data_employ = df_employ_install_mainten_repair["2020"].head(55)
    data_drug_usage = df_drug_usage["2020"].head(55)

else:
    data_employ = df_employ_prod["2020"].head(55)
    data_drug_usage = df_drug_usage["2020"].head(55)

# make a divider
st.markdown("""---""")

# ----------------------------------------------------------------------------------------------
# BIVARIATE CHLOROPLETH MAP BLOCK

# ultimately we need a dataframe that has columns for:
#   FIPS (codes)
#   bivariate results (low-low, low-medium, low-high
#                      medium-low, medium-medium, medium-high
#                      high-low, high-medium, high-high)

# -------------------------------
# get FIPS data

# read in US counties information
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# get a list of FIPS codes for WV counties
df_fips = pd.read_csv('data/WV FIPS.csv')
data_fips = df_fips["FIPS"]

# -------------------------------
# get the ranges for low, medium, and high employment

# get the interval to have 3 equal levels
interval = (max(data_employ) - min(data_employ))/3

# get the range for low employment
employ_range_low = [min(data_employ), min(data_employ)+interval]

# get the range for medium employment
employ_range_med = [min(data_employ)+interval, min(data_employ)+interval+interval]

# get the range for high employment
employ_range_high = [min(data_employ)+interval+interval, min(data_employ)+interval+interval+interval]

# -------------------------------
# get the ranges for low, medium, and high drug usage

# get the interval to have 3 equal levels
interval = (max(data_drug_usage) - min(data_drug_usage))/3

# get the range for low drug usage
drug_usage_range_low = [min(data_drug_usage), min(data_drug_usage)+interval]

# get the range for medium drug usage
drug_usage_range_med = [min(data_drug_usage)+interval, min(data_drug_usage)+interval+interval]

# get the range for high drug usage
drug_usage_range_high = [[min(data_drug_usage)+interval+interval, min(data_drug_usage)+interval+interval+interval]]

# -------------------------------
# get the bivariate category for each county

data_bivariate = np.zeros(55, dtype=int)

# for each county
for iCounty in range(55):

    # if employment is low and drug usage is low
    if (employ_range_low[0] <= data_employ[iCounty] < employ_range_low[1]) and (drug_usage_range_low[0] <= data_drug_usage[iCounty] < drug_usage_range_low[1]):
        data_bivariate[iCounty] = 11

    # if employment is low and drug usage is medium
    elif (employ_range_low[0] <= data_employ[iCounty] < employ_range_low[1]) and (drug_usage_range_med[0] <= data_drug_usage[iCounty] < drug_usage_range_med[1]):
        data_bivariate[iCounty] = 12

    # if employment is low and drug usage is high
    #elif (employ_range_low[0] <= data_employ[iCounty] < employ_range_low[1]) and (drug_usage_range_high[0] <= data_drug_usage[iCounty] <= drug_usage_range_high[1]):
        #data_bivariate[iCounty] = 13

    # if employment is medium and drug usage is low
    elif (employ_range_med[0] <= data_employ[iCounty] < employ_range_med[1]) and (drug_usage_range_low[0] <= data_drug_usage[iCounty] < drug_usage_range_low[1]):
        data_bivariate[iCounty] = 21

    # if employment is medium and drug usage is medium
    elif (employ_range_med[0] <= data_employ[iCounty] < employ_range_med[1]) and (drug_usage_range_med[0] <= data_drug_usage[iCounty] < drug_usage_range_med[1]):
        data_bivariate[iCounty] = 22

    # if employment is medium and drug usage is high
    #elif (employ_range_med[0] <= data_employ[iCounty] < employ_range_med[1]) and (drug_usage_range_high[0] <= data_drug_usage[iCounty] <= drug_usage_range_high[1]):
        #data_bivariate[iCounty] = 23

    # if employment is high and drug usage is low
    elif (employ_range_high[0] <= data_employ[iCounty] <= employ_range_high[1]) and (drug_usage_range_low[0] <= data_drug_usage[iCounty] < drug_usage_range_low[1]):
        data_bivariate[iCounty] = 31

    # if employment is high and drug usage is medium
    elif (employ_range_high[0] <= data_employ[iCounty] <= employ_range_high[1]) and (drug_usage_range_med[0] <= data_drug_usage[iCounty] < drug_usage_range_med[1]):
        data_bivariate[iCounty] = 32

    # if employment is high and drug usage is high
    #elif (employ_range_high[0] <= data_employ[iCounty] <= employ_range_high[1]) and (drug_usage_range_high[0] <= data_drug_usage[iCounty] <= drug_usage_range_high[1]):
        #data_bivariate[iCounty] = 33

    else:
        data_bivariate[iCounty] = 44

# -------------------------------
# plot

# make final dataframe
data = {'fips': data_fips,
        'bivariate': data_bivariate}
df_final = pd.DataFrame(data)

# create choropleth map
fig = px.choropleth_mapbox(
    df_final,
    geojson=counties,
    locations='fips',
    color='bivariate',
    color_continuous_scale="Viridis",
    center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
    opacity=0.75,
    mapbox_style="carto-positron",
    labels={'employment':'Num employed in chosen industry'}
)

st.plotly_chart(fig, theme="streamlit")





