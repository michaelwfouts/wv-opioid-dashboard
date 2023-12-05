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
    'Poverty Rates (Percent)':        "data/WV Drug Epidemic Dataset.xlsx - Poverty Rates (Percent).csv",
    'Drug Arrests (Per 1,000)':       "data/WV Drug Epidemic Dataset.xlsx - Drug Arrests (Per 1000).csv",
    'Drug Mortality (Per 100,000)':       "data/WV Drug Epidemic Dataset.xlsx - Drug Mortality (Per 100,000).csv",
    'Illicit Drug Use (Percent)':     "data/WV Drug Epidemic Dataset.xlsx - Illicit Drug Past Mo (Percent).csv",
    'Life Expectancy':      "data/WV Drug Epidemic Dataset.xlsx - Life Expectancy.csv",
    'Population':           "data/WV Drug Epidemic Dataset.xlsx - Population.csv",
    'Unemployment Rates (Percent)':   "data/WV Drug Epidemic Dataset.xlsx - Unemployment Rates (Percent).csv",
    'Opioid Dispensing Rate (Per 100)' : 'data\WV Drug Epidemic Dataset.xlsx - Opioid Dispensing Rate per 100.csv',
    'Physician Ratio' : 'data\WV Drug Epidemic Dataset.xlsx - Physicians Ratio (people_1 primary care physican)_numeric.csv',
    'Fish, Farms, and Forest Labor (Employment per 1,000 Jobs)':     'data\WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Farm&Fish&Forest.csv',
    'Install, Maintenance, and Repair (Employment per 1,000 Jobs)':     'data\WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Install&Mainten&Repair.csv',
    'Production Labor (Employment per 1,000 Jobs)':     'data\WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Production.csv',
    'Construction and Extraction Labor (Employment per 1,000 Jobs)':     'data\WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs- Construction&Extraction .csv'
}

# Visualization Explanation
st.write("# Historical Events")
st.markdown("""---""")
st.write("This visualization takes an event perspective to the opioid epidemic, events related to the crisis from 1995 to current day.  Event information was taken from several sources and can be filtered by source. Metrics of consideration are aggregated over the 55 counties for the entire state of WV.")
st.markdown("""---""")

metric = st.selectbox(
    'Select metric to explore:',
    (fileDict.keys()),
     index=0
)

# load data
df = pd.read_csv(fileDict[metric])
df = df.iloc[np.arange(len(fips))]

if metric in ['Fish, Farms, and Forest Labor (Employment per 1,000 Jobs)', 'Install, Maintenance, and Repair (Employment per 1,000 Jobs)', 'Production Labor (Employment per 1,000 Jobs)', 'Construction and Extraction Labor (Employment per 1,000 Jobs)']:
    # If labor data, drop Area Column
    df = df.drop('Area', axis=1)


df_timeline = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Timeline.csv')

source_filter = st.multiselect(
    'Filter Sources:',
    df_timeline['Source (Short)'].unique().tolist())

if source_filter: # if source_filter is not blank
    df_timeline = df_timeline[df_timeline['Source (Short)'].isin(source_filter)]
    df_timeline = df_timeline.reset_index()

# Drug Arrests and Population are totals and need to be summed.  The other metrics are
# per capita/percentages and averaging makes the most sense.
if metric in ['Population']:
    plot_row = df.drop(df.columns[0], axis=1).sum(axis=0)
    # Convert the sum row to a DataFrame and transpose it to make it a single row
    plot_df = pd.DataFrame(plot_row)
else:
    plot_row = df.drop(df.columns[0], axis=1)
    plot_row = plot_row.apply(pd.to_numeric, errors='coerce')
    plot_row = plot_row.mean(axis=0)
    # Convert the sum row to a DataFrame and transpose it to make it a single row
    plot_df = pd.DataFrame(plot_row)

# Create a line chart using Plotly Express
fig = px.line(plot_df, x=plot_df.index, y=0, markers=True, line_shape='linear', title= metric + ' vs Time')
fig.update_xaxes(title_text='Year')
fig.update_yaxes(title_text=metric)
fig.update_traces(hovertemplate='Year: %{x} <br>' + metric +': %{y:.1f}')

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

# To not make the legend incredibly long
if metric in ['Fish, Farms, and Forest Labor (Employment per 1,000 Jobs)', 'Install, Maintenance, and Repair (Employment per 1,000 Jobs)', 'Production Labor (Employment per 1,000 Jobs)', 'Construction and Extraction Labor (Employment per 1,000 Jobs)']:
    fig.update_xaxes(title_text='Employment Per 1,000') 

# Show the plot
st.plotly_chart(fig, theme="streamlit")

footer="Sources: White House, Centers for Disease Control and Prevention (CDC), United States Food and Drug Administration (FDA), WV.gov, Department of Justice (DOJ)"
st.markdown(footer)