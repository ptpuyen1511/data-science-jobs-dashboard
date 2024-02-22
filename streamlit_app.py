# Inspired from a tutorial "Building a dashboard in Python using Streamlit" (By Chanin Nantasenamat)

# Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Page configuration
st.set_page_config(page_title="US Data Science Jobs Dashboard", page_icon=":bar_chart:", layout="wide")


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
    ax.set_frame_on(False)

    return ax

## WordCloud (top 20 needed skills) and Top 5 words (top 5 needed skills)
def make_wordcloud_chart(jobs_df):
    skill_counts = pd.DataFrame(jobs_df['job_skills'].str.split(', ', expand=False).values.tolist()).stack().value_counts()
    skills_freq = skill_counts.head(20)

    all_wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(skills_freq)
    plt.axis('off')
    plt.imshow(all_wc, interpolation='bilinear')

    return plt


##  Barh charts (count skills by levels)

# Dashboard Main Panel
st.markdown('## US Data Science Jobs Dashboard')

col = st.columns(2) # Two columns with equal width

with col[0]:
    st.markdown('### Jobs by Location')
    

    st.markdown('### Jobs by Level')
    # barh_chart = make_barh_chart(jobs_df)
    # st.pyplot(barh_chart.figure)

with col[1]:
    st.markdown('### Top 20 Needed Skills')
    wc_chart = make_wordcloud_chart(jobs_df)
    st.pyplot(fig=wc_chart)

    st.markdown('### Top 5 Need Skills by Level')