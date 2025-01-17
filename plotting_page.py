# plotting_page.py
"""
Data visualization page for showing plots and diagrams for the extracted data.
"""
import pandas as pd
import seaborn as sns
from sqlalchemy import text
import matplotlib.pyplot as plt
from config_and_auxiliary import *


def get_query(selected_query):
    """
    Runs the query and returns the pd.Dataframe.
    @param selected_query: query text
    @return: pd.DataFrame
    """
    if st.session_state["MySQL_URL"].is_connected:
        try:
            df = pd.read_sql_query(text(selected_query),
                                   st.session_state["MySQL_URL"].engine)
            if df.empty:
                print("Returned no DATA")
            else:
                return df
        except Exception as e:
            print(f"Error executing query: {e}")


def analyze_page():
    """
        In this page instead of getting the data directly it will get the last 10 data from the MySQL DB
        which is extracted from Home page and stored in the database mentioned above.
    """
    st.subheader("Plots and Diagrams:")

    query = """
    SELECT 
    c.channel_name,
    COUNT(DISTINCT v.video_id) AS video_count,
    COUNT(DISTINCT p.playlist_id) AS playlist_count
    FROM 
        channels c
    LEFT JOIN 
        playlists p ON c.channel_id = p.channel_id
    LEFT JOIN 
        videos v ON c.channel_id = v.channel_id
    GROUP BY 
        c.channel_name;"""
    data_df = get_query(query)
    sns.set_style("whitegrid")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    palette = sns.color_palette("husl", len(data_df))  # Generate a color palette
    sns.barplot(x='channel_name', y='video_count', data=data_df, palette=palette, ax=ax)

    # Customize the plot
    for container, color in zip(ax.containers, palette):
        for bar in container:
            bar.set_edgecolor("black")

    # Add legend for colors instead of x-axis names
    handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in palette]
    labels = data_df['channel_name'].tolist()
    ax.legend(handles, labels, title="Channel Names", loc='upper right')

    ax.set_xlabel('Channel Name')
    ax.set_ylabel('Video Count')
    ax.set_title('Total Number of Videos in Each Channel')
    st.pyplot(fig)


