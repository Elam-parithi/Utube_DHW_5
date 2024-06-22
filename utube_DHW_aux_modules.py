
# utube_DHW_aux_modules.py
# This module contains all the variables, functions and declaration commonly used across modules.

import json
import sqlite3
import logging
from datetime import datetime
import streamlit as st
import temp_credentials
import youtube_extractor as yt
import mysql.connector as mysql
from annotated_text import annotated_text

current_date = datetime.now().strftime("%Y-%m-%d")
log_filepath = f"./logs/Utube_website-{current_date}.log"
logging.basicConfig(filename=log_filepath, format='%(asctime)s %(message)s', filemode='w')
log = logging.getLogger('Utube_extractor')
log.setLevel(logging.DEBUG)


def save_dict_to_json(data):
    # first key from the dictionary is the channel name
    channel_name = next(iter(data))
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # xtracted_data/Sahi Siva-2024-06-02-14-54-06.json
    filename = f"xtracted_data/{channel_name}-{current_datetime}.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data successfully saved to {filename}")
    return filename


def key_hide(api_key, visible_chr=5):
    hidden_key = '*' * (len(api_key) - visible_chr) + api_key[-visible_chr:]
    return hidden_key


sql_db_option = ['External SQL DB', 'Internal SQLite3 DB']
default_localDB_filename = "Utube_DHW-4"

API_key = temp_credentials.api_key
SQL_host = temp_credentials.SQL_host
SQL_port = temp_credentials.SQL_port
SQL_user = temp_credentials.SQL_user
SQL_pswd = temp_credentials.SQL_pswd
SQL_DB = temp_credentials.SQL_DB
sql_status_check = None

if "API_key" not in st.session_state:
    st.session_state["API_key"] = API_key
if "API_key_pass" not in st.session_state:
    st.session_state["API_key_pass"] = None

if "DB_type" not in st.session_state:
    st.session_state["DB_type"] = None

if "Active_SQL_connection" not in st.session_state:
    st.session_state["Active_SQL_connection"] = None
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []
if "config" not in st.session_state:
    st.session_state["config"] = config = {
        'SQL_host': SQL_host,
        'SQL_port': SQL_port,
        'SQL_user': SQL_user,
        'SQL_pswd': SQL_pswd,
        'SQL_DB': SQL_DB
    }

st.set_page_config(
    page_title="Utube DHW 4",
    page_icon=r"Icons/Calendula.ico",
    layout='wide',
)

if st.session_state["API_key_pass"]:
    tube = yt.YouTubeDataExtractor(API_key)


def page_sql_status():
    sql_cursor = None
    if st.session_state["DB_type"] == sql_db_option[0]:
        st.success("Active SQL connection!!!")
        sql_con_status = "✔️"
        qa = mysql.connect(
            host=st.session_state['config']['SQL_host'],
            user=st.session_state['config']['SQL_user'],
            password=st.session_state['config']['SQL_pswd'],
            database=st.session_state['config']['SQL_DB'],
            port=st.session_state['config']['SQL_port']
        )
        sql_cursor = qa.cursor()
    elif st.session_state["DB_type"] == sql_db_option[1]:
        sql_con_status = "✔️"
        try:
            conn = sqlite3.connect(default_localDB_filename)
            st.success(f"Connected to SQLite database: {default_localDB_filename}")
            sql_cursor = conn.cursor()
        except sqlite3.Error as e:
            st.error(e)
    else:
        sql_con_status = "❌"
        pass
    st.write(f"Connection status: {sql_con_status}")
    st.divider()
    return sql_cursor


st.title("YouTube Data Harvesting and Warehousing using SQL and Streamlit")
annotated_text('by ', ('[Elamparithi T](https://www.linkedin.com/in/elamparithi-t/)', 'Data Scientist', "#8ef"))
