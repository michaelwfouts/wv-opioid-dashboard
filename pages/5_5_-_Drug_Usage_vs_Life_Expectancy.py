import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
# from plotly.subplots import make_subplots
from urllib.request import urlopen

# Set the page title
st.set_page_config(
    page_title="Drug Usage vs Life Expectancy",
    page_icon="⌛",
    layout="centered",
)

# Visualization Explaination
st.write("# Drug Usage vs Life Expectancy")
st.markdown("""---""")
st.write("While it can be hypothesized that the higher the life expectancy, the lower the opioid usage with the epidemic, this relationship needs to be explored in more detail.  These visualizations aim at looking at this from a geographical perspective to see if this is true.")
st.markdown("""---""")

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

# st.write("Choropleth maps may take some time to load.")

# Create overall dataframes
df['County'] = df['County'].str.replace(' County', '', case=False)
df[year_to_filter] = df[year_to_filter].astype(str)
df[year_to_filter] = df[year_to_filter].str.replace(',', '', case=False).astype(float)
# lifeExpectancy = lifeExptDF.loc[lifeExptDF['Year'] == year_to_filter, 'Expectancy']
# lifeExpectancy = lifeExpectancy[lifeExpectancy.keys()[0]]
# df[year_to_filter] = lifeExpectancy - df[year_to_filter]
merged_df = df.merge(fipsDF, on='County', how='inner').sort_values('County')

df2['County'] = df2['County'].str.replace(' County', '', case=False)
df2[year_to_filter] = df2[year_to_filter].astype(str)
df2[year_to_filter] = df2[year_to_filter].str.replace(',', '', case=False).astype(float)
merged_df2 = df2.sort_values('County')

# apply high/medium/low column to dataframes
# Life Expectancy
max = merged_df[year_to_filter].max()
min = merged_df[year_to_filter].min()
third = (max - min)/3
# Opioid Dispensing
max2 = merged_df2[year_to_filter].max()
min2 = merged_df2[year_to_filter].min()
third2 = (max2 - min2)/3
ranges = []
for i in range(len(fips)):
    value = merged_df.iloc[i][year_to_filter]
    value2 = merged_df2.iloc[i][year_to_filter]
    if value <= min + third:
        if value2 <= min2 + third2:
            ranges.append("Low Opioid, Low Life Expt")
        elif min2 + third2 <= value2 and value2 <= max2 - third2:
            ranges.append("Med Opioid, Low Life Expt")
        elif max2 - third2 <= value2:
            ranges.append("High Opioid, Low Life Expt")
    elif min + third <= value and value <= max - third:
        if value2 <= min2 + third2:
            ranges.append("Low Opioid, Med Life Expt")
        elif min2 + third2 <= value2 and value2 <= max2 - third2:
            ranges.append("Med Opioid, Med Life Expt")
        elif max2 - third2 <= value2:
            ranges.append("High Opioid, Med Life Expt")
    elif max - third <= value:
        if value2 <= min2 + third2:
            ranges.append("Low Opioid, High Life Expt")
        elif min2 + third2 <= value2 and value2 <= max2 - third2:
            ranges.append("Med Opioid, High Life Expt")
        elif max2 - third2 <= value2:
            ranges.append("High Opioid, High Life Expt")
merged_df["values"] = ranges

merged_df = merged_df[['County', year_to_filter, 'values', 'FIPS']]
merged_df = merged_df.rename(columns={year_to_filter: year_to_filter + 'Metric'})

drug_use_df = merged_df2[['County', year_to_filter]]
df['County'] = df['County'].str.replace(' County', '', case=False)
drug_use_df = drug_use_df.rename(columns={year_to_filter: year_to_filter + 'Drug Use'})

drug_use_df['County'] = drug_use_df['County'].str.replace(' County', '', case=False)
drug_use_df['County'] = drug_use_df['County'].str.replace(', WV', '', case=False)

merged_df = merged_df.merge(drug_use_df, on='County', how='inner')

# blue = FFFFFF 8888FF 0000FF
# red =  FFFFFF FF8888 FF0000
# average colors together
biColor = {'Low Opioid, Low Life Expt': '#FFFFFF', 'Low Opioid, Med Life Expt': '#C3C3FF', 'Low Opioid, High Life Expt': '#7F7FFF',
           'Med Opioid, Low Life Expt': '#FFC3C3', 'Med Opioid, Med Life Expt': '#C388C3', 'Med Opioid, High Life Expt': '#7F44C3',
           'High Opioid, Low Life Expt': '#FF7F7F', 'High Opioid, Med Life Expt': '#C3447F', 'High Opioid, High Life Expt': '#7F007F'}

