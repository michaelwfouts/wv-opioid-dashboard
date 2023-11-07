import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
from urllib.request import urlopen

st.set_page_config(
    page_title="Map",
    page_icon="👋",
)

# uploaded_file = st.file_uploader('data/WV FIPS.csv')
df1=pd.read_csv('data/WV FIPS.csv')

if st.checkbox('Show WV FIPS'):
    st.subheader('FIPS')
    st.write(df1)

# read geojson file containing WV map with county borders
f = open('data/WV_County_Boundaries.geojson')
counties = json.load(f)

# load population data
df = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Population.csv')
df = df.dropna()
df = df.loc[:, ['County', '2017']]

# load fips
fipsDF = pd.read_csv('data/WV FIPS.csv')

# Create overall dataframe
df['County'] = df['County'].str.replace(' County', '', case=False)
df['2017'] = df['2017'].str.replace(',', '', case=False).astype('float')
merged_df = df.merge(fipsDF, on='County', how='inner')

# Load US counties information
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
    
# create map figure
fig = px.choropleth_mapbox(merged_df, 
                           geojson=counties, 
                           locations='FIPS', 
                           color='2017',
                           color_continuous_scale="Viridis",
                           center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
                           opacity=0.75,
                           mapbox_style="carto-positron")

st.plotly_chart(fig)