# Your Credentials your responsibility.

import json
import random
import string
import streamlit as st
import youtube_extractor as yt

"""
This code contains default api keys should not be disclosed. protected using secret.
added to .git ignore file. I'm using Secrets.toml file to keep secrets locally.
for API it will generate random 24char API key, sql database default to sqlite.
Mongo will be set none.

use your YouTube API credentials to use this application. 
you don't need to enter the credentials directly here. unless using permanently.
But your can add it at the time of execution in UI.
"""

MAX_CHANNELS = 10
light_colors = [
    "#cfc",  # Light Green
    "#ffb",  # Light Yellow
    "#ccf",  # Light Lavender
    "#fcf",  # Light Pink
    "#cff",  # Light Cyan
    "#ffc",  # Light Peach
    "#eef",  # Light Blue-Grey
    "#fdd",  # Light Rose
    "#efe",  # Light Mint
    "#eec",  # Light Lemon
    "#cfe",  # Light Teal
    "#fce",  # Light Coral
    "#cfd",  # Light Aqua
    "#fef",  # Light Magenta
    "#dff",  # Light Ice Blue
    "#fdc",  # Light Apricot
    "#eff",  # Light Sky Blue
    "#dfe",  # Light Seafoam
    "#ecf",  # Light Lilac
    "#fdb"  # Light Salmon
]


# database_url = 'mysql+pymysql://user:password@host/dbname'
# sqlite:///Database_storage/Utube_DHW-5.db  # SQLite


def generate_api_key(length=24):
    """
    Generate a YouTube-like API key.

    Args:
        length (int): The length of the key, default is 24.

    Returns:
        str: A randomly generated API key.
    """
    characters = string.ascii_letters + string.digits + '-_'  # Alphanumeric + dash and underscore
    api_key = ''.join(random.choices(characters, k=length))
    return api_key


def save_dict_to_json(data):
    """
    Function to save the dict to json file in extracted_data folder as *.json
    Args:
        data (dict): json format dictionary
    Returns:
        str: name of the file
    """
    channel_name = next(iter(data))
    filename = f"extracted_data/{channel_name}.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data successfully saved to {filename}")
    return filename


def key_hide(secret_text, visible_chr=5):
    """
    Function to hide sensitive secret text,
    It will show * instead of chars only last mentioned
    chars will be shown for identification.
    Args:
        secret_text (str): required text here, no default.
        visible_chr (int): chars to show at last of *
    Returns:
        str: name of the file
    """
    hidden_key = '*' * (len(secret_text) - visible_chr) + secret_text[-visible_chr:]
    return hidden_key


API_key = st.secrets["api_key"]
database_URI = st.secrets["database_uri"]
MongoDB_URI = st.secrets["mongo_uri"]

if not API_key:
    API_key = generate_api_key()
if not database_URI:
    database_URI = "sqlite:///Database_storage/Utube_DHW-5.db"

# Streamlit session state initialization
configurations = {
    "api_key":API_key,
    "mysql_config":database_URI,
    "mongo_config":MongoDB_URI,
    "API_key_pass":None,
    "sql_state":None,
    "mongo_state":None,
    "file_lists":None
}

for key, value in configurations.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Instantiate YouTubeDataExtractor if API key is available
if st.session_state["API_key_pass"]:
    tube = yt.YouTubeDataExtractor(API_key)
