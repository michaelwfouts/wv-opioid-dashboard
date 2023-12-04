import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import math
from urllib.request import urlopen
import json

# ----------------------------------------
# PAGE LEVEL SETTINGS

# Set the page title
st.set_page_config(
    page_title="Industry vs Drug Usage",
    page_icon="🛠️",
    layout="centered",
)

# ----------------------------------------
# TITLE AND INTRO BLOCKS

# write a title
st.write("# Employment in Regional Industries vs. Opioid Dispensing Rate")

# make a divider
st.markdown("""---""")

# write a description
st.write("Some of the major industries in West Virginia (e.g., construction and extraction, forestry, etc.) are known to cause injuries to workers that are likely to be treated with opioid pain relievers. This led us to ask: Are the number of people employed in these industries correlated with opioid dispensing rates? With this visualization, we hope to provide some insight into this question by using a bivariate choropleth map to look at the relationship between the number of people employed in a chosen industry per 1000 jobs and the opioid dispensing rate per 100 people in each county. ")

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

#year_to_filter = "2020"
#industry_to_filter = "Farming, Fishing, and Forestry"

# read in data from the dataset
df_employ_const_ext = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs- Construction&Extraction .csv')
df_employ_farm_fish_forest = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Farm&Fish&Forest.csv')
df_employ_install_mainten_repair = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Install&Mainten&Repair.csv')
df_employ_prod = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Production.csv')
df_drug_usage = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Opioid Dispensing Rate per 100.csv')

# get a list of the counties
data_counties = df_employ_const_ext["County"]

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

# sort the FIPS codes so that it is in the same order as the counties alphabetically (McDowell County is out of place in orginial dataframe)
df_fips_sort = df_fips.sort_values('County')
data_fips_sort = df_fips_sort["FIPS"]
data_fips_sort = data_fips_sort.reset_index(drop=True)

# -------------------------------
# check for entries of 'na' in the data and convert data type to float

# for each county
for iCounty in range(55):

    # if the employment data is na
    if data_employ[iCounty] == 'na':
      
      # make it a nan
      data_employ[iCounty] = np.nan

    # convert str to float 
    data_employ[iCounty] = float(data_employ[iCounty])

# -------------------------------
# get the ranges for low, medium, and high employment

# get the interval to have 3 equal levels
interval = (np.nanmax(data_employ) - np.nanmin(data_employ))/3

# get the range for low employment
employ_range_low = [np.nanmin(data_employ), np.nanmin(data_employ)+interval]

# get the range for medium employment
employ_range_med = [np.nanmin(data_employ)+interval, np.nanmin(data_employ)+interval+interval]

# get the range for high employment
employ_range_high = [np.nanmin(data_employ)+interval+interval, np.nanmax(data_employ)]

# -------------------------------
# get the ranges for low, medium, and high drug usage

# get the interval to have 3 equal levels
interval = (np.nanmax(data_drug_usage) - np.nanmin(data_drug_usage))/3

# get the range for low drug usage
drug_usage_range_low = [np.nanmin(data_drug_usage), np.nanmin(data_drug_usage)+interval]

# get the range for medium drug usage
drug_usage_range_med = [np.nanmin(data_drug_usage)+interval, np.nanmin(data_drug_usage)+interval+interval]

# get the range for high drug usage
drug_usage_range_high = [np.nanmin(data_drug_usage)+interval+interval, np.nanmax(data_drug_usage)]

# -------------------------------
# get the bivariate category for each county

# define variables for categories
data_employ_level = np.empty(55, dtype="<U100")
data_drug_usage_level = np.empty(55, dtype="<U100")
data_bivariate = np.empty(55, dtype="<U100")

