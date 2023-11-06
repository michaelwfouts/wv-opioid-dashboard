import streamlit as st
import pandas as pd
import numpy as np

import json
import numpy as np
import pandas as pd
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

###
# read geojson file containing WV map with county borders
f = open('data/WV_County_Boundaries.geojson')
counties = json.load(f)

# load data
df = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Population.csv')
df = df.dropna()
df = df.loc[:, ['County', '2017']]

fipsDF = pd.read_csv('data/WV FIPS.csv')

colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"]
colorscale = px.colors.sequential.Plasma
fips = fipsDF.loc[:, 'FIPS'].tolist()
values = df.loc[:, '2017'].tolist()
for i in range(len(values)):
    values[i] = values[i].replace(",", "")
    values[i] = int(values[i])
endpts = list(np.linspace(0, max(values), len(colorscale) - 1))

# strcture figure

df['County'] = df['County'].str.replace(' County', '', case=False)
merged_df = df.merge(fipsDF, on='County', how='inner')

# Load US counties information
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
    
# strcture figure
fig = px.choropleth_mapbox(merged_df, 
                           geojson=counties, 
                           locations='FIPS', 
                           color='2017',
                           color_continuous_scale="Viridis",
                           center = {"lat": 37.0902, "lon": -95.7129}, zoom = 2.5,
                           opacity=0.75,
                           mapbox_style="carto-positron")


# fig = ff.create_choropleth(
#     fips=fips, values=values, scope=["WV"],
#     binning_endpoints=endpts, colorscale=colorscale,
#     show_state_data=False,
#     show_hover=True,
#     simplify_county=0,
#     asp = 2.5,
#     title_text = 'West Virginia Population',
#     legend_title = 'Population'
# )
# fig.layout.template = None
# fig.update_layout(showlegend=False)

st.plotly_chart(fig)
###

# Load US counties information
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)



# fig.update_layout(title='Biomass Residue Generation by County', 
#                   coloraxis_colorbar_title_text='Biomass (M tonnes/yr)'
# )

# fig.show()