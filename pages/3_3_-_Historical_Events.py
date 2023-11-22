import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# Set the page title
st.set_page_config(
    page_title="Historical Events",
    page_icon="📖",
    layout="centered",
)

# Load data
@st.cache_data  # Cache ability for faster app 
def load_fips(path):
    # Return list of FIPS numbers for 55 counties
    fipsDF = pd.read_csv(path)
    fips = fipsDF.loc[:, 'FIPS'].tolist()
    return fips

fips = load_fips('data/WV FIPS.csv')

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

# Visualization Explaination
st.write("# Historical Events Visualization")
st.write("This visualization takes an event perspective to the opioid epidemic, events related to the crisis from 1995 to current day.  Event information was taken from several sources and can be filtered by source. Metrics of consideration are aggregated over the 55 counties for the entire state of WV.")
st.markdown("""---""")

metric = st.selectbox(
    'Select metric to explore',
    ('Drug Arrests', 'Drug Mortality', 'Illicit Drug Use', 'Life Expectancy',
     'Population', 'Poverty Rates', 'Unemployment Rates'),
     index=0
)

# load data
df = pd.read_csv(fileDict[metric])
df = df.iloc[np.arange(len(fips))]

df_timeline = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Timeline.csv')

source_filter = st.multiselect(
    'Select the Sources You Would Like',
    df_timeline['Source (Short)'].unique().tolist())

if source_filter: # if source_filter is not blank
    df_timeline = df_timeline[df_timeline['Source (Short)'].isin(source_filter)]
    df_timeline = df_timeline.reset_index()

# Drug Arrests and Population are totals and need to be summed.  The other metrics are
# per capita/percentages and averaging makes the most sense.
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
fig.update_traces(hovertemplate='Year: %{x} <br>' + metric +': %{y}')

for i, line in enumerate(df_timeline['Year']):
    x_points = [line] * 10  # Same x-coordinate for all 5 points
    y_points = np.linspace(plot_df[0].min(), plot_df[0].max(), 10)  # Vary y-coordinate from 0 to max y

    fig.add_trace(go.Scatter(x=x_points, y=y_points,
                             mode='lines',
                             line=dict(color='red', width=2, dash='dash'),
                             hoverinfo='text',
                             hovertext='Year: ' + str(df_timeline['Year'][i]) + '<br>Source: ' + df_timeline['Source (Short)'][i] + '<br>Event: ' + df_timeline['Event'][i],
                             showlegend=False))

fig.update_layout(
    hoverlabel=dict(
        align="left"
    )
)
# Show the plot
st.plotly_chart(fig, theme="streamlit")