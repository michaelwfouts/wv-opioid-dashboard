import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

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
df_timeline = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Timeline.csv')

# load data
# df = pd.read_csv(fileDict[metric])
df = df.iloc[np.arange(len(fips))]

if metric in ['Drug Arrests', 'Population']:
    plot_row = df.drop(df.columns[0], axis=1).sum(axis=0)
    # Convert the sum row to a DataFrame and transpose it to make it a single row
    plot_df = pd.DataFrame(plot_row)
else:
    plot_row = df.drop(df.columns[0], axis=1).mean(axis=0)
    # Convert the sum row to a DataFrame and transpose it to make it a single row
    plot_df = pd.DataFrame(plot_row)

# Create a line chart using Plotly Express
fig = px.line(plot_df, x=plot_df.index, y=0, markers=True, line_shape='linear', title= metric + ' vs Time')
fig.update_xaxes(title_text='Year')
fig.update_yaxes(title_text=metric)

for i, line in enumerate(df_timeline['Year']):
    x_points = [line] * 10  # Same x-coordinate for all 5 points
    y_points = np.linspace(plot_df[0].min(), plot_df[0].max(), 10)  # Vary y-coordinate from 0 to max y

    fig.add_trace(go.Scatter(x=x_points, y=y_points,
                             mode='lines',
                             line=dict(color='red', width=2, dash='dash'),
                             hoverinfo='text',
                             hovertext='Year: ' + str(df_timeline['Year'][i]) + '<br>Event: ' + df_timeline['Event'][i],
                             showlegend=False))

fig.update_layout(
    hoverlabel=dict(
        align="left"
    )
)
# Show the plot
st.plotly_chart(fig, theme="streamlit")