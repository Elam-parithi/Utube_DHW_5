"""
Data visualization page for showing plots and diagrams for the extracted data.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import text
import streamlit as st

sns.set_palette(sns.color_palette(["#4169E1", "#FFD700", "#6A5ACD", "#B22222", "#228B22"]))
union_alpha = 0.8


def get_query(selected_query):
    """
    Runs the query and returns a DataFrame.
    """
    if st.session_state["MySQL_URL"].is_connected:
        try:
            df = pd.read_sql_query(text(selected_query), st.session_state["MySQL_URL"].engine)
            if df.empty:
                st.warning("Query returned no data.")
            else:
                return df
        except Exception as e:
            st.error(f"Error executing query: {e}")


def plotting_bar(fig_point, x_label, y_label, dataframe):
    """
    plotting for bar plot with empty labels and xticks.
    @param fig_point: axes point
    @param x_label: label for x
    @param y_label: label for y
    @param dataframe: dataframe for plot
    """
    if x_label not in dataframe.columns:
        raise ValueError(f"'{x_label}' column is not found in the dataframe.")
    palette = sns.color_palette("husl", len(dataframe))  # Generate a color palette
    sns.barplot(x=x_label, y=y_label, data=dataframe, dodge=False, hue=x_label,
                palette=palette, ax=fig_point, alpha=union_alpha, legend=True)
    fig_point.legend(fontsize=6, title_fontsize=8)
    fig_point.set_xlabel("")
    fig_point.set_xticks([])
    fig_point.set_ylabel(y_label)


def analyze_page():
    st.subheader("Channel-wise Analysis")

    query = """
    SELECT c.channel_name, 
       c.channel_views AS 'Channel Views',
       COUNT(DISTINCT v.video_id) AS 'Video Count', 
       COUNT(DISTINCT p.playlist_id) AS 'Playlist Count'
    FROM channels c
    LEFT JOIN playlists p ON c.channel_id = p.channel_id
    LEFT JOIN videos v ON c.channel_id = v.channel_id
    GROUP BY c.channel_name, c.channel_views;"""
    data_df = get_query(query)

    avg_query = """SELECT 
        c.channel_name,
        AVG(v.duration) AS 'Average duration',
        SUM(v.duration) AS 'Total duration',
        COUNT(com.comment_id) AS 'Total comments'
    FROM channels c
    LEFT JOIN videos v ON c.channel_id = v.channel_id
    LEFT JOIN comments com ON v.video_id = com.video_id
    GROUP BY c.channel_id, c.channel_name
    ORDER BY 'Average duration' DESC, 'Total duration' DESC, 'Total comments' DESC;"""

    sns.set_style("whitegrid")
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharey=False)

    plotting_bar(axes[0, 0], 'channel_name', 'Video Count', data_df)
    axes[0, 0].set_title('Total Number of Videos in Each Channel')
    plotting_bar(axes[0, 1], 'channel_name', 'Playlist Count', data_df)
    axes[0, 1].set_title('Total Number of Playlists in Each Channel')
    plotting_bar(axes[0, 2], 'channel_name', 'Channel Views', data_df)
    axes[0, 2].set_title('Total Number of Viewers in Each Channel')

    avg_df = get_query(avg_query)
    plotting_bar(axes[1, 0], 'channel_name', 'Average duration', avg_df)
    axes[1, 0].set_title('Average Duration (sec) of Each Channel')
    plotting_bar(axes[1, 1], 'channel_name', 'Total duration', avg_df)
    axes[1, 1].set_title('Total Video Duration (sec) of Each Channel')
    plotting_bar(axes[1, 2], 'channel_name', 'Total comments', avg_df)
    axes[1, 2].set_title('Total Comments of Each Channel')

    plt.tight_layout()
    st.pyplot(plt)

    st.subheader("Playlist-wise Analysis")
    # Top 5 most viewed playlist and its average sentiment.
    playlist_query = """
    SELECT p.playlist_name, SUM(v.view_count) AS total_view_count, AVG(c.sentiment) AS average_sentiment
    FROM (SELECT video_id, playlist_id, view_count FROM videos
         ORDER BY view_count DESC LIMIT 5) v
    JOIN playlists p ON v.playlist_id = p.playlist_id
    LEFT JOIN comments c ON v.video_id = c.video_id
    GROUP BY p.playlist_name ORDER BY total_view_count DESC;
    """
    playlist_df = get_query(playlist_query)
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    # First plot: Sentiment vs View Count
    sns.scatterplot(data=playlist_df, x='total_view_count', y='average_sentiment', hue='playlist_name', palette='deep',
                    ax=axes[0])
    axes[0].set_title('Sentiment vs View Count')
    axes[0].set_xlabel('Total View Count')
    axes[0].set_ylabel('Average Sentiment')

    # Second plot: Total View Count per Playlist
    sns.barplot(data=playlist_df, x='playlist_name', y='total_view_count', palette='deep', ax=axes[1])
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].set_title('Total View Count top 5 viewed Playlist')
    axes[1].set_xlabel('Playlist Name')
    axes[1].set_ylabel('Total View Count')

    # Third plot: Average Sentiment per Playlist
    sns.barplot(data=playlist_df, x='playlist_name', y='average_sentiment', palette='deep', ax=axes[2])
    axes[2].tick_params(axis='x', rotation=45)
    axes[2].set_title('Average Sentiment top 5 viewed Playlist')
    axes[2].set_xlabel('Playlist Name')
    axes[2].set_ylabel('Average Sentiment')

    plt.tight_layout()
    st.pyplot(plt)

    st.subheader("Video-wise Data")
    # video query
    video_query = """
    SELECT v.video_id, v.video_name, v.view_count, AVG(c.sentiment) AS average_sentiment FROM videos v
    LEFT JOIN comments c ON v.video_id = c.video_id
    GROUP BY v.video_id ORDER BY v.view_count DESC LIMIT 5;
    """
    video_df = get_query(video_query)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    palette = sns.color_palette("husl", len(video_df))  # Generate a color palette
    sns.barplot(x='video_id', y='view_count', data=video_df, ax=axes[0],
                hue='video_id', palette=palette, alpha=union_alpha)
    axes[0].set_title('View Count of top 5 viewed Videos')
    axes[0].set_ylabel('View Count')
    axes[0].set_xlabel('Video ID')

    sns.barplot(x='video_id', y='average_sentiment', data=video_df, ax=axes[1],
                hue='video_id', palette=palette, alpha=union_alpha)
    axes[1].set_title('Average Sentiment of top 5 viewed Videos')
    axes[1].set_ylabel('Average Sentiment')
    axes[1].set_xlabel('Video ID')

    plt.tight_layout()
    st.pyplot(plt)

    st.subheader("Comment Sentiment Data")
    # sentiment query
    sentiment_query = """
        SELECT c.channel_name, cm.sentiment FROM channels c
        JOIN videos v ON c.channel_id = v.channel_id
        JOIN comments cm ON v.video_id = cm.video_id
        ORDER BY c.channel_name, cm.sentiment;
        """
    sentiment_df = get_query(sentiment_query)
    if sentiment_df is not None:
        fig, axes = plt.subplots(1, 2, figsize=(15, 8), sharey=False)
        # palette = sns.color_palette("husl", len(dataframe))  # Generate a color palette
        sns.histplot(
            data=sentiment_df, x='sentiment', hue='channel_name', kde=True,
            bins=30, palette='tab10', ax=axes[0], legend=True)
        axes[0].set_title("Distribution of Sentiment Scores by Channel")
        axes[0].set_xlabel("Sentiment Score")
        axes[0].set_ylabel("Frequency")
        sns.violinplot(data=sentiment_df, x="channel_name", y="sentiment", palette="pastel",
                       ax=axes[1], hue="channel_name", legend=False)
        axes[1].set_title('Violin Plot: Sentiment Distribution per Channel')
        axes[1].tick_params(axis='x', rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
