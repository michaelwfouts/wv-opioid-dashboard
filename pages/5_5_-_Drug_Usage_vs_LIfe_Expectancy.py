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


# Load US counties information
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# fips to map county codes to location
fipsDF = pd.read_csv('data/WV FIPS.csv')
fips = fipsDF.loc[:, 'FIPS'].tolist()

# load data
df = pd.read_csv("data/WV Drug Epidemic Dataset.xlsx - Life Expectancy.csv")
df = df.iloc[np.arange(len(fips))]
df2 = pd.read_csv("data/WV Drug Epidemic Dataset.xlsx - Opioid Dispensing Rate per 100.csv")
df2 = df2.iloc[np.arange(len(fips))]

# national average lifespan data
lifeExptDF = pd.read_csv("data/National Average Lifespan.csv")

# get year data with slider
year_to_filter = str(st.slider('Year', 2006, 2020, 2020))    # 2006 to 2020 for now

# Create overall dataframes
df['County'] = df['County'].str.replace(' County', '', case=False)
df[year_to_filter] = df[year_to_filter].astype(str)
df[year_to_filter] = df[year_to_filter].str.replace(',', '', case=False).astype(float)
lifeExpectancy = lifeExptDF.loc[lifeExptDF['Year'] == year_to_filter, 'Expectancy']
lifeExpectancy = lifeExpectancy[lifeExpectancy.keys()[0]]
df[year_to_filter] = lifeExpectancy - df[year_to_filter]
merged_df = df.merge(fipsDF, on='County', how='inner')

df2['County'] = df2['County'].str.replace(' County', '', case=False)
df2[year_to_filter] = df2[year_to_filter].astype(str)
df2[year_to_filter] = df2[year_to_filter].str.replace(',', '', case=False).astype(float)
merged_df2 = df2

# apply high/medium/low column to dataframes
max = merged_df[year_to_filter].max()
min = merged_df[year_to_filter].min()
third = (max - min)/3
max2 = merged_df2[year_to_filter].max()
min2 = merged_df2[year_to_filter].min()
third2 = (max2 - min2)/3
ranges = []
for i in range(len(fips)):
    value = merged_df.iloc[i][year_to_filter]
    value2 = merged_df2.iloc[i][year_to_filter]
    if value <= min + third:
        if value2 <= min2 + third2:
            ranges.append("low_low")
        elif min2 + third2 <= value2 and value2 <= max2 - third2:
            ranges.append("low_medium")
        elif max2 - third2 <= value2:
            ranges.append("low_high")
    elif min + third <= value and value <= max - third:
        if value2 <= min2 + third2:
            ranges.append("medium_low")
        elif min2 + third2 <= value2 and value2 <= max2 - third2:
            ranges.append("medium_medium")
        elif max2 - third2 <= value2:
            ranges.append("medium_high")
    elif max - third <= value:
        if value2 <= min2 + third2:
            ranges.append("high_low")
        elif min2 + third2 <= value2 and value2 <= max2 - third2:
            ranges.append("high_medium")
        elif max2 - third2 <= value2:
            ranges.append("high_high")
merged_df["ranges"] = ranges

# blue = FFFFFF 8888FF 0000FF
# red =  FFFFFF FF8888 FF0000
# average colors together
biColor = {'low_low': '#FFFFFF', 'low_medium': '#C3C3FF', 'low_high': '#7F7FFF',
           'medium_low': '#FFC3C3', 'medium_medium': '#C388C3', 'medium_high': '#7F44C3',
           'high_low': '#FF7F7F', 'high_medium': '#C3447F', 'high_high': '#7F007F'}

custom_color_scale = [
    [0.0, '#FFFFFF'], [0.125, '#C3C3FF'], [0.25, '#7F7FFF'],
    [0.375, '#FFC3C3'], [0.5, '#C388C3'], [0.625, '#7F44C3'],
    [0.75, '#FF7F7F'], [0.875, '#C3447F'], [1.0, '#7F007F']
]

fig = px.choropleth_mapbox(merged_df,
                            geojson=counties,  # You can provide your own GeoJSON file or use px.data.gapminder()
                            locations='FIPS',
                            color='ranges',
                            color_discrete_map=biColor,
                            hover_name=df['County'].tolist(),
                            center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
                            mapbox_style="carto-positron",
                            title='Bivariate Choropleth Map',
                            labels={'Variable1': 'Variable 1'},
                            opacity=1)
# removes the legend
fig.update_traces(showlegend=False)
fig.update_layout(width=550)

# create the legend
legend = go.Heatmap(
    z=[[0.0, 0.125, 0.25], [0.375, 0.5, 0.625], [0.75, 0.875, 1.0]],
    x=[1, 2, 3],
    y=[1, 2, 3],
    showscale=False,
    colorscale=custom_color_scale,
)

# Create a layout with a color axis for the legend
layout = go.Layout(
    title="Legend",
    height=300,
    width=230,
    xaxis=dict(title="Difference in life expectency"),
    yaxis=dict(title="Drug usage"),
    coloraxis=dict(
        cmin=1,  # Set the minimum value
        cmax=9,  # Set the maximum value
        colorbar=dict(title="Legend Title")
    )
)
legend = go.Figure(data=[legend], layout=layout)
legend.update_traces(showlegend=False)

# have legend next to figure
col1, col2 = st.columns([4, 1])
with col1:
    st.plotly_chart(fig, theme="streamlit")
with col2:
    st.plotly_chart(legend, theme="streamlit")

#st.plotly_chart(fig, theme="streamlit")
#st.plotly_chart(legend, theme="streamlit")

# Define the content of the page
st.write("# Page Under Construction")
st.write("This page is currently under construction. Please check back later for updates.")