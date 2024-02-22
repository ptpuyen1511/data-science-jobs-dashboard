# Inspired from a tutorial "Building a dashboard in Python using Streamlit" (By Chanin Nantasenamat)

# Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.patches as mpatches
import plotly.express as px

# Page configuration
st.set_page_config(page_title='US Data Science Jobs Dashboard', page_icon=':bar_chart:', layout='wide')


# Load preprocessed dataset
jobs_df = pd.read_csv('data/preprocessed_jobs.csv')
long_lat_df = pd.read_csv('data/state_us.csv')
two_letters_state_df = pd.read_csv('data/2_letters_state_us.csv')

# Plots
## Symbol map (count jobs by location)
def make_symbol_map(jobs_df, long_lat_df, two_letters_state_df):
    df = pd.DataFrame(jobs_df.groupby('job_loc_state').size()).rename(columns={0: 'count'}).reset_index()
    jobs_count_df = df[df['job_loc_state'].str.len() == 2].copy()
    merged_df = jobs_count_df.merge(long_lat_df.merge(two_letters_state_df, left_on='State', right_on='State/Territory'), left_on='job_loc_state', right_on='Abbreviation')
    
    fig = px.scatter_geo(merged_df, lat='Latitude', lon='Longitude',hover_name='State', size='count', scope='usa', color_discrete_sequence=[px.colors.qualitative.Plotly[8]])
    fig.update_layout(margin={'t':0, 'b': 0, 'l': 0, 'r': 0})

    return fig


## Barh chart (count jobs by level)
def make_barh_chart(jobs_df):
    count_jobs_df = pd.DataFrame(jobs_df.groupby(['job_level']).size().sort_values(ascending=True)).reset_index().rename(columns={0: 'count'}).set_index('job_level')
    
    ax = count_jobs_df.plot.barh(title='', legend=False, color='deepskyblue')
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

    return plt, skill_counts.head(5).index.to_list()[:5]


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
st.markdown('<h2 style="text-align: center; color: black; background-color: #9ec3ff;">US Data Science Jobs Dashboard</h2>', unsafe_allow_html=True)
st.write('')

row1_col = st.columns(2)

with row1_col[0]:
    container = st.container(border=True)
    container.markdown('<h4 style="text-align: center; color: black; background-color: #9ec3ff;">Jobs by Location</h4>', unsafe_allow_html=True)
    # st.markdown('#### Jobs by Location')
    symbol_map_fig = make_symbol_map(jobs_df, long_lat_df, two_letters_state_df)
    container.plotly_chart(symbol_map_fig, use_container_width=True)
    plt.figure()

with row1_col[1]:
    container = st.container(border=True)
    container.markdown('<h4 style="text-align: center; color: black; background-color: #9ec3ff;">Detailed Jobs Dataframe</h4>', unsafe_allow_html=True)
    # st.markdown('#### Detailed Jobs Dataframe')
    query = container.text_input('Search ...')
    jobs_clone_df = jobs_df[['job_link', 'job_title', 'company', 'job_location', 'job_type', 'job_skills']].copy()
    if query:
        mask = jobs_clone_df.applymap(lambda x: query.lower() in str(x).lower()).any(axis=1)
        jobs_clone_df = jobs_clone_df[mask]

    container.dataframe(jobs_clone_df,
                        hide_index=True,
                        column_config={
                            'job_link': st.column_config.LinkColumn('Job Link'), 'job_title': 'Job Title', 'company': 'Company', 'job_location': 'Job Location', 'job_type': 'Job Type', 'job_skills': 'Job Skills'},
                        column_order=('Job Title', 'Company', 'Job Type', 'Job Location', 'Job Skills', 'Job Link'),
                        use_container_width=True)

row2_col = st.columns(3) # 3 columns with equal width

with row2_col[0]:
    container = st.container(border=True)
    container.markdown('<h4 style="text-align: center; color: black; background-color: #9ec3ff;">Jobs by Level</h4>', unsafe_allow_html=True)
    # st.markdown('#### Jobs by Level')
    barh_chart_ax = make_barh_chart(jobs_df)
    container.pyplot(barh_chart_ax.figure, use_container_width=True)
    plt.figure()

with row2_col[1]:
    container = st.container(border=True)
    container.markdown('<h4 style="text-align: center; color: black; background-color: #9ec3ff;">Top 20 Needed Skills</h4>', unsafe_allow_html=True)
    # st.markdown('#### Top 20 Needed Skills')
    wc_chart_plt, top_5 = make_wordcloud_chart(jobs_df)
    container.markdown(f'**Top 5 skills: {", ".join(top_5)}**')
    container.pyplot(fig=wc_chart_plt, use_container_width=True)
    plt.figure()
    

with row2_col[2]:
    container = st.container(border=True)
    container.markdown('<h4 style="text-align: center; color: black; background-color: #9ec3ff;">Top 5 Skills by Level*</h4>', unsafe_allow_html=True)
    # st.markdown('#### Top 5 Skills by Level*')
    barh_skills_chart_plt = make_barh_skills_chart(jobs_df)
    container.markdown('**After removing top 5 skills from top 20*')
    container.pyplot(fig=barh_skills_chart_plt, use_container_width=True)
