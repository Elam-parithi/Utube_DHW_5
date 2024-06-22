
# SQL_Analysis.py
# for querying and answering preconfigured results.

import streamlit as st
import pandas as pd
from utube_DHW_aux_modules import page_sql_status


def query_sql():
    query_list = ['Select your Question',
                  '1. What are the names of all the videos and their corresponding channels?',
                  '2. Which channels have the most number of videos, and how many videos do they have?',
                  '3. What are the top 10 most viewed videos and their respective channels?',
                  '4. How many comments were made on each video, and what are their corresponding video names?',
                  '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                  '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                  '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                  '8. What are the names of all the channels that have published videos in the year 2022?',
                  '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                  '10. Which videos have the highest number of comments, and what are their corresponding channel names?']
    query_cursor = page_sql_status()
    selection = st.selectbox('Select your Question', options=query_list)
    sql_query = None
    if selection == query_list[1]:
        sql_query = ("""SELECT Channel.channel_name, Video.video_name FROM Video;
                        JOIN Channel ON Channel.channel_id = Video.channel_id;
                        ORDER BY Channel.channel_name;""")
        columns = ['Channel Name', 'Video Name']

    elif selection == query_list[2]:
        sql_query = ("""SELECT DISTINCT Channel.channel_name, COUNT(Video.video_id) AS Total_Videos 
                        FROM Channel 
                        JOIN Video ON Channel.channel_id = Video.channel_id
                        GROUP BY Channel.channel_name 
                        ORDER BY Total_Videos DESC""")
        columns = ['Channel Name', 'Total Videos']

    elif selection == query_list[3]:
        sql_query = ("""SELECT Channel.channel_name, Video.video_name, Video.view_count AS Total_Views
                        FROM Video
                        JOIN Channel ON Channel.channel_id = Video.channel_id
                        ORDER BY Video.view_count DESC
                        LIMIT 10""")
        columns = ['Channel Name', 'Video Name', 'Total Views']

    elif selection == query_list[4]:
        sql_query = ("""SELECT Video.video_name, Video.comment_count AS Total_Comments
                        FROM Video
                        ORDER BY Video.comment_count DESC""")
        columns = ['Video Name', 'Total Comments']

    elif selection == query_list[5]:
        sql_query = ("""SELECT Channel.channel_name, Video.video_name, Video.like_count AS Highest_Likes FROM Video 
                        JOIN Channel ON Video.channel_id = Channel.channel_id
                        WHERE Video.like_count = (SELECT MAX(v.like_count) FROM Video v WHERE Video.channel_id = v.channel_id)
                        ORDER BY Highest_Likes DESC""")
        columns = ['Channel Name', 'Video Name', 'Highest Likes']

    elif selection == query_list[6]:
        sql_query = ("""SELECT Video.video_name, Video.like_count AS Likes
                        FROM Video
                        ORDER BY Video.like_count DESC""")
        columns = ['Video Name', 'Likes']

    elif selection == query_list[7]:
        sql_query = ("""SELECT Channel.channel_name, Channel.channel_views AS Total_Views
                        FROM Channel
                        ORDER BY Channel.channel_views DESC""")
        columns = ['Channel Name', 'Total Views']

    elif selection == query_list[8]:
        sql_query = ("""SELECT DISTINCT Channel.channel_name
                        FROM Channel
                        JOIN Video ON Video.channel_id = Channel.channel_id
                        WHERE YEAR(Video.publish_date) = 2022""")
        columns = ['Channel Name']

    elif selection == query_list[9]:
        sql_query = ("""SELECT Channel.channel_name,
                        TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(TIME(Video.duration)))), "%H:%i:%s") AS Duration
                        FROM Video
                        JOIN Channel ON Video.channel_id = Channel.channel_id
                        GROUP BY Channel.channel_name""")
        columns = ['Channel Name', 'Duration']

    elif selection == query_list[10]:
        sql_query = ("""SELECT Channel.channel_name, Video.video_name, Video.comment_count AS Total_Comments
                        FROM Video
                        JOIN Channel ON Channel.channel_id = Video.channel_id
                        ORDER BY Video.comment_count DESC""")
        columns = ['Channel Name', 'Video Name', 'Total Comments']

    else:
        columns = []
        st.write("Please select a valid query from the dropdown.")

    if st.button("proceed"):
        st.subheader("MySQL Code :")
        st.code(sql_query, language='sql')
        st.divider()
        query_cursor.execute(sql_query)
        sql_query_output = query_cursor.fetchall()
        st.subheader("Results :")
        df = pd.DataFrame(sql_query_output, columns=columns).reset_index(drop=True)
        st.dataframe(df)

