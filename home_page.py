# home_page.py

# this is the default landing page for my application.
# This python code contains a function called home_page() which is called in Utube_website.py

import streamlit as st
import json
import os
import sqlite3
from datetime import datetime
import logging as log
from streamlit_tags import st_tags
import data_con as dt
from utube_DHW_aux_modules import yt, key_hide, sql_db_option, default_localDB_filename

directory_path = r"xtracted_data"

if os.path.exists(directory_path):
    log.info(f"Directory already exists: {directory_path}")
else:
    os.makedirs(directory_path)
    log.info(f"Directory created: {directory_path}")


def save_dict_to_json(channel_data_e, item):
    json_filename = f"{item}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    file_path = os.path.join(directory_path, json_filename)
    with open(file_path, "w") as extractfile:
        json.dump(channel_data_e, extractfile)
        log.info(f"log file was created.")
    return file_path


def upload_data_to_sql(filename):
    st.info(f"SQL upload initiated, DB_type:{st.session_state['DB_type']}")
    status_updates = st.status(f"SQL upload initiated, use_sqlite3:{st.session_state['DB_type']}", expanded=True)
    sql_connector = None
    if st.session_state["DB_type"] == sql_db_option[0]:
        host = st.session_state["config"]['SQL_host']
        port = st.session_state["config"]['SQL_port']
        username = st.session_state["config"]['SQL_user']
        password = st.session_state["config"]['SQL_pswd']
        database_name = st.session_state["config"]['SQL_DB']
        sql_connector = dt.CustomConnector(host, port, username, password, database_name)

        if sql_connector:
            st.info(f"(upload_data_to_sql) SQL upload initiated, DB_type:{st.session_state['DB_type']}")

    elif st.session_state["DB_type"] == sql_db_option[1]:
        try:
            sql_connector = sqlite3.connect(default_localDB_filename)
            log.info("local db connected.")
        except sqlite3.Error as e:
            log.error(e)

    else:
        print("Unknown DB_type.")
        log.error(f"Unknown DB_type. => {st.session_state['DB_type']}")

    st.write("Tube extractors SQL connection initialized")
    sql_connector.create_tables()
    with open(filename, 'r', encoding='cp1252') as file:
        data = json.load(file)
        channel_ = next(iter(data))
        channel_id = data[channel_]['Channel_Id']
        name = data[channel_]['Channel_Name']
        channel_type = data[channel_]['Subscription_Count']
        views = data[channel_]['Channel_Views']
        description = data[channel_]['Channel_Description']
        status = data[channel_]
        print(status.keys())
        sql_connector.upload_channel_data(channel_id, name, channel_type, views, description, status)
        st.write(f"Channel_data({name}) upload_completed.")

        for items in data[channel_]['playlist']:
            playlist_name = items['playlist_title']
            playlist_id = items['playlist_ID']
            sql_connector.upload_playlist_data(playlist_name, playlist_id, channel_id)
            st.write(f"playlist_data({playlist_name}) upload_completed.")

            for video in items['videos']:
                video_key = next(iter(video))
                video_id = video[video_key]['Video_Id']
                video_name = video[video_key]['Video_Name']
                video_description = video[video_key]['Video_Description']
                publish_date = video[video_key]['PublishedAt']
                view_count = video[video_key]['View_Count']
                like_count = video[video_key]['Like_Count']
                dislike_count = video[video_key]['Dislike_Count']
                favourite_count = video[video_key]['Favorite_Count']
                comment_count = video[video_key]['Comment_Count']
                duration = video[video_key]['Duration']
                thumbnail = video[video_key]['Thumbnail']
                caption_status = video[video_key]['Caption_Status']

                try:
                    sql_connector.upload_video_data(video_id, playlist_id, video_name, video_description,
                                                    publish_date, view_count, like_count, dislike_count,
                                                    favourite_count, comment_count, duration, thumbnail, caption_status)
                    st.write(f"Video:{video_name} upload completed.")
                except ValueError as e:
                    print(video_id, playlist_id, video_name, video_description,
                          publish_date, view_count, like_count, dislike_count, favourite_count,
                          comment_count, duration, thumbnail, caption_status)
                    print(e)

                print(video[video_key])

                # Upload comments for the video
                for comment in video[video_key]['Comments']:
                    comment_id = comment['Comment_Id']
                    comment_text = comment['Comment_Text']
                    comment_author = comment['Comment_Author']
                    comment_published_date = comment['Comment_PublishedAt']

                    try:
                        sql_connector.upload_comment_data(comment_id, video_id, comment_text, comment_author,
                                                          comment_published_date)
                        st.write("Comment upload completed. Comment_id:", comment_id)
                    except ValueError as e:
                        print(comment_id, video_id, comment_text, comment_author, comment_published_date)
                        print(e)
    status_updates.update(label="SQL Upload was completed.", state="complete", expanded=False)


