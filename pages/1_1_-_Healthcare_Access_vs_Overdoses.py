import streamlit as st
import pandas as pd

# Set the page title
st.set_page_config(
    page_title="Healthcare Access vs. Overdoses",
    page_icon="🏥",
    layout="centered",
)

# load data
df_physician_person_ratio = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Physicians Ratio (people_1 primary care physican).csv')
df_overdose = pd.read_csv('data/WV Drug Epidemic Dataset.xlsx - Drug Mortality (Per 100,000).csv')

# TODO:
# scatterplot -- physician/person ratio x axis, drug mortality y axis
# each point = county
# maybe color dots red if they are considered low physician ratio? check what this number is 