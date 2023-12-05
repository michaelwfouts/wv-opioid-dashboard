import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
from urllib.request import urlopen

st.set_page_config(
    page_title="Further Exploration Map",
    page_icon="🗺️",
)

# Visualization explanation
st.write("# Further Exploration Map")
st.markdown("""---""")
st.write("This visualization serves as a platform to explore each of the metrics in relation to the opioid epidemic. The goal is to allow you to take this research into your own hands by trying to answer questions the previous visualizations may have raised that you would like answered.")
st.markdown("""---""")

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
    'Drug Arrests (Per 1,000)':         px.colors.sequential.Reds,
    'Drug Mortality (Per 100,000)':       px.colors.sequential.Oranges,
    'Illicit Drug Use (Percent)':     px.colors.sequential.Greens,
    'Life Expectancy':      px.colors.sequential.Blues,
    'Population':           px.colors.sequential.Purples,
    'Poverty Rates (Percent)':        px.colors.sequential.Teal,
    'Unemployment Rates (Percent)':   px.colors.sequential.Greys,
    'Opioid Dispensing Rate (Per 100)':         px.colors.sequential.Reds,
    'Physician Ratio':       px.colors.sequential.Oranges,
    'Fish, Farms, and Forest Labor (Employment per 1,000 Jobs)':     px.colors.sequential.Greens,
    'Install, Maintenance, and Repair (Employment per 1,000 Jobs)':     px.colors.sequential.Oranges,
    'Production Labor (Employment per 1,000 Jobs)':     px.colors.sequential.Blues,
    'Construction and Extraction Labor (Employment per 1,000 Jobs)':     px.colors.sequential.Reds
}

# maps metric name to a file name
fileDict = {
    'Poverty Rates (Percent)':        "data/WV Drug Epidemic Dataset.xlsx - Poverty Rates (Percent).csv",
    'Drug Arrests (Per 1,000)':       "data/WV Drug Epidemic Dataset.xlsx - Drug Arrests (Per 1000).csv",
    'Drug Mortality (Per 100,000)':       "data/WV Drug Epidemic Dataset.xlsx - Drug Mortality (Per 100,000).csv",
    'Illicit Drug Use (Percent)':     "data/WV Drug Epidemic Dataset.xlsx - Illicit Drug Past Mo (Percent).csv",
    'Life Expectancy':      "data/WV Drug Epidemic Dataset.xlsx - Life Expectancy.csv",
    'Population':           "data/WV Drug Epidemic Dataset.xlsx - Population.csv",
    'Unemployment Rates (Percent)':   "data/WV Drug Epidemic Dataset.xlsx - Unemployment Rates (Percent).csv",
    'Opioid Dispensing Rate (Per 100)' : 'data\WV Drug Epidemic Dataset.xlsx - Opioid Dispensing Rate per 100.csv',
    'Physician Ratio' : 'data\WV Drug Epidemic Dataset.xlsx - Physicians Ratio (people_1 primary care physican)_numeric.csv',
    'Fish, Farms, and Forest Labor (Employment per 1,000 Jobs)':     'data\WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Farm&Fish&Forest.csv',
    'Install, Maintenance, and Repair (Employment per 1,000 Jobs)':     'data\WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Install&Mainten&Repair.csv',
    'Production Labor (Employment per 1,000 Jobs)':     'data\WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Production.csv',
    'Construction and Extraction Labor (Employment per 1,000 Jobs)':     'data\WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs- Construction&Extraction .csv'
}

# select box for metric
metric = st.selectbox(
    'Select metric to explore:',
    (fileDict.keys()),
     index=0
)

# load data
df = pd.read_csv(fileDict[metric])
df = df.iloc[np.arange(len(fips))]
popDF = pd.read_csv(fileDict['Population'])
years = df.columns[1:].sort_values(ascending=False).to_numpy()

if metric in ['Fish, Farms, and Forest Labor (Employment per 1,000 Jobs)', 'Install, Maintenance, and Repair (Employment per 1,000 Jobs)', 'Production Labor (Employment per 1,000 Jobs)', 'Construction and Extraction Labor (Employment per 1,000 Jobs)']:
    # If labor data, drop Area Column
    df = df.drop('Area', axis=1)

# get year data with slider
year_to_filter = str(st.selectbox("Select Year:", df.columns[1:].sort_values(ascending=False))) # 2005 to max year

# Create overall dataframe
df['County'] = df['County'].str.replace(' County', '', case=False)
df[year_to_filter] = df[year_to_filter].astype(str)
df[year_to_filter] = df[year_to_filter].str.replace(',', '', case=False).astype(float)
merged_df = df.merge(fipsDF, on='County', how='inner')

# per capita info
# if metric == 'Drug Arrests':
#     popDF = popDF.astype(str)
#     popDF[year_to_filter] = popDF[year_to_filter].str.replace(',', '', case=False).astype(float)
#     merged_df[year_to_filter] = df[year_to_filter]/popDF[year_to_filter] * 100000

# To not make the legend incredibly long
if metric in ['Fish, Farms, and Forest Labor (Employment per 1,000 Jobs)', 'Install, Maintenance, and Repair (Employment per 1,000 Jobs)', 'Production Labor (Employment per 1,000 Jobs)', 'Construction and Extraction Labor (Employment per 1,000 Jobs)']:
    legend_metric = 'Employment Per 1,000'
else: legend_metric = metric

# create map figure
fig = px.choropleth_mapbox(merged_df, 
                           geojson=counties, 
                           locations='FIPS', 
                           color=year_to_filter,
                           color_continuous_scale=colorDict[metric],
                           center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
                           opacity=0.75,
                           hover_name = df['County'].tolist(),
                           labels={year_to_filter: legend_metric},
                           mapbox_style="carto-positron",
                           custom_data=['County',
                                        year_to_filter])

fig.update_traces(hovertemplate='County: %{customdata[0]}<br><br>' + 
                                metric + ': %{customdata[1]:.2f}')

fig.update_layout(title_text=metric)

st.plotly_chart(fig, theme="streamlit")

footer="Sources: Centers for Disease Control and Prevention (CDC), US Bureau of Labor Statistics, United States Census Bureau, US Department of Agriculture (USDA) Economic Research Service, IndexMundi, Inter-university Consortium for Political and Social Research (ICPSR)"
st.markdown(footer)
