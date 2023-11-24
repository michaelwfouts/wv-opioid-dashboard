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

# Visualization Explaination
st.write("# Healthcare Access vs. Overdoses Visualization")
st.markdown("""---""")

# load data
df_physician_person_ratio = pd.read_csv('/Users/arif/Desktop/wv-opioid-dashboard/data/WV Drug Epidemic Dataset.xlsx - Physicians Ratio (people_1 primary care physican).csv')
df_overdose = pd.read_csv('/Users/arif/Desktop/wv-opioid-dashboard/data/WV Drug Epidemic Dataset.xlsx - Drug Mortality (Per 100,000).csv')
df_visual = pd.DataFrame()

counties = df_physician_person_ratio.County

# average physician to person ratio:
# about 26 per 100,000 people
# https://www.amnhealthcare.com/blog/physician/perm/is-there-an-ideal-physician-to-population-ratio/
cutoff = 26 / 100000

# Use Slider to Select Year
year_to_filter = st.selectbox(
    'Select Year:',
    ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
)

if year_to_filter == "2013":
    df_physician_person_ratio = df_physician_person_ratio["2013"].head(55)
    df_overdose = df_overdose["2013"].head(55)
elif year_to_filter == "2014":
    df_physician_person_ratio = df_physician_person_ratio["2014"].head(55)
    df_overdose = df_overdose["2014"].head(55)
elif year_to_filter == "2015":
    df_physician_person_ratio = df_physician_person_ratio["2015"].head(55)
    df_overdose = df_overdose["2015"].head(55)
elif year_to_filter == "2016":
    df_physician_person_ratio = df_physician_person_ratio["2016"].head(55)
    df_overdose = df_overdose["2016"].head(55)
elif year_to_filter == "2017":
    df_physician_person_ratio = df_physician_person_ratio["2017"].head(55)
    df_overdose = df_overdose["2017"].head(55)
elif year_to_filter == "2018":
    df_physician_person_ratio = df_physician_person_ratio["2018"].head(55)
    df_overdose = df_overdose["2018"].head(55)
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

df_visual['access'] = df_physician_person_ratio
df_visual['overdoses'] = df_overdose
nums = []
for entry in df_physician_person_ratio:
    num = 1 / int(entry.replace(',', ''))
    nums.append(num)
np_nums = np.array(nums)
np_cutoff = np.full(len(np_nums), cutoff, dtype=float)
df_visual['color'] = np.where(np_nums < np_cutoff, 'green', 'red')
print(df_visual)
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