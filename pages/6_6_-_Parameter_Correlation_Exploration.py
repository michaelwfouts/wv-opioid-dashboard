import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from scipy.stats import pearsonr

# Set the page title
st.set_page_config(
    page_title="Under Construction",
    page_icon="🚧",
    layout="centered",
)

# fips to map county codes to location
fipsDF = pd.read_csv('data/WV FIPS.csv')
fips = fipsDF.loc[:, 'FIPS'].tolist()

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

metric = st.selectbox(
    'Select metric to explore',
    ('Drug Arrests', 'Drug Mortality', 'Illicit Drug Use', 'Life Expectancy',
     'Population', 'Poverty Rates', 'Unemployment Rates'),
     index=0
)

# load data
df = pd.read_csv(fileDict[metric])

# get year data with slider
year_to_filter = st.selectbox(
    'Select Year:',
    df.columns[1:].sort_values(ascending=False)
)

# load data
# df = pd.read_csv(fileDict[metric])
df = df.iloc[np.arange(len(fips))]

# Assume 2014 for all the data
pearson_metric = []
pearson_value = []
for value in fileDict:
    df_test = pd.read_csv(fileDict[value]).iloc[np.arange(len(fips))]
    if year_to_filter in df_test:
        missing_filter = df[year_to_filter].isnull()
        missing_filter_test = df_test[year_to_filter].isnull()
        index_filter = np.invert(missing_filter + missing_filter_test)
        r, p_value = pearsonr(df[year_to_filter][index_filter], df_test[year_to_filter][index_filter])
        pearson_metric.append(value)
        pearson_value.append(r)

# Round and create dataframe for visualization
df_bar = pd.DataFrame({'Values': np.array(pearson_value).round(3)}, index = pearson_metric).sort_values(by="Values", ascending=False)
# Remove metric of comparison
df_bar = df_bar[df_bar['Values'] != 1]

# Create a Plotly bar chart
fig = px.bar(
    df_bar,
    x=df_bar.index,
    y='Values',
    title=metric
)

fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='Pearson Correlation')

# Customize the chart
fig.update_layout(xaxis=dict(tickangle=-45))

st.plotly_chart(fig, theme="streamlit")