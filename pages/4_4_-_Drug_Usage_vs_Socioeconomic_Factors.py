import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
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
replacement_dict_drug_use = {1: 'Low Opioid', 2: 'Med Opioid', 3: 'High Opioid'}
#replacement_dict_metric = {1: 'Low ' + metric, 2: 'Med ' + metric, 3: 'High ' + metric}

replacement_dict_Arrests =      {1: 'Low Arrests', 2: 'Med Arrests', 3: 'High Arrests'}
replacement_dict_Poverty =      {1: 'Low Poverty', 2: 'Med Poverty', 3: 'High Poverty'}
replacement_dict_Unemployment = {1: 'Low Unemployment', 2: 'Med Unemployment', 3: 'High Unemployment'}
replacement_dict_metric = {"Drug Arrests": replacement_dict_Arrests,
                           "Poverty Rates": replacement_dict_Poverty,
                           "Unemployment Rates": replacement_dict_Unemployment}

# Replace values in the specified column
drug_use_df['Drug Use Cat'] = drug_use_df['Drug Use Cat'].replace(replacement_dict_drug_use)
merged_df['Metric Rate Cat'] = merged_df['Metric Rate Cat'].replace(replacement_dict_metric[metric])

# Combine the two together
merged_df['Bivariate'] = drug_use_df['Drug Use Cat'].astype(str)+ ', ' + merged_df['Metric Rate Cat'].astype(str) 

# Rename columns
merged_df = merged_df.rename(columns={year_to_filter: year_to_filter + 'Metric'})
drug_use_df = drug_use_df.rename(columns={year_to_filter: year_to_filter + 'Drug Use'})

final_df = merged_df.merge(drug_use_df, on='County', how='inner')
final_df = final_df.sort_values(by=[year_to_filter + 'Drug Use', year_to_filter + 'Metric'])

# Red (Drug Arrests)          # FFFFFF  FF8888  FF0000
# Black (opiod dispensing)    # FFFFFF  888888  000000
biColorDrugArrests = {'Low Opioid, Low Arrests': '#FFFFFF', 'Low Opioid, Med Arrests': '#FFC3C3', 'Low Opioid, High Arrests': '#FF7F7F',
                      'Med Opioid, Low Arrests': '#C3C3C3', 'Med Opioid, Med Arrests': '#C38888', 'Med Opioid, High Arrests': '#C34444',
                      'High Opioid, Low Arrests': '#7F7F7F', 'High Opioid, Med Arrests': '#7F4444', 'High Opioid, High Arrests': '#7F0000'}
Legend_DrugArrests_Color = [
    [0.0, '#FFFFFF'], [0.125, '#FFC3C3'], [0.25, '#FF7F7F'],
    [0.375, '#C3C3C3'], [0.5, '#C38888'], [0.625, '#C34444'],
    [0.75, '#7F7F7F'], [0.875, '#7F4444'], [1.0, '#7F0000']
]

# Green (Poverty)             # FFFFFF  887F88  00FF00
# Black (opiod dispensing)    # FFFFFF  888888  000000
biColorPoverty =     {'Low Opioid, Low Poverty': '#FFFFFF', 'Low Opioid, Med Poverty': '#C3FFC3', 'Low Opioid, High Poverty': '#7FFF7F',
                      'Med Opioid, Low Poverty': '#C3C3C3', 'Med Opioid, Med Poverty': '#88C388', 'Med Opioid, High Poverty': '#44C344',
                      'High Opioid, Low Poverty': '#7F7F7F', 'High Opioid, Med Poverty': '#447F44', 'High Opioid, High Poverty': '#007F00'}
Legend_Poverty_Color = [
    [0.0, '#FFFFFF'], [0.125, '#C3FFC3'], [0.25, '#7FFF7F'],
    [0.375, '#C3C3C3'], [0.5, '#88C388'], [0.625, '#44C344'],
    [0.75, '#7F7F7F'], [0.875, '#447F44'], [1.0, '#007F00']
]

