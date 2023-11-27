import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
from urllib.request import urlopen

# Set the page title
st.set_page_config(
    page_title="Drug Usage vs. Socioeconomic Factors",
    page_icon="📈",
    layout="centered",
)

# Load US counties information
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# fips to map county codes to location
fipsDF = pd.read_csv('data/WV FIPS.csv')
fips = fipsDF.loc[:, 'FIPS'].tolist()

# Since Drug Use will always be used, preload it in
drug_use_df = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Opioid Dispensing Rate per 100.csv')
drug_use_df['County'] = drug_use_df['County'].str.replace(' County', '', case=False)
drug_use_df['County'] = drug_use_df['County'].str.replace(', WV', '', case=False)


# maps metric name to a file name
fileDict = {
    'Drug Arrests':         "data/WV Drug Epidemic Dataset.xlsx - Drug Arrests (Raw).csv",
    'Poverty Rates':        "data/WV Drug Epidemic Dataset.xlsx - Poverty Rates (Percent).csv",
    'Unemployment Rates':   "data/WV Drug Epidemic Dataset.xlsx - Unemployment Rates (Percent).csv"
}

yearsDict = {
    'Drug Arrests':         ["1985", "2014"],
    'Poverty Rates':        ["1997", "2022"],
    'Unemployment Rates':   ["1990", "2022"]
}

# select box for metric
metric = st.selectbox(
    'Select metric to explore',
    ('Drug Arrests', 'Poverty Rates', 'Unemployment Rates'),
     index=0
)

# load secondary data
df = pd.read_csv(fileDict[metric])
# filter to just 55 counties
df = df.iloc[np.arange(len(fips))]
# Identify years for drug use data
drug_use_years = drug_use_df.columns[1:].sort_values(ascending=False).to_numpy().astype(int)

# get year data with slider
min_year = max(np.min(drug_use_years), int(yearsDict[metric][0]))
max_year = min(np.max(drug_use_years), int(yearsDict[metric][1]))
year_to_filter = str(st.slider('Year', min_year, max_year, max_year))

# clean df of second metric
df['County'] = df['County'].str.replace(' County', '', case=False)
# df[year_to_filter] = df[year_to_filter].astype(str)
# df[year_to_filter] = df[year_to_filter].str.replace(',', '', case=False).astype(float)
# Add FIPS
merged_df = df.merge(fipsDF, on='County', how='inner')

# per capita info
if metric == 'Drug Arrests':
    popDF = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Population.csv')
    # popDF = popDF.astype(str)
    # popDF[year_to_filter] = popDF[year_to_filter].str.replace(',', '', case=False).astype(float)
    merged_df[year_to_filter] = df[year_to_filter]/popDF[year_to_filter] * 100000 # Per 100,000 Transformation

# Function to categorize values into thirds (High, Medium, Low)
def categorize_thirds(value):
    if value <= min_value + third:
        return 1
    elif min_value + third < value <= min_value + 2 * third:
        return 2
    else:
        return 3

# Filter to just County columns and just needed year
merged_df = merged_df[['County',year_to_filter,'FIPS']]
drug_use_df = drug_use_df[['County',year_to_filter]]

# Create High, Med, Low Category for each
# merged_df
# Find the minimum and maximum values
min_value = merged_df[year_to_filter].min()
max_value = merged_df[year_to_filter].max()

# Calculate the range and thirds
value_range = max_value - min_value
third = value_range / 3

# Apply the function to create a new column
merged_df['Metric Rate Cat'] = merged_df[year_to_filter].apply(categorize_thirds)

# drug_use_df
# Find the minimum and maximum values
min_value = drug_use_df[year_to_filter].min()
max_value = drug_use_df[year_to_filter].max()

# Calculate the range and thirds
value_range = max_value - min_value
third = value_range / 3

# Apply the function to create a new column
drug_use_df['Drug Use Cat'] = drug_use_df[year_to_filter].apply(categorize_thirds)

# Define the replacements
replacement_dict_drug_use = {1: 'Low Opioid Dispensing', 2: 'Med Opioid Dispensing', 3: 'High Opioid Dispensing'}
replacement_dict_metric = {1: 'Low ' + metric, 2: 'Med ' + metric, 3: 'High ' + metric}

# Replace values in the specified column
drug_use_df['Drug Use Cat'] = drug_use_df['Drug Use Cat'].replace(replacement_dict_drug_use)
merged_df['Metric Rate Cat'] = merged_df['Metric Rate Cat'].replace(replacement_dict_metric)

# Combine the two together
merged_df['Bivariate'] = drug_use_df['Drug Use Cat'].astype(str)+ ', ' + merged_df['Metric Rate Cat'].astype(str) 

# Rename columns
merged_df = merged_df.rename(columns={year_to_filter: year_to_filter + 'Metric'})
drug_use_df = drug_use_df.rename(columns={year_to_filter: year_to_filter + 'Drug Use'})

final_df = merged_df.merge(drug_use_df, on='County', how='inner')
final_df = final_df.sort_values(by=[year_to_filter + 'Drug Use', year_to_filter + 'Metric'])

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

# Create choropleth map
fig = px.choropleth_mapbox(
    final_df,
    geojson=counties,  # Replace with your GeoJSON file
    locations='FIPS',
    color='Bivariate',
    color_continuous_scale=color_scale,
    center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
    opacity=0.75,
    hover_name = df['County'].tolist(),
    labels={year_to_filter: metric},
    mapbox_style="carto-positron",
    title='Bivariate Choropleth Map'
)

st.plotly_chart(fig, theme="streamlit")