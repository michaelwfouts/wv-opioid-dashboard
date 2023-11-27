import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import math

# Set the page title
st.set_page_config(
    page_title="Industry vs Drug Usage",
    page_icon="🚧",
    layout="centered",
)

# Page Content
st.write("# Page Under Construction")
st.write("This page is currently under construction.  Please check back later for updates")

# Visualization Explanation
st.write("# Regional Industry vs. Drug Usage")
st.markdown("""---""")

# load data
df_employ_const_ext = pd.read_csv('/Users/emily/Documents/GitHub/wv-opioid-dashboard/data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs- Construction&Extraction .csv')
df_employ_farm_fish_forest = pd.read_csv('/Users/emily/Documents/GitHub/wv-opioid-dashboard/data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Farm&Fish&Forest.csv')
df_employ_install_mainten_repair = pd.read_csv('/Users/emily/Documents/GitHub/wv-opioid-dashboard/data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Install&Mainten&Repair.csv')
df_employ_production = pd.read_csv('/Users/emily/Documents/GitHub/wv-opioid-dashboard/data/WV Drug Epidemic Dataset.xlsx - Employment per 1000 jobs - Production.csv')
df_drug_usage = pd.read_csv('/Users/emily/Documents/GitHub/wv-opioid-dashboard/data/WV Drug Epidemic Dataset.xlsx - Opioid Dispensing Rate per 100.csv')
df_visual = pd.DataFrame()

counties = df_employ_const_ext.County

# Use Slider to Select Year
year_to_filter = st.selectbox(
    'Select Year:',
    ["2019", "2020", "2021", "2022"]
)

if year_to_filter == "2019":
    df_employ_const_ext = df_employ_const_ext["2019"].head(55)
    df_drug_usage = df_drug_usage["2019"].head(55)

elif year_to_filter == "2020":
    df_employ_const_ext = df_employ_const_ext["2020"].head(55)
    df_drug_usage = df_drug_usage["2020"].head(55)

elif year_to_filter == "2021":
    df_employ_const_ext = df_employ_const_ext["2021"].head(55)
    df_drug_usage = df_drug_usage["2021"].head(55)

else:
    df_employ_const_ext = df_employ_const_ext["2022"].head(55)
    df_drug_usage = df_drug_usage["2022"].head(55)


