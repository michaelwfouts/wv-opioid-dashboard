import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from urllib.request import urlopen

# Set the page title
st.set_page_config(
    page_title="Drug Usage vs Life Expectancy",
    page_icon="🚧",
    layout="centered",
)


# # Load US counties information
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)

# # fips to map county codes to location
# fipsDF = pd.read_csv('data/WV FIPS.csv')
# fips = fipsDF.loc[:, 'FIPS'].tolist()

# # load data
# df = pd.read_csv("data/WV Drug Epidemic Dataset.xlsx - Life Expectancy.csv")
# df = df.iloc[np.arange(len(fips))]
# df2 = pd.read_csv("data/WV Drug Epidemic Dataset.xlsx - Drug Mortality (Per 100,000).csv")
# df2 = df2.iloc[np.arange(len(fips))]

# # national average lifespan data
# lifeExptDF = pd.read_csv("data/National Average Lifespan.csv")

# # get year data with slider
# year_to_filter = str(st.slider('Year', 2005, 2014, 2013))    # 2005 to 2014 for now

# # Create overall dataframes
# df['County'] = df['County'].str.replace(' County', '', case=False)
# df[year_to_filter] = df[year_to_filter].astype(str)
# df[year_to_filter] = df[year_to_filter].str.replace(',', '', case=False).astype(float)
# lifeExpectancy = lifeExptDF.loc[lifeExptDF['Year'] == year_to_filter, 'Expectancy']
# lifeExpectancy = lifeExpectancy[lifeExpectancy.keys()[0]]
# df[year_to_filter] = lifeExpectancy - df[year_to_filter]
# merged_df = df.merge(fipsDF, on='County', how='inner')

# df2['County'] = df2['County'].str.replace(' County', '', case=False)
# df2[year_to_filter] = df2[year_to_filter].astype(str)
# df2[year_to_filter] = df2[year_to_filter].str.replace(',', '', case=False).astype(float)
# merged_df2 = df2.merge(fipsDF, on='County', how='inner')

# fig = px.choropleth_mapbox(merged_df,
#                             geojson=counties,  # You can provide your own GeoJSON file or use px.data.gapminder()
#                             locations='FIPS',
#                             #featureidkey="properties.name",
#                             color=year_to_filter,
#                             color_continuous_scale=px.colors.sequential.Blues,
#                             hover_name=df['County'].tolist(),
#                             center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
#                             mapbox_style="carto-positron",
#                             title='Bivariate Choropleth Map',
#                             labels={'Variable1': 'Variable 1'},
#                             #template='plotly_dark',
#                             opacity=1)
# #fig.show()

# fig.add_trace(go.Choroplethmapbox(locations=fips,
#                                   geojson=counties,
#                                   z=merged_df2[year_to_filter].tolist(),
#                                   colorscale=px.colors.sequential.Reds,
#                                   marker_opacity=0.5,
#                                   marker_line_width=1))
# #fig.show()
# st.plotly_chart(fig, theme="streamlit")

# Define the content of the page
st.write("# Page Under Construction")
st.write("This page is currently under construction. Please check back later for updates.")