import streamlit as st
import pandas as pd
import numpy as np

import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

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

# select box for metric
metric = st.selectbox(
    'Select metric to explore',
    ('Drug Arrests', 'Drug Mortality', 'Illicit Drug Use', 'Life Expectancy',
     'Population', 'Poverty Rates', 'Unemployment Rates'),
     index=0
)

# load data
df = pd.read_csv(fileDict[metric])
df = df.iloc[np.arange(len(fips))]

# get year data with slider
year_to_filter = st.slider('Year', 2005, 2014, 2014)    # 2005 to 2014 for now
values = df.loc[:, str(year_to_filter)].tolist()
for i in range(len(values)):
    values[i] = str(values[i])
    values[i] = values[i].replace(",", "")
    values[i] = float(values[i])
endpts = list(np.linspace(0, max(values), len(colorDict[metric]) - 1))  # thresholds for different colors in choropleth

print(len(fips))
print(len(values))
# strcture figure
fig = ff.create_choropleth(
    fips=fips, values=values, scope=["WV"],
    binning_endpoints=endpts, colorscale=colorDict[metric],
    show_state_data=False,
    show_hover=True,
    simplify_county=0,
    asp = 2.5,
    title_text = 'West Virginia Population',
    legend_title = 'Population'
)
fig.layout.template = None
fig.update_layout(showlegend=True)

st.plotly_chart(fig, theme="streamlit")