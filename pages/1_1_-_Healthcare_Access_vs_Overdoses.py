import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# Set the page title
st.set_page_config(
    page_title="Healthcare Access vs. Overdoses",
    page_icon="🏥",
    layout="centered",
)

# load data CHANGE THESE PATHS BEFORE COMMITTING!!!!!!!!!!!!!!!!
df_physician_person_ratio = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Physicians Ratio (people_1 primary care physican).csv')
df_overdose = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Drug Mortality (Per 100,000).csv')

counties = df_physician_person_ratio.County

df_physician_person_ratio_2013 = df_physician_person_ratio["2013"].head(55)
df_physician_person_ratio_2014 = df_physician_person_ratio["2014"].head(55)
df_physician_person_ratio_2015 = df_physician_person_ratio["2015"].head(55)
df_physician_person_ratio_2016 = df_physician_person_ratio["2016"].head(55)
df_physician_person_ratio_2017 = df_physician_person_ratio["2017"].head(55)
df_physician_person_ratio_2018 = df_physician_person_ratio["2018"].head(55)
df_physician_person_ratio_2019 = df_physician_person_ratio["2019"].head(55)
df_physician_person_ratio_2020 = df_physician_person_ratio["2020"].head(55)
df_physician_person_ratio_2021 = df_physician_person_ratio["2021"].head(55)
df_physician_person_ratio_2022 = df_physician_person_ratio["2022"].head(55)


df_overdose_2013 = df_overdose["2013"].head(55)
df_overdose_2014 = df_overdose["2014"].head(55)
df_overdose_2015 = df_overdose["2015"].head(55)
df_overdose_2016 = df_overdose["2016"].head(55)
df_overdose_2017 = df_overdose["2017"].head(55)
df_overdose_2018 = df_overdose["2018"].head(55)
df_overdose_2019 = df_overdose["2019"].head(55)
df_overdose_2020 = df_overdose["2020"].head(55)
df_overdose_2021 = df_overdose["2021"].head(55)
df_overdose_2022 = df_overdose["2022"].head(55)

# Use Slider to Select Year
year_to_filter = st.selectbox(
    'Select Year:',
    ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
)

if year_to_filter == "2013":
    fig = px.scatter(df_physician_person_ratio_2013, df_overdose_2013)
    fig.update_traces(hovertemplate=counties[df_physician_person_ratio_2013.index])
elif year_to_filter == "2014":
    fig = px.scatter(df_physician_person_ratio_2014, df_overdose_2014)
    fig.update_traces(hovertemplate=counties[df_physician_person_ratio_2014.index])
elif year_to_filter == "2015":
    fig = px.scatter(df_physician_person_ratio_2015, df_overdose_2015)
    fig.update_traces(hovertemplate=counties[df_physician_person_ratio_2015.index])
elif year_to_filter == "2016":
    fig = px.scatter(df_physician_person_ratio_2016, df_overdose_2016)
    fig.update_traces(hovertemplate=counties[df_physician_person_ratio_2016.index])
elif year_to_filter == "2017":
    fig = px.scatter(df_physician_person_ratio_2017, df_overdose_2017)
    fig.update_traces(hovertemplate=counties[df_physician_person_ratio_2017.index])
elif year_to_filter == "2018":
    fig = px.scatter(df_physician_person_ratio_2018, df_overdose_2018)
    fig.update_traces(hovertemplate=counties[df_physician_person_ratio_2018.index])
elif year_to_filter == "2019":
    fig = px.scatter(df_physician_person_ratio_2019, df_overdose_2019)
    fig.update_traces(hovertemplate=counties[df_physician_person_ratio_2019.index])
elif year_to_filter == "2020":
    fig = px.scatter(df_physician_person_ratio_2020, df_overdose_2020)
    fig.update_traces(hovertemplate=counties[df_physician_person_ratio_2020.index])
elif year_to_filter == "2021":
    fig = px.scatter(df_physician_person_ratio_2021, df_overdose_2021)
    fig.update_traces(hovertemplate=counties[df_physician_person_ratio_2021.index])
else:
    fig = px.scatter(df_physician_person_ratio_2022, df_overdose_2022)
    fig.update_traces(hovertemplate=counties[df_physician_person_ratio_2022.index])

fig.update_xaxes(title_text='Physician to Person Ratio')
fig.update_yaxes(title_text='Drug Mortality Per 100,000')
fig.update_layout(
    hoverlabel=dict(
        align="left"
    )
)

# TODO:
# maybe color dots red if they are considered low physician ratio? check what this number is 

st.plotly_chart(fig, theme="streamlit")