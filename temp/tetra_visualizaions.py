import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

from dotenv import load_dotenv
from os import getenv
load_dotenv('../.secrets')
schema = getenv('DB_NAME')
pre_con = getenv('pre_conn')
DATABASE_URL = f'{pre_con}{schema}'

engine = create_engine(DATABASE_URL)


# Fetch data from tables
@st.cache_data
def load_data():
    channels = pd.read_sql("SELECT * FROM channels LIMIT 5000", engine)
    playlists = pd.read_sql("SELECT * FROM playlists LIMIT 5000", engine)
    videos = pd.read_sql("SELECT * FROM videos LIMIT 10000", engine)
    comments = pd.read_sql("SELECT * FROM comments LIMIT 10000", engine)
    return channels, playlists, videos, comments



# Load data into DataFrames
channels, playlists, videos, comments = load_data()

st.title("Video Platform Data Visualization")

# Create tabs for better organization
tab1, tab2, tab3, tab4 = st.tabs(["Channels", "Playlists", "Videos", "Comments"])

# Tab 1: Channel Visualizations
with tab1:
    st.header("Channel Data Overview")

    col1, col2 = st.columns(2)

    # Plot 1: Channel Type Distribution
    with col1:
        st.subheader("Channel Type Distribution")
        fig, ax = plt.subplots()
        sns.countplot(data=channels, y='channel_type', palette='viridis', ax=ax)
        st.pyplot(fig)

    # Plot 2: Top 10 Channels by Views
    with col2:
        st.subheader("Top 10 Channels by Views")
        top_channels = channels.nlargest(10, 'channel_views')
        fig, ax = plt.subplots()
        sns.barplot(data=top_channels, x='channel_views', y='channel_name', palette='coolwarm')
        st.pyplot(fig)

# Tab 2: Playlist Visualizations
with tab2:
    st.header("Playlist Data Overview")

    # Plot: Number of Playlists per Channel
    st.subheader("Number of Playlists per Channel")
    playlists_count = playlists['channel_id'].value_counts().reset_index()
    playlists_count.columns = ['channel_id', 'playlist_count']
    merged_data = pd.merge(playlists_count, channels[['channel_id', 'channel_name']], on='channel_id')

    fig, ax = plt.subplots()
    sns.barplot(data=merged_data, x='playlist_count', y='channel_name', palette='magma')
    st.pyplot(fig)

# Tab 3: Video Visualizations
with tab3:
    st.header("Video Data Overview")

    col1, col2 = st.columns(2)

    # Plot 1: Video Views Distribution
    with col1:
        st.subheader("Video Views Distribution")
        fig, ax = plt.subplots()
        sns.histplot(videos['view_count'], bins=30, kde=True, color='green')
        st.pyplot(fig)

    # Plot 2: Average Duration per Channel
    with col2:
        st.subheader("Average Video Duration per Channel")
        avg_duration = videos.groupby('channel_id')['duration'].mean().reset_index()
        avg_duration = pd.merge(avg_duration, channels[['channel_id', 'channel_name']], on='channel_id')

        fig, ax = plt.subplots()
        sns.barplot(data=avg_duration, x='duration', y='channel_name', palette='plasma')
        st.pyplot(fig)

# Tab 4: Comment Visualizations
with tab4:
    st.header("Comment Data Overview")

    # Plot: Sentiment Analysis Distribution
    st.subheader("Comment Sentiment Distribution")
    fig, ax = plt.subplots()
    sns.countplot(data=comments, x='sentiment_type', palette='cool')
    st.pyplot(fig)

    # Display random comments
    st.subheader("Random Sample of Comments")
    st.dataframe(comments.sample(10)[['comment_author', 'comment_text', 'sentiment_type']])
