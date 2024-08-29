# Your Credentials your responsibility.

import streamlit as st

"""
This code contains default api keys should not be disclosed. protected using secret.
added to .git ignore.

use your YouTube API credentials to use this application. you don't need to enter the credentials directly here. 
But your can add it at the time of execution in UI.
"""

# database_url = 'sqlite:///my_database.db'  # SQLite
# database_url = 'mysql+pymysql://user:password@host/dbname'
# sqlite:///Database_storage/Utube_DHW-5.db
try:
  api_key = st.secrets["api_key"]
  database_uri = st.secrets["database_uri"]
  mongo_uri = st.secrets["mongo_uri"]
except KeyError as e:
  st.write("Key errored")
  st.code(e, launguage=text)
