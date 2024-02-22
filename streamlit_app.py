# Inspired from a tutorial "Building a dashboard in Python using Streamlit" (By Chanin Nantasenamat)

# Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="US Data Science Jobs Dashboard", page_icon=":bar_chart:", layout="wide")
st.theme('light')


# Load preprocessed dataset
jobs_df = pd.read_csv('data/preprocessed_jobs.csv')

# Plots
## Symbol map (count jobs by location)

## Barh chart (count jobs by level)
def make_barh_chart(jobs_df):
    count_jobs_df = pd.DataFrame(jobs_df.groupby(['job_level']).size().sort_values(ascending=True)).reset_index().rename(columns={0: 'count'}).set_index('job_level')
    
    ax = count_jobs_df.plot.barh(title='', legend=False)
    ax.set_xlabel('Count')
    ax.set_ylabel('Job Level')
    ax.bar_label(ax.containers[0])

    return ax

## WordCloud (top 20 needed skills) and Top 5 words (top 5 needed skills)

##  Barh charts (count skills by levels)

# Dashboard Main Panel
col = st.columns(2) # Two columns with equal width

with col[0]:
    st.markdown('### Jobs by Location')
    

    st.markdown('### Jobs by Level')
    barh_chart = make_barh_chart(jobs_df)
    st.pyplot(barh_chart.figure)

with col[1]:
    st.markdown('### Top 20 Needed Skills')

    st.markdown('### Top 5 Need Skills by Level')