# for each county
for iCounty in range(55):

    # if employment is low and drug usage is low
    if (employ_range_low[0] <= data_employ[iCounty] < employ_range_low[1]) and (drug_usage_range_low[0] <= data_drug_usage[iCounty] < drug_usage_range_low[1]):
        data_employ_level[iCounty] = 'Low'
        data_drug_usage_level[iCounty] = 'Low'
        data_bivariate[iCounty] = 'Low Opioid Dispensing, Low Employment'

    # if employment is low and drug usage is medium
    elif (employ_range_low[0] <= data_employ[iCounty] < employ_range_low[1]) and (drug_usage_range_med[0] <= data_drug_usage[iCounty] < drug_usage_range_med[1]):
        data_employ_level[iCounty] = 'Low'
        data_drug_usage_level[iCounty] = 'Medium'
        data_bivariate[iCounty] = 'Medium Opioid Dispensing, Low Employment'

    # if employment is low and drug usage is high
    elif (employ_range_low[0] <= data_employ[iCounty] < employ_range_low[1]) and (drug_usage_range_high[0] <= data_drug_usage[iCounty] <= drug_usage_range_high[1]):
        data_employ_level[iCounty] = 'Low'
        data_drug_usage_level[iCounty] = 'High'
        data_bivariate[iCounty] = 'High Opioid Dispensing, Low Employment'

    # if employment is medium and drug usage is low
    elif (employ_range_med[0] <= data_employ[iCounty] < employ_range_med[1]) and (drug_usage_range_low[0] <= data_drug_usage[iCounty] < drug_usage_range_low[1]):
        data_employ_level[iCounty] = 'Medium'
        data_drug_usage_level[iCounty] = 'Low'
        data_bivariate[iCounty] = 'Low Opioid Dispensing, Medium Employment'

    # if employment is medium and drug usage is medium
    elif (employ_range_med[0] <= data_employ[iCounty] < employ_range_med[1]) and (drug_usage_range_med[0] <= data_drug_usage[iCounty] < drug_usage_range_med[1]):
        data_employ_level[iCounty] = 'Medium'
        data_drug_usage_level[iCounty] = 'Medium'
        data_bivariate[iCounty] = 'Medium Opioid Dispensing, Medium Employment'

    # if employment is medium and drug usage is high
    elif (employ_range_med[0] <= data_employ[iCounty] < employ_range_med[1]) and (drug_usage_range_high[0] <= data_drug_usage[iCounty] <= drug_usage_range_high[1]):
        data_employ_level[iCounty] = 'Medium'
        data_drug_usage_level[iCounty] = 'High'
        data_bivariate[iCounty] = 'High Opioid Dispensing, Medium Employment'

    # if employment is high and drug usage is low
    elif (employ_range_high[0] <= data_employ[iCounty] <= employ_range_high[1]) and (drug_usage_range_low[0] <= data_drug_usage[iCounty] < drug_usage_range_low[1]):
        data_employ_level[iCounty] = 'High'
        data_drug_usage_level[iCounty] = 'Low'
        data_bivariate[iCounty] = 'Low Opioid Dispensing, High Employment'

    # if employment is high and drug usage is medium
    elif (employ_range_high[0] <= data_employ[iCounty] <= employ_range_high[1]) and (drug_usage_range_med[0] <= data_drug_usage[iCounty] < drug_usage_range_med[1]):
        data_employ_level[iCounty] = 'High'
        data_drug_usage_level[iCounty] = 'Medium'
        data_bivariate[iCounty] = 'Medium Opioid Dispensing, High Employment'

    # if employment is high and drug usage is high
    elif (employ_range_high[0] <= data_employ[iCounty] <= employ_range_high[1]) and (drug_usage_range_high[0] <= data_drug_usage[iCounty] <= drug_usage_range_high[1]):
        data_employ_level[iCounty] = 'High'
        data_drug_usage_level[iCounty] = 'High'
        data_bivariate[iCounty] = 'High Opioid Dispensing, High Employment'

    # if employment is not available and drug usage is low
    elif np.isnan(data_employ[iCounty]) and (drug_usage_range_low[0] <= data_drug_usage[iCounty] < drug_usage_range_low[1]):
        data_employ_level[iCounty] = 'Not Available'
        data_drug_usage_level[iCounty] = 'Low'
        data_bivariate[iCounty] = 'Data Not Available'
        data_employ[iCounty] = 'na';

    # if employment is not available and drug usage is medium
    elif np.isnan(data_employ[iCounty]) and (drug_usage_range_med[0] <= data_drug_usage[iCounty] < drug_usage_range_med[1]):
        data_employ_level[iCounty] = 'Not Available'
        data_drug_usage_level[iCounty] = 'Medium'
        data_bivariate[iCounty] = 'Data Not Available'
        data_employ[iCounty] = 'na';

    # if employment is not available and drug usage is high
    elif np.isnan(data_employ[iCounty]) and (drug_usage_range_high[0] <= data_drug_usage[iCounty] < drug_usage_range_high[1]):
        data_employ_level[iCounty] = 'Not Available'
        data_drug_usage_level[iCounty] = 'High'
        data_bivariate[iCounty] = 'Data Not Available'
        data_employ[iCounty] = 'na';

    else:
        data_bivariate[iCounty] = 'Needs Fixed'

# -------------------------------
# plot

# make final dataframe
data = {'fips': data_fips_sort,
        'county': data_counties,
        'employment': data_employ,
        'employment_level': data_employ_level,
        'drug_usage': data_drug_usage,
        'drug_usage_level': data_drug_usage_level,
        'bivariate': data_bivariate}
df_final = pd.DataFrame(data)

# set the colors for the legends
biColorEmploy = {'Low Opioid Dispensing, Low Employment': '#FFFFFF', 'Low Opioid Dispensing, Medium Employment': '#FFC3C3', 'Low Opioid Dispensing, High Employment': '#FF7F7F',
                 'Medium Opioid Dispensing, Low Employment': '#C3C3C3', 'Medium Opioid Dispensing, Medium Employment': '#C38888', 'Medium Opioid Dispensing, High Employment': '#C34444',
                 'High Opioid Dispensing, Low Employment': '#7F7F7F', 'High Opioid Dispensing, Medium Employment': '#7F4444', 'High Opioid Dispensing, High Employment': '#7F0000',
                 'Data Not Available':'#E5D3B3','Needs Fixed':'#0000FF'}


Legend_Employ_Color = [
    [0.0, '#FFFFFF'], [0.125, '#FFC3C3'], [0.25, '#FF7F7F'],
    [0.375, '#C3C3C3'], [0.5, '#C38888'], [0.625, '#C34444'],
    [0.75, '#7F7F7F'], [0.875, '#7F4444'], [1.0, '#7F0000']
]

ChoroColorDict = {"Employment": biColorEmploy}
LegendColorDict = {"Employment": Legend_Employ_Color}

categoryOrderDict = {"Employment": ['Low Opioid Dispensing, Low Employment', 'Low Opioid Dispensing, Medium Employment', 'Low Opioid Dispensing, High Employment', 
                                    'Medium Opioid Dispensing, Low Employment', 'Medium Opioid Dispensing, Medium Employment', 'Medium Opioid Dispensing, High Employment', 
                                    'High Opioid Dispensing, Low Employment', 'High Opioid Dispensing, Medium Employment', 'High Opioid Dispensing, High Employment',
                                    'Data Not Available','Needs Fixed']}


# Define color scale
color_scale = [
    'rgb(255,0,0)',  # High Metric1, Low Metric2
    'rgb(255,165,0)',  # High Metric1, Medium Metric2
    'rgb(255,255,0)',  # High Metric1, High Metric2
    'rgb(0,128,0)',  # Medium Metric1, Low Metric2
    'rgb(173,216,230)',  # Medium Metric1, Medium Metric2
    'rgb(0,255,0)',  # Medium Metric1, High Metric2
    'rgb(0,0,255)',  # Low Metric1, Low Metric2
    'rgb(128,0,128)',  # Low Metric1, Medium Metric2
    'rgb(128,0,0)'  # Low Metric1, High Metric2
]


# create choropleth map
fig = px.choropleth_mapbox(
    df_final,
    geojson=counties,
    locations='fips',
    color='bivariate',
    color_discrete_map=ChoroColorDict["Employment"],
    center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
    opacity=1.0,
    category_orders={'bivariate': categoryOrderDict["Employment"]},
    mapbox_style="carto-positron",
    custom_data=['county',
                 'employment',
                 'employment_level',
                 'drug_usage',
                 'drug_usage_level']
)

fig.update_traces(hovertemplate='%{customdata[0]}<br><br>' + 
                                'Opioid Dispensing Rate Per 100 People: %{customdata[3]} (%{customdata[4]})<br>' +
                                'Employment per 1000 Jobs: %{customdata[1]} (%{customdata[2]})<br>')

fig.update_layout(
    hoverlabel=dict(
        align="left"
    )
)

# create the legend
legend = go.Heatmap(
    z=[[0.0, 0.125, 0.25], [0.375, 0.5, 0.625], [0.75, 0.875, 1.0]],
    x=["low", "medium", "high"],
    y=["low", "medium", "high"],
    showscale=False,
    colorscale=LegendColorDict["Employment"],
)

# Create a layout with a color axis for the legend
layout = go.Layout(
    title="Legend",
    height=300,
    width=270,
    xaxis=dict(title="Employment"),
    yaxis=dict(title="Opioid Dispensing Rate"),
    hovermode=False,
    coloraxis=dict(
        cmin=1,  # Set the minimum value
        cmax=9,  # Set the maximum value
        colorbar=dict(title="Legend Title")
    )
)
legend = go.Figure(data=[legend], layout=layout)
legend.update_traces(showlegend=False)
legend.update_xaxes(fixedrange=True)
legend.update_yaxes(fixedrange=True)
legend.update_layout(title_text='Legend', title_x=0.5)

# have legend next to figure
col1, col2 = st.columns([3, 4])
with col1:
    st.plotly_chart(legend, theme="streamlit")
with col2:
    st.plotly_chart(fig, theme="streamlit")



footer="Sources: Centers for Disease Control and Prevention (CDC), US Bureau of Labor Statistics, The Washington Post"
st.markdown(footer)
