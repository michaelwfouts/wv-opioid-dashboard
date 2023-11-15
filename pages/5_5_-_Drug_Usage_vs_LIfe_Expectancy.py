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
    page_title="Under Construction",
    page_icon="🚧",
    layout="centered",
)


# Load US counties information
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# fips to map county codes to location
fipsDF = pd.read_csv('data/WV FIPS.csv')
fips = fipsDF.loc[:, 'FIPS'].tolist()

# load data
df = pd.read_csv("data/WV Drug Epidemic Dataset.xlsx - Drug Mortality (Per 100,000).csv")
df = df.iloc[np.arange(len(fips))]

# get year data with slider
year_to_filter = str(st.slider('Year', 2005, 2014, 2014))    # 2005 to 2014 for now

# Create overall dataframe
df['County'] = df['County'].str.replace(' County', '', case=False)
df[year_to_filter] = df[year_to_filter].astype(str)
df[year_to_filter] = df[year_to_filter].str.replace(',', '', case=False).astype(float)
df['2006'] = df['2006'].astype(str)
df['2006'] = df['2006'].str.replace(',', '', case=False).astype(float)
merged_df = df.merge(fipsDF, on='County', how='inner')

# print("A")
# fig = make_subplots(rows=2, cols=1,
#                     specs=[[{'type': 'mapbox'}, {'type': 'xy'}]],
#                     subplot_titles=('Title 1', 'Title 2'))
# # create map figure
# fig.append_trace(px.choropleth_mapbox(merged_df, 
#                            geojson=counties, 
#                            locations='FIPS', 
#                            color=year_to_filter,
#                            color_continuous_scale=px.colors.sequential.Reds,
#                            center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
#                            opacity=0.5,
#                            hover_name = df['County'].tolist(),
#                            mapbox_style="carto-positron").data[0], row=1, col=1)

# # add second color
# fig2 = px.choropleth_mapbox(merged_df,
#                            geojson=counties, 
#                            locations='FIPS', 
#                            color=year_to_filter,
#                            color_continuous_scale=px.colors.sequential.Viridis,
#                            center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
#                            opacity=0.5,
#                            mapbox_style="carto-positron")
# print("B")
# fig.append_trace(fig2.data[0], row=2, col=1)

# print("C")

fig = px.choropleth_mapbox(merged_df,
                            geojson=counties,  # You can provide your own GeoJSON file or use px.data.gapminder()
                            locations='FIPS',
                            #featureidkey="properties.name",
                            color='2006',
                            color_continuous_scale=px.colors.sequential.Reds,
                            hover_name=df['County'].tolist(),
                            center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
                            mapbox_style="carto-positron",
                            title='Bivariate Choropleth Map',
                            labels={'Variable1': 'Variable 1'},
                            #template='plotly_dark',
                            opacity=0.35)

#fig.show()

fig.add_trace(go.Choroplethmapbox(locations=fips,
                                  geojson=counties,
                                  z=merged_df["2006"].tolist(),
                                  colorscale=px.colors.sequential.Blues,
                                  marker_opacity=0.35,
                                  marker_line_width=0))


# # Add a second trace for Variable2
# fig.add_trace(px.choropleth_mapbox(merged_df, 
#                                     geojson=counties,
#                                     locations='FIPS',
#                                     # featureidkey="properties.name",
#                                     color='2014',
#                                     color_continuous_scale=px.colors.sequential.Blues,
#                                     center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
#                                     mapbox_style="carto-positron",
#                                     #hover_name='Country',
#                                     #template='plotly_dark',
#                                     opacity=0.7).data[0])

#fig.show()

st.plotly_chart(fig, theme="streamlit")

print("D")

# Define the content of the page
st.write("# Page Under Construction")
st.write("This page is currently under construction. Please check back later for updates.")