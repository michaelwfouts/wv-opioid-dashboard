import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from scipy.stats import pearsonr
from scipy.stats import spearmanr

# Set the page title
st.set_page_config(
    page_title=" Parameter Correlation Exploration",
    page_icon="📊",
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
    'Opioid Dispensing Rate (Per 100)' : 'data/WV Drug Epidemic Dataset.xlsx - Opioid Dispensing Rate per 100.csv',
    'Physician Ratio' : 'data/WV Drug Epidemic Dataset.xlsx - Physicians Ratio (people_1 primary care physican)_numeric.csv',
    'Manual Labor (Employment per 1,000 Jobs)' : 'data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - (Overall).csv'
}

# Visualization Explaination
st.write("# Parameter Correlation Exploration")
st.markdown("""---""")
st.write("This visualization compares county data for a given year and metric to produce a correlation metric.  This correlation metric shows how related the metrics are where correlation coefficients closer to +1 move in the same direction, coefficients closer to -1 move in opposite directions, and coefficients close to 0 are not correlated with eachother.")
st.markdown("""---""")

# Visualization Layout
# The first row has two columns.  The first selects the metric of interest and the second selects the correlation method
col1, col2 = st.columns([1, 1])
with col1:
    metric = st.selectbox(
        'Select metric to explore:',
        (fileDict.keys()),
        index=0
    )

with col2:
    correlation_selection = st.radio(
    "Select Correlation Type:",
    ["**Pearson**", "**Spearman**"],
    captions = ["Linear Relationships", "Mix of Linear and Non-Linear Relationships"])

# Load Data for Selected Metric
df = pd.read_csv(fileDict[metric])
# Some data has blank values at the end; so hard cut off after 55 rows
df = df.iloc[np.arange(len(fips))]

# Use Slider to Select Year
year_to_filter = st.selectbox(
    'Select Year:',
    df.columns[1:].sort_values(ascending=False)
)

# The following section determines the analysis to be completed (Pearson or Spearman)
# For Pearson
if correlation_selection == '**Pearson**':
    # Name Plot
    plot_title = 'Pearson Correlation'
    # Dummy lists for holding data
    correlation_metric = []
    correlation_value = []
    # For each dataset possible
    for value in fileDict:
        # Load in the dataset for comparison
        df_test = pd.read_csv(fileDict[value]).iloc[np.arange(len(fips))]
        # Only apply to years where both datasets have values
        if year_to_filter in df_test:
            # Some counties have missing data.  Identify those indexes for the year given if applicable.
            # Missing data indexes in metric selected
            missing_filter = df[year_to_filter].isnull()
            # Missing data indexes in all other datasets
            missing_filter_test = df_test[year_to_filter].isnull()
            # Combine to create index where only both datasets have values
            index_filter = np.invert(missing_filter + missing_filter_test)

            # Perform Correlation filtering by year and where data is available.
            r, p_value = pearsonr(df[year_to_filter][index_filter].astype(float), df_test[year_to_filter][index_filter].astype(float))
            correlation_metric.append(value)
            correlation_value.append(r)

# For Spearman
if correlation_selection == '**Spearman**':
    plot_title = 'Spearman Correlation'
    correlation_metric = []
    correlation_value = []
    # For each dataset possible
    for value in fileDict:
        # Load in the dataset for comparison
        df_test = pd.read_csv(fileDict[value]).iloc[np.arange(len(fips))]
        # Only apply to years where both datasets have values
        if year_to_filter in df_test:
            # Some counties have missing data.  Identify those indexes for the year given if applicable.
            # Missing data indexes in metric selected
            missing_filter = df[year_to_filter].isnull()
            # Missing data indexes in all other datasets
            missing_filter_test = df_test[year_to_filter].isnull()
            # Combine to create index where only both datasets have values
            index_filter = np.invert(missing_filter + missing_filter_test)

            # Perform Correlation filtering by year and where data is available.
            r, p_value = spearmanr(df[year_to_filter][index_filter], df_test[year_to_filter][index_filter])
            correlation_metric.append(value)
            correlation_value.append(r)

# Round and create dataframe for visualization
df_bar = pd.DataFrame({'Values': np.array(correlation_value).round(3)}, index = correlation_metric).sort_values(by="Values", ascending=False)
# Remove metric of selected since it's comparison value will always be 1
df_bar = df_bar[df_bar['Values'] != 1]

# Create a Plotly bar chart
fig = px.bar(
    df_bar,
    x=df_bar.index,
    y='Values',
    title=metric,
)

fig.update_xaxes(title_text='')
fig.update_yaxes(title_text=plot_title)

# Customize the chart
fig.update_layout(xaxis=dict(tickangle=-45))

fig.update_traces(hovertemplate='Comparison Metric: %{x}<br>' + plot_title + ': %{y}')

# Plot figure
st.plotly_chart(fig, theme="streamlit")

footer="Sources: Centers for Disease Control and Prevention (CDC), US Bureau of Labor Statistics, United States Census Bureau, US Department of Agriculture (USDA) Economic Research Service, IndexMundi, Inter-university Consortium for Political and Social Research (ICPSR)"
st.markdown(footer)