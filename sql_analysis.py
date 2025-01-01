# sql_analysis.py
"""
This is for Querying the SQL table and getting the output.
"""

import pandas as pd
import streamlit as st
from code_editor import code_editor
from sqlalchemy import text

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
    '10. Which videos have the highest number of comments, and what are their corresponding channel names?',
    '# Manual Query']

# Button configuration for Execute button.
editor_button_configuration = [
    {
        "name":"Execute",
        "feather":"Play",
        "primary":True,
        "hasText":True,
        "showWithIcon":True,
        "commands":["submit"],
        "style":{"bottom":"0.44rem", "right":"0.4rem"}},
    {
        "name":"Copy",
        "feather":"Copy",
        "hasText":True,
        "alwaysOn":True,
        "commands":["copyAll",
                    ["infoMessage",
                     {
                         "text":"Copied to clipboard!",
                         "timeout":2500,
                         "classToggle":"show"
                     }
                     ]
                    ],
        "style":{
            "top":"-0.25rem",
            "right":"0.4rem"
        }}
]

# Auto complete list for Ace Editor.
Auto_completes = [
    {"caption":"channels", "value":"channels", "meta":"youtube_dh.channels", "name":"Table", "score":400},
    {"caption":"playlists", "value":"playlists", "meta":"youtube_db.playlists", "name":"Table", "score":400},
    {"caption":"comments", "value":"comments", "meta":"youtube_db.comments", "name":"Table", "score":400},
    {"caption":"videos", "value":"videos", "meta":"youtube_db.videos", "name":"Table", "score":400},
    {"caption":"youtube_dh", "value":"youtube_dh", "meta":"youtube_dh", "name":"Database", "score":400},
]


def Selections_work():
    selection = st.selectbox('pick your Question', options=query_list)

    if selection == query_list[0]:
        sql_query = "-- Select the options above or write query here."

    elif selection == query_list[1]:
        sql_query = ("SELECT channels.channel_name, videos.video_name FROM videos \n"
                     "JOIN channels ON channels.channel_id = videos.channel_id\n"
                     "ORDER BY channels.channel_name;")

    elif selection == query_list[2]:
        sql_query = ("SELECT DISTINCT channels.channel_name, COUNT(Videos.video_id) AS Total_Videos FROM channels \n"
                     "JOIN Videos ON channels.channel_id = Videos.channel_id GROUP BY channels.channel_name \n"
                     "ORDER BY Total_Videos DESC;")

    elif selection == query_list[3]:
        sql_query = ("SELECT channels.channel_name, Videos.video_name, Videos.view_count AS Total_Views FROM Videos\n"
                     "JOIN channels ON channels.channel_id = Videos.channel_id\n"
                     "ORDER BY Videos.view_count DESC LIMIT 10;")

    elif selection == query_list[4]:
        sql_query = ("SELECT videos.video_name, videos.comment_count AS Total_Comments FROM videos\n"
                     "ORDER BY videos.comment_count DESC; ")

    elif selection == query_list[5]:
        sql_query = ("""
SELECT channels.channel_name, videos.video_name, videos.like_count AS Highest_Likes FROM videos 
JOIN channels ON videos.channel_id = channels.channel_id
WHERE videos.like_count = (SELECT MAX(v.like_count) FROM videos v WHERE videos.channel_id = v.channel_id)
ORDER BY Highest_Likes DESC;""")

    elif selection == query_list[6]:
        sql_query = ("SELECT videos.video_name, videos.like_count AS Likes FROM videos\n"
                     "ORDER BY videos.like_count DESC;")

    elif selection == query_list[7]:
        sql_query = ("SELECT channels.channel_name, channels.channel_views AS Total_Views FROM channels\n"
                     "ORDER BY channels.channel_views DESC;")

    elif selection == query_list[8]:
        sql_query = ("SELECT DISTINCT channels.channel_name FROM channels\n"
                     "JOIN Videos ON Videos.channel_id = channels.channel_id\n"
                     "WHERE YEAR(Videos.published_date) = 2022;")

    elif selection == query_list[9]:
        sql_query = ("""
SELECT channels.channel_name, TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(TIME(videos.duration)))), "%H:%i:%s") AS Duration 
FROM Videos JOIN channels ON videos.channel_id = channels.channel_id
GROUP BY channels.channel_name;""")

    elif selection == query_list[10]:
        sql_query = ("""
SELECT channels.channel_name, videos.video_name, videos.comment_count AS Total_Comments FROM videos
JOIN channels ON channels.channel_id = videos.channel_id ORDER BY videos.comment_count DESC;""")

    else:
        st.write("Please select a valid query from the dropdown.")
        sql_query = '-- write your own code here.'

    return sql_query


def query_sql():
    selected_query = Selections_work()
    if st.button('pick'):
        st.subheader("SQL Query code Editor: (MySQL)")
        st.write(" write only one query only. I made code to display only on table at a time.")
        # code editor of MySQL
        response_dict = code_editor(selected_query,
                                    lang="sql",
                                    height=[19, 10],
                                    key="sql_editor",
                                    buttons=editor_button_configuration,
                                    shortcuts="vscode",
                                    completions=Auto_completes,
                                    theme="dark",
                                    options={"wrap":True})
        # response output from code_editor
        if len(response_dict['id']) != 0 and (
                response_dict['type'] == "selection" or response_dict['type'] == "submit"):
            selected_query = response_dict['text']
        if selected_query == '':
            print("No Output")
        # print(selected_query)
        if st.session_state["MySQL_URL"].is_connected:
            st.subheader("Results:")
            try:
                df = pd.read_sql_query(text(selected_query), st.session_state["MySQL_URL"].engine)
                if df.empty:
                    st.error("The query executed successfully, but returned no data.")
                    st.empty()
                else:
                    st.dataframe(df)
                    st.toast("Hurray! RETURNED SOME DATA")
            except Exception as e:
                print(f"Error executing query: {e}")

