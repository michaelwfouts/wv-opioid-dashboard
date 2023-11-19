import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

import streamlit as st

# Page title and description
st.title("Exploring the Opioid Epidemic in West Virginia")
st.write(
    "Welcome to our data exploration tool for the opioid epidemic in West Virginia. This Streamlit app is part of our CS 560 project, "
    "which aims to provide insights into the devastating impact of the opioid crisis in this region. By analyzing various metrics and "
    "data points, we hope to shed light on the complex nature of the epidemic and its consequences on the state's communities."
)

# Subheading
st.subheader("Project Objectives:")
st.markdown(
    "- **Analyze Key Metrics**: We will examine important metrics such as drug usage, poverty, and treatment access."
)
st.markdown(
    "- **Visualize Data**: Utilize interactive charts and maps to visualize data, making it easier to understand the trends and patterns."
)
st.markdown(
    "- **Raise Awareness**: Our goal is to increase awareness of the opioid epidemic's impact on West Virginia and contribute to ongoing efforts to combat it."
)

# Data sources
st.subheader("Data Sources:")
st.markdown(
    "We have collected data from various sources, including government agencies, healthcare providers, and research organizations. "
    "Our app integrates this data to provide a comprehensive view of the situation. Specific sources will be referenced in the final version of the app."
)

# Get started
st.subheader("Let's Get Started:")
st.write(
    "We invite you to explore the opioid epidemic data in West Virginia. "
    "Use the menu on the left to begin your journey, and feel free to interact with the visualizations, filters, and tools available. "
    "If you have any questions or need assistance, please don't hesitate to reach out to our team."
)

# Project team and contact
st.subheader("Project Team:")
st.write(
    "This project was developed by the CS 560 team at West Virginia University. "
    "If you have questions, feedback, or would like to get in touch with us, please contact:"
)
st.markdown(
    "- **Michael Fouts**: mwfouts@mix.wvu.edu"
)
st.markdown(
    "- **Emily Herrick**: emherrick@mix.wvu.edu"
)
st.markdown(
    "- **Kevin Reisch**: krr00021@mix.wvu.edu"
)
st.markdown(
    "- **Sadaf Sarwari**: sas0004@mix.wvu.edu"
)

# Footer
st.write("Thank you for using our app. Together, we can better understand and address the opioid epidemic in West Virginia.")
