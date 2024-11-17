# sql_analysis.py
"""
This is for Querying the SQL table and getting the output.
"""

# Import necessary libraries and functions

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text


def get_sqlalchemy_engine():
    return create_engine(st.session_state["mysql_config"])


# todo:create a separate query file for all the SQL query here.

query_list = [
    'Select your Question',
    '1. What are the names of all the videos and their corresponding channels?',
    '2. Which channels have the most number of videos, and how many videos do they have?',
    '3. What are the top 10 most viewed videos and their respective channels?',
    '4. How many comments were made on each video, and what are their corresponding video names?',
    '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
    '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
    '7. What is the total number of views for each channel, and what are their corresponding channel names?',
    '8. What are the names of all the channels that have published videos in the year 2022?',
    '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
    '10. Which videos have the highest number of comments, and what are their corresponding channel names?'
]


def query_sql():
    selection = st.selectbox('Select your Question', options=query_list)
    sql_query = None
    columns = []

    if selection == query_list[1]:
        sql_query = ("""SELECT channels.channel_name, videos.video_name FROM videos 
        JOIN channels ON channels.channel_id = videos.channel_id
        ORDER BY channels.channel_name;""")
        columns = ['Channel Name', 'Video Name']

    elif selection == query_list[2]:
        sql_query = ("""
        SELECT DISTINCT channels.channel_name, COUNT(Videos.video_id) AS Total_Videos FROM channels 
        JOIN Videos ON channels.channel_id = Videos.channel_id GROUP BY channels.channel_name 
        ORDER BY Total_Videos DESC;""")
        columns = ['Channel Name', 'Total Videos']

    elif selection == query_list[3]:
        sql_query = ("""SELECT channels.channel_name, Videos.video_name, Videos.view_count AS Total_Views FROM Videos
        JOIN channels ON channels.channel_id = Videos.channel_id
        ORDER BY Videos.view_count DESC LIMIT 10;""")
        columns = ['Channel Name', 'Video Name', 'Total Views']

    elif selection == query_list[4]:
        sql_query = ("""SELECT videos.video_name, videos.comment_count AS Total_Comments FROM videos
        ORDER BY videos.comment_count DESC; """)
        columns = ['Video Name', 'Total Comments']

    elif selection == query_list[5]:
        sql_query = ("""SELECT channels.channel_name, videos.video_name, videos.like_count AS Highest_Likes FROM videos 
        JOIN channels ON videos.channel_id = channels.channel_id
        WHERE videos.like_count = (SELECT MAX(v.like_count) FROM videos v WHERE videos.channel_id = v.channel_id)
        ORDER BY Highest_Likes DESC;""")
        columns = ['Channel Name', 'Video Name', 'Highest Likes']

    elif selection == query_list[6]:
        sql_query = ("""SELECT videos.video_name, videos.like_count AS Likes FROM videos
        ORDER BY videos.like_count DESC;""")
        columns = ['Video Name', 'Likes']

    elif selection == query_list[7]:
        sql_query = ("""SELECT channels.channel_name, channels.channel_views AS Total_Views FROM channels
        ORDER BY channels.channel_views DESC;""")
        columns = ['Channel Name', 'Total Views']

    elif selection == query_list[8]:
        sql_query = ("""SELECT DISTINCT channels.channel_name FROM channels
        JOIN Videos ON Videos.channel_id = channels.channel_id
        WHERE YEAR(Videos.published_date) = 2022;""")
        columns = ['Channel Name']

    elif selection == query_list[9]:
        sql_query = ("""SELECT channels.channel_name, TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(TIME(videos.duration)))), "%H:%i:%s") AS Duration FROM Videos
        JOIN channels ON videos.channel_id = channels.channel_id
        GROUP BY channels.channel_name;""")
        columns = ['Channel Name', 'Duration']

    elif selection == query_list[10]:
        sql_query = ("""SELECT channels.channel_name, videos.video_name, videos.comment_count AS Total_Comments FROM videos
        JOIN channels ON channels.channel_id = videos.channel_id ORDER BY videos.comment_count DESC;""")
        columns = ['Channel Name', 'Video Name', 'Total Comments']

    else:
        columns = []
        st.write("Please select a valid query from the dropdown.")

    if st.button("Run Query"):
        engine = get_sqlalchemy_engine()
        st.subheader("SQL Query:")
        st.code(sql_query, language='sql')
        st.divider()
        if st.session_state["MySQL_URL"].is_connected:
            with st.session_state["MySQL_URL"].connection as connection:
                result = connection.execute(text(sql_query))
                sql_query_output = result.fetchall()

        st.subheader("Results:")
        df = pd.DataFrame(sql_query_output, columns=columns).reset_index(drop=True)
        st.dataframe(df)
