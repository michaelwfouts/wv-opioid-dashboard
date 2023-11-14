import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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

# load data
# df = pd.read_csv(fileDict[metric])
df = df.iloc[np.arange(len(fips))]

sum_row = df.drop(df.columns[0], axis=1).sum(axis=0)

# Convert the sum row to a DataFrame and transpose it to make it a single row
sum_df = pd.DataFrame(sum_row)

# Create a line chart using Plotly Express
fig = px.line(sum_df, x=sum_df.index, y=0, markers=True, line_shape='linear', title='Population Over Years')

# Show the plot
st.plotly_chart(fig, theme="streamlit")