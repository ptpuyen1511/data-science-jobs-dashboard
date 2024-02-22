# Inspired from a tutorial "Building a dashboard in Python using Streamlit" (By Chanin Nantasenamat)

# Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.patches as mpatches

# Page configuration
st.set_page_config(page_title='US Data Science Jobs Dashboard', page_icon=':bar_chart:', layout='wide')


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
def make_barh_skills_chart(jobs_df):
    skill_counts = pd.DataFrame(jobs_df['job_skills'].str.split(', ', expand=False).values.tolist()).stack().value_counts()
    top_5_skills = skill_counts.head(5).index.to_list()[:5]

    _, axes = plt.subplots(4, 1)
    levels = ['Principle/Head/Manager', 'Lead Data Science/Scientist', 'Senior Data Science/Scientist', 'Data Science/Scientist']
    colors = ['tab:pink', 'tab:blue', 'tab:orange', 'tab:cyan']

    for i, l in enumerate(levels):
        ax = pd.DataFrame(jobs_df[jobs_df['job_level'] == l]['job_skills'].str.split(', ', expand=False).values.tolist()).stack().loc[lambda x: ~x.str.contains('|'.join(top_5_skills))].value_counts().head(5).sort_values().plot.barh(ax=axes[i], color=colors[i], legend=False)
        axes[i].bar_label(axes[i].containers[0])
        axes[i].get_xaxis().set_ticks([])
        axes[i].set_frame_on(False)

    labels = [mpatches.Patch(color=c) for c in colors]
    plt.legend(labels, levels, ncol=1, loc='lower right', fontsize=5)

    return plt

# Dashboard Main Panel
st.markdown("<h3 style='text-align: center; color: black;'>US Data Science Jobs Dashboard</h1>", unsafe_allow_html=True)

row1_col = st.columns(2) # Two columns with equal width

with row1_col[0]:
    st.markdown('#### Jobs by Location')

with row1_col[1]:
    st.markdown('#### Jobs by Level')
    barh_chart_ax = make_barh_chart(jobs_df)
    st.pyplot(barh_chart_ax.figure, use_container_width=True)
    plt.figure()


row2_col = st.columns(2) # Two columns with equal width

with row2_col[0]:
    st.markdown('#### Top 20 Needed Skills')
    wc_chart_plt = make_wordcloud_chart(jobs_df)
    st.pyplot(fig=wc_chart_plt, use_container_width=True)
    plt.figure()

with row2_col[1]:
    st.markdown('#### Top 5 Skills by Level*')
    st.markdown('**After removing top 5 skills from top 20*')
    barh_skills_chart_plt = make_barh_skills_chart(jobs_df)
    st.pyplot(fig=barh_skills_chart_plt, use_container_width=True)
