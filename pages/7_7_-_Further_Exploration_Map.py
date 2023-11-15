import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
from urllib.request import urlopen

st.set_page_config(
    page_title="Exploration Map",
    page_icon="🗺️",
)

# if st.checkbox('Show WV FIPS'):
#     st.subheader('FIPS')
#     st.write(df1)

# Load US counties information
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# fips to map county codes to location
fipsDF = pd.read_csv('data/WV FIPS.csv')
fips = fipsDF.loc[:, 'FIPS'].tolist()

# different color scales for different metrics
colorDict = {
    'Drug Arrests':         px.colors.sequential.Reds,
    'Drug Mortality':       px.colors.sequential.Oranges,
    'Illicit Drug Use':     px.colors.sequential.Greens,
    'Life Expectancy':      px.colors.sequential.Blues,
    'Population':           px.colors.sequential.Purples,
    'Poverty Rates':        px.colors.sequential.Teal,
    'Unemployment Rates':   px.colors.sequential.Greys
}

# maps metric name to a file name
fileDict = {
    'Drug Arrests':         "data/WV Drug Epidemic Dataset.xlsx - Drug Arrests (Raw).csv",
    'Drug Mortality':       "data/WV Drug Epidemic Dataset.xlsx - Drug Mortality (Per 100,000).csv",
    'Illicit Drug Use':     "data/WV Drug Epidemic Dataset.xlsx - Illicit Drug Past Mo (Percent).csv",
    'Life Expectancy':      "data/WV Drug Epidemic Dataset.xlsx - Life Expectancy.csv",
    'Population':           "data/WV Drug Epidemic Dataset.xlsx - Population.csv",
    'Poverty Rates':        "data/WV Drug Epidemic Dataset.xlsx - Poverty Rates (Percent).csv",
    'Unemployment Rates':   "data/WV Drug Epidemic Dataset.xlsx - Unemployment Rates (Percent).csv"
}

yearsDict = {
    'Drug Arrests':         ["1985", "2014"],
    'Drug Mortality':       ["1980", "2021"],
    'Illicit Drug Use':     ["2002", "2014"],
    'Life Expectancy':      ["1980", "2022"],
    'Population':           ["1970", "2022"],
    'Poverty Rates':        "data/WV Drug Epidemic Dataset.xlsx - Poverty Rates (Percent).csv",
    'Unemployment Rates':   "data/WV Drug Epidemic Dataset.xlsx - Unemployment Rates (Percent).csv"
}

# select box for metric
metric = st.selectbox(
    'Select metric to explore',
    ('Drug Arrests', 'Drug Mortality', 'Life Expectancy',
     'Population', 'Poverty Rates', 'Unemployment Rates'),
     index=0
)

# load data
df = pd.read_csv(fileDict[metric])
df = df.iloc[np.arange(len(fips))]
popDF = pd.read_csv(fileDict['Population'])
years = df.columns[1:].sort_values(ascending=False).to_numpy()

# get year data with slider
year_to_filter = str(st.slider('Year', 2005, int(years.max()), int(years.max()))) # 2005 to max year

# Create overall dataframe
df['County'] = df['County'].str.replace(' County', '', case=False)
df[year_to_filter] = df[year_to_filter].astype(str)
df[year_to_filter] = df[year_to_filter].str.replace(',', '', case=False).astype(float)
merged_df = df.merge(fipsDF, on='County', how='inner')

# per capita info
if metric == 'Drug Arrests':
    popDF = popDF.astype(str)
    popDF[year_to_filter] = popDF[year_to_filter].str.replace(',', '', case=False).astype(float)
    merged_df[year_to_filter] = df[year_to_filter]/popDF[year_to_filter] * 100000

# create map figure
fig = px.choropleth_mapbox(merged_df, 
                           geojson=counties, 
                           locations='FIPS', 
                           color=year_to_filter,
                           color_continuous_scale=colorDict[metric],
                           center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
                           opacity=0.75,
                           hover_name = df['County'].tolist(),
                           labels={year_to_filter: metric},
                           mapbox_style="carto-positron")

st.plotly_chart(fig, theme="streamlit")