custom_color_scale = [
    [0.0, '#FFFFFF'], [0.125, '#C3C3FF'], [0.25, '#7F7FFF'],
    [0.375, '#FFC3C3'], [0.5, '#C388C3'], [0.625, '#7F44C3'],
    [0.75, '#FF7F7F'], [0.875, '#C3447F'], [1.0, '#7F007F']
]

# Display loading bar
with st.spinner("Loading..."):
    fig = px.choropleth_mapbox(merged_df,
                                geojson=counties,  # You can provide your own GeoJSON file or use px.data.gapminder()
                                locations='FIPS',
                                color='values',
                                color_discrete_map=biColor,
                                hover_name=df['County'].tolist(),
                                center = {"lat": 38.7214, "lon": -80.6530}, zoom = 5,
                                mapbox_style="carto-positron",
                                title='Opiod Dispensing Rate vs Life Expectancy',
                                labels={'Variable1': 'Variable 1', "Legend": " "},
                                category_orders={'values': ['Low Opioid, Low Life Expt', 'Low Opioid, Med Life Expt', 'Low Opioid, High Life Expt', 
                                                            'Med Opioid, Low Life Expt', 'Med Opioid, Med Life Expt', 'Med Opioid, High Life Expt', 
                                                            'High Opioid, Low Life Expt', 'High Opioid, Med Life Expt', 'High Opioid, High Life Expt']},
                                opacity=1.0,
                                custom_data=['County', 
                                            year_to_filter + 'Metric',
                                            year_to_filter + 'Drug Use',
                                            'values'] )
    # removes the legend
    #fig.update_traces(showlegend=False)
    fig.update_layout(width=550)

    fig.update_traces(hovertemplate='County: %{customdata[0]}<br><br>' + 
                                    'Metrics: %{customdata[3]}<br>' + 
                                    'Opioid Dispensing Rate per 100: %{customdata[2]:.1f}<br>' +
                                    'Life Expectancy: %{customdata[1]:.1f}')
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
        colorscale=custom_color_scale,
    )

    # Create a layout with a color axis for the legend
    layout = go.Layout(
        title="Legend",
        height=300,
        width=270,
        xaxis=dict(title="Life Expectancy"),
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

# Linechart for how life expectancy has changed over time

fig2 = px.line()

fig2.add_scatter(x=lifeExptDF['Year'], y=lifeExptDF['Expectancy'], mode='lines', name='National Life Expectancy')

# Add in specific data
df = pd.read_csv("data/WV Drug Epidemic Dataset.xlsx - Life Expectancy.csv")
df = df.iloc[np.arange(len(fips))]
df['County'] = df['County'].str.replace(' County', '', case=False)
WV_life = pd.DataFrame(df.drop(df.columns[0], axis=1).mean(axis=0))

fig2.add_scatter(x=WV_life.index, y=WV_life[0], mode='lines', name='WV Life Expectancy')

# Customize layout
fig2.update_layout(title='Life Expectancy Comparison', 
                   xaxis_title='Year', 
                   yaxis_title='Life Expectancy')

fig2.update_xaxes(range=[2000, 2023])
fig2.update_layout(hovermode="x unified")

# Show the plot
# st.plotly_chart(fig2, theme="streamlit")

# Dot Plot to explore relationship between counties
drug_use_df = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Opioid Dispensing Rate per 100.csv')
drug_use_df['County'] = drug_use_df['County'].str.replace(' County', '', case=False)
drug_use_df['County'] = drug_use_df['County'].str.replace(', WV', '', case=False)
drug_use_df = drug_use_df[['County', year_to_filter]]
df = df[['County', year_to_filter]]
df = df.rename(columns={year_to_filter: 'Life Expectancy'})
drug_use_df = drug_use_df.rename(columns={year_to_filter: 'Opioid Dispensing Rate'})
merged_df = df.merge(drug_use_df, on='County', how='inner')

# Create a dot plot with Plotly Express
fig3 = px.scatter(merged_df, 
                  x='Opioid Dispensing Rate', 
                  y='Life Expectancy',
                  custom_data=['County'])

fig3.update_traces(hovertemplate='County: %{customdata[0]}<br><br>' + 
                                'Opioid Dispensing: %{x:.2f} <br>' +
                                'Life Expectancy: %{y:.2f}')

# Customize layout
fig3.update_layout(title='Opioid Dispensing Rate vs Life Expectancy', 
                   xaxis_title='Opioid Dispensing Rate', 
                   yaxis_title='Life Expectancy')

st.plotly_chart(fig2, theme="streamlit")

st.plotly_chart(fig3, theme="streamlit")

footer="Sources: Centers for Disease Control and Prevention (CDC), Global Health Data Exchange (GHDx), County Health Rankings and Roadmaps"
st.markdown(footer)
