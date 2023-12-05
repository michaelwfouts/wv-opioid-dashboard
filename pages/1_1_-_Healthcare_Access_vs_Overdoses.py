import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import math

# Set the page title
st.set_page_config(
    page_title="Healthcare Access vs Overdoses",
    page_icon="🏥",
    layout="centered",
)

# Visualization explanation
url = "https://www.amnhealthcare.com/blog/physician/perm/is-there-an-ideal-physician-to-population-ratio/"
st.write("# Healthcare Access vs Overdoses")
st.markdown("""---""")
st.write("This visualization explores the relationship between healthcare access--measured by the person-to-physician ratio per county--and overdoses per 100,000 people. Hovering over each dot reveals the county name and the exact numbers for the two parameters described. Dots in red are counties that have a person-to-physician ratio below what is considered viable for a region's populace.*")
st.write("*The cutoff person-to-physician ratio was derived by taking the average Family Medicine ratios of the three sources listed on [this AMN Healthcare webpage](%s), updated in 2023.*" %url)
st.markdown("""---""")

# Load data
df_physician_person_ratio = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Physicians Ratio (people_1 primary care physican).csv')
df_overdose = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Drug Mortality (Per 100,000).csv')
df_visual = pd.DataFrame()

# Get county names (will use in hover info)
counties = df_physician_person_ratio.County

# Average physician to person ratio:
# about 26 per 100,000 people
# https://www.amnhealthcare.com/blog/physician/perm/is-there-an-ideal-physician-to-population-ratio/
cutoff = 26 / 100000

# Use slider to select year
year_to_filter = st.selectbox(
    'Select Year:',
    ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
)

# Get pertinent info depending on selected year
# NOTE: removing Clay County due to missing data for years 2015 - 2018
if year_to_filter == "2013":
    df_physician_person_ratio = df_physician_person_ratio["2013"].head(55)
    df_overdose = df_overdose["2013"].head(55)
elif year_to_filter == "2014":
    df_physician_person_ratio = df_physician_person_ratio["2014"].head(55)
    df_overdose = df_overdose["2014"].head(55)
elif year_to_filter == "2015":
    df_physician_person_ratio = df_physician_person_ratio["2015"].head(55)
    df_overdose = df_overdose["2015"].head(55)
    df_physician_person_ratio.drop(df_physician_person_ratio.index[7], inplace=True)
    df_overdose.drop(df_overdose.index[7], inplace=True)
elif year_to_filter == "2016":
    df_physician_person_ratio = df_physician_person_ratio["2016"].head(55)
    df_overdose = df_overdose["2016"].head(55)
    df_physician_person_ratio.drop(df_physician_person_ratio.index[7], inplace=True)
    df_overdose.drop(df_overdose.index[7], inplace=True)
elif year_to_filter == "2017":
    df_physician_person_ratio = df_physician_person_ratio["2017"].head(55)
    df_overdose = df_overdose["2017"].head(55)
    df_physician_person_ratio.drop(df_physician_person_ratio.index[7], inplace=True)
    df_overdose.drop(df_overdose.index[7], inplace=True)
elif year_to_filter == "2018":
    df_physician_person_ratio = df_physician_person_ratio["2018"].head(55)
    df_overdose = df_overdose["2018"].head(55)
    df_physician_person_ratio.drop(df_physician_person_ratio.index[7], inplace=True)
    df_overdose.drop(df_overdose.index[7], inplace=True)
elif year_to_filter == "2019":
    df_physician_person_ratio = df_physician_person_ratio["2019"].head(55)
    df_overdose = df_overdose["2019"].head(55)
elif year_to_filter == "2020":
    df_physician_person_ratio = df_physician_person_ratio["2020"].head(55)
    df_overdose = df_overdose["2020"].head(55)
elif year_to_filter == "2021":
    df_physician_person_ratio = df_physician_person_ratio["2021"].head(55)
    df_overdose = df_overdose["2021"].head(55)
else:
    df_physician_person_ratio = df_physician_person_ratio["2022"].head(55)
    df_overdose = df_overdose["2022"].head(55)

# Set up visualization data frame
df_visual['access'] = df_physician_person_ratio
df_visual['overdoses'] = df_overdose

# Figure out which entries will be red vs. green based on whether they meet the cutoff 
nums = []
for entry in df_visual['access']:
    entry_no_commas = int(str(entry).replace(',', ''))
    num = 1 / entry_no_commas
    nums.append(num)
np_nums = np.array(nums)
np_cutoff = np.full(len(np_nums), cutoff, dtype=float)
df_visual['color'] = np.where(np_nums < np_cutoff, 'red', 'green')

# Create the scatter plot
fig = px.scatter(df_visual, df_physician_person_ratio, df_overdose)
fig.update_traces(hovertemplate=counties[df_physician_person_ratio.index] + '<br>%{x} people per physician<br>%{y} overdoses per 100,000 people')
fig.update_traces(marker=dict(color=df_visual['color']))
fig.update_xaxes(title_text='Healthcare Access')
fig.update_yaxes(title_text='Overdoses')
fig.update_layout(
    hoverlabel=dict(
        align="left"
    )
)

st.plotly_chart(fig, theme="streamlit")

footer="Sources: Global Health Data Exchange (GHDx), County Health Rankings and Roadmaps, San Francisco Chronicle, Centers for Disease Control and Prevention (CDC)"
st.markdown(footer)