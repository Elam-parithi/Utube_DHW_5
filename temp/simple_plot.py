# Streamlit Dashboard for YouTube Data Analysis
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv(r'/.secrets')
db_precon = getenv('pre_conn')
DB_name = getenv('DB_NAME')

# Database connection
connection_string = f"{db_precon}{DB_name}"
print("connection_string")
engine = create_engine(connection_string)

# Streamlit app
st.title("YouTube Data Analysis Dashboard")


# Helper function to execute SQL queries and fetch data
def fetch_data(query):
    with engine.connect() as connection:
        return pd.read_sql(query, connection)


# Queries for different tables
channel_query = "SELECT * FROM channels"
playlist_query = "SELECT * FROM playlists"
video_query = "SELECT * FROM videos"
comment_query = "SELECT * FROM comments"

# Load data
st.sidebar.header("Load Data")
if st.sidebar.button("Load Channels Data"):
    df_channels = fetch_data(channel_query)
    st.write("Channels Data", df_channels)

if st.sidebar.button("Load Playlists Data"):
    df_playlists = fetch_data(playlist_query)
    st.write("Playlists Data", df_playlists)

if st.sidebar.button("Load Videos Data"):
    df_videos = fetch_data(video_query)
    st.write("Videos Data", df_videos)

if st.sidebar.button("Load Comments Data"):
    df_comments = fetch_data(comment_query)
    st.write("Comments Data", df_comments)

# Visualization: Channel Overview
st.header("Channel Overview")
if 'df_channels' in locals():
    st.subheader("Total Views Per Channel")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="channel_name", y="channel_views", data=df_channels)
    plt.xticks(rotation=45)
    plt.title("Total Views Per Channel")
    st.pyplot(plt)

# Visualization: Video Insights
st.header("Video Insights")
if 'df_videos' in locals():
    st.subheader("Views Distribution by Video")
    plt.figure(figsize=(10, 6))
    sns.histplot(df_videos['view_count'], kde=True, bins=30)
    plt.title("Distribution of Video Views")
    st.pyplot(plt)

    st.subheader("Top 10 Videos by View Count")
    top_videos = df_videos.nlargest(10, "view_count")[["video_name", "view_count"]]
    st.bar_chart(top_videos.set_index("video_name"))

    st.subheader("Likes vs. Dislikes")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="like_count", y="dislike_count", hue="channel_id", data=df_videos)
    plt.title("Likes vs Dislikes")
    st.pyplot(plt)

# Visualization: Sentiment Analysis
st.header("Comment Sentiment Analysis")
if 'df_comments' in locals():
    st.subheader("Sentiment Distribution")
    plt.figure(figsize=(10, 6))
    sns.countplot(x="sentiment_type", data=df_comments)
    plt.title("Sentiment Type Distribution")
    st.pyplot(plt)

    st.subheader("Average Sentiment Score by Video")
    avg_sentiment = df_comments.groupby("video_id")["sentiment"].mean().reset_index()
    st.bar_chart(avg_sentiment.set_index("video_id"))

# Video Duration Insights
st.header("Video Duration Analysis")
if 'df_videos' in locals():
    st.subheader("Distribution of Video Durations")
    plt.figure(figsize=(10, 6))
    sns.histplot(df_videos["duration"], kde=True, bins=30)
    plt.title("Video Duration Distribution")
    st.pyplot(plt)

# Closing the database connection
engine.dispose()