def home_page():
    """
    This is the Home page where you enter channel name/ID and get details.
    """

    # Check if the API key is valid
    if st.session_state["API_key_pass"] is None:
        st.info("Just loaded the page, set the API_key in ⚙️ Configuration page.")
        disabled_key = True
    elif st.session_state["API_key_pass"]:
        api_key = key_hide(st.session_state["API_key"])
        st.success(f'✔️ API key is valid. {api_key}')
        disabled_key = False
    elif not st.session_state["API_key_pass"]:
        api_key = key_hide(st.session_state["API_key"])
        st.error(f'❌ API key is invalid. {api_key}')
        disabled_key = True
    else:
        st.error("session state API_key error.")
        disabled_key = True

    st.subheader("Home")

    file_list = []

    with st.form(key="ChannelID_names", clear_on_submit=False):
        keywords = st_tags(
            label="Channel ID/names (max 10):",
            maxtags=10,
            key="keywords",
            value=['guvi', 'UCgLnPO7GYxq47FzF5j3TSlA']
        )
        if st.form_submit_button("proceed"):
            log.info(f"proceed button pressed. {keywords}")
            chid_list = []
            utube_generator = yt.YouTubeDataExtractor(st.session_state["API_key"])

            for item in keywords:
                if not utube_generator.check_input_type(check_text=item):
                    # Convert channel name to channel ID if necessary
                    try:
                        channel_id = utube_generator.get_channel_id(item)
                    except AttributeError as e:
                        log.debug(e)
                        st.error(f"Error converting channel name to ID: {e}")
                        continue
                else:
                    channel_id = item
                chid_list.append(channel_id)

            st.info(chid_list)
            log.info(chid_list)
            file_list = []

            for item in chid_list:
                with st.status(f"Extracting data from channel ID: {item}", expanded=True) as Extraction_status:
                    try:
                        channel_data_e = utube_generator.guvi_format(item)  # channel_data_e is a JSON dict.
                        st.write("Channel data was extracted and stored as Dictionary.")
                        first_key = next(iter(channel_data_e))
                        channel_name_filename = channel_data_e[first_key]["Channel_Name"]
                        filename = save_dict_to_json(channel_data_e, channel_name_filename)
                        st.write("Dictionary was converted to json file.")
                        file_list.append(filename)
                        st.write(f"Data saved to '{filename}'.")
                        Extraction_status.update(label="Extraction completed.", state="complete", expanded=False)
                    except Exception as e:
                        log.error(f"Error extracting data for channel ID {item}: {e}")
                        st.error(f"Error extracting data for channel ID {item}: {e}")
    st.write("Files:", file_list)

    # from here on the columns will take over. we got filelist above.
    # time to upload to SQL with the click of button.
    # also show the json code as raw data within a scrollable container.

    for tie in file_list:
        tie_container = st.container()
        v1, v2 = tie_container.columns(2)
        v1.success(tie)
        try:
            print("Try initiated.")
            with open(tie, "r") as file:
                data = json.load(file)
                v1.json(data, expanded=False)
            print("File read")
            upload_data_to_sql(tie)
            v2.info("Data uploaded to SQL")
            print("Data uploaded to SQL")

        except Exception as e:
            v1.error(f"Error reading or uploading file {tie}: {e}")
            log.error(f"Error reading or uploading file {tie}: {e}")