# Blue (Unemployment)         # FFFFFF  FF8888  FF0000
# Black (opiod dispensing)    # FFFFFF  888888  000000
biColorUnemployment ={'Low Opioid, Low Unemployment': '#FFFFFF', 'Low Opioid, Med Unemployment': '#C3C3FF', 'Low Opioid, High Unemployment': '#7F7FFF',
                      'Med Opioid, Low Unemployment': '#C3C3C3', 'Med Opioid, Med Unemployment': '#8888C3', 'Med Opioid, High Unemployment': '#4444C3',
                      'High Opioid, Low Unemployment': '#7F7F7F', 'High Opioid, Med Unemployment': '#44447F', 'High Opioid, High Unemployment': '#00007F'}
Legend_Unemployment_Color = [
    [0.0, '#FFFFFF'], [0.125, '#C3C3FF'], [0.25, '#7F7FFF'],
    [0.375, '#C3C3C3'], [0.5, '#8888C3'], [0.625, '#4444C3'],
    [0.75, '#7F7F7F'], [0.875, '#44447F'], [1.0, '#00007F']
]

ChoroColorDict = {"Drug Arrests": biColorDrugArrests,
                   "Poverty Rates": biColorPoverty,
                   "Unemployment Rates": biColorUnemployment}
LegendColorDict = {"Drug Arrests": Legend_DrugArrests_Color,
                   "Poverty Rates": Legend_Poverty_Color,
                   "Unemployment Rates": Legend_Unemployment_Color}

categoryOrderDict = {"Drug Arrests": ['Low Opioid, Low Arrests', 'Low Opioid, Med Arrests', 'Low Opioid, High Arrests', 
                                      'Med Opioid, Low Arrests', 'Med Opioid, Med Arrests', 'Med Opioid, High Arrests', 
                                      'High Opioid, Low Arrests', 'High Opioid, Med Arrests', 'High Opioid, High Arrests'],
                     "Poverty Rates": ['Low Opioid, Low Poverty', 'Low Opioid, Med Poverty', 'Low Opioid, High Poverty', 
                                       'Med Opioid, Low Poverty', 'Med Opioid, Med Poverty', 'Med Opioid, High Poverty', 
                                       'High Opioid, Low Poverty', 'High Opioid, Med Poverty', 'High Opioid, High Poverty'],
                     "Unemployment Rates": ['Low Opioid, Low Unemployment', 'Low Opioid, Med Unemployment', 'Low Opioid, High Unemployment', 
                                       'Med Opioid, Low Unemployment', 'Med Opioid, Med Unemployment', 'Med Opioid, High Unemployment', 
                                       'High Opioid, Low Unemployment', 'High Opioid, Med Unemployment', 'High Opioid, High Unemployment']}

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
    #color_continuous_scale=color_scale,
    color_discrete_map=ChoroColorDict[metric],
    center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
    opacity=1.0,
    # hover_name = final_df['County'].tolist(),
    # labels={year_to_filter: metric},
    category_orders={'Bivariate': categoryOrderDict[metric]},
    mapbox_style="carto-positron",
    title='Opiod Dispensing vs. ' + metric,
    custom_data=['County', 
                 'Drug Use Cat', 
                 'Metric Rate Cat', 
                 year_to_filter + 'Metric',
                 year_to_filter + 'Drug Use']
)


fig.update_traces(hovertemplate='County: %{customdata[0]}<br><br>' + 
                                'Opioid Dispensing: %{customdata[4]:.1f} (%{customdata[1]})<br>' +
                                 metric + ': %{customdata[3]:.1f} (%{customdata[2]})')

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
    colorscale=LegendColorDict[metric],
)

# Create a layout with a color axis for the legend
layout = go.Layout(
    title="Legend",
    height=300,
    width=270,
    xaxis=dict(title="Difference in life expectancy"),
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

# fig.update_layout(legend_title_text='Combined Categorical Metrics')

# st.plotly_chart(fig, theme="streamlit")

footer="Sources: Centers for Disease Control and Prevention (CDC), US Bureau of Labor Statistics, United States Census Bureau, US Department of Agriculture (USDA) Economic Research Service, IndexMundi, Inter-university Consortium for Political and Social Research (ICPSR)"
st.markdown(footer)