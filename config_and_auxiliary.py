# Your Credentials your responsibility.
import json
import random
import string
import streamlit as st
from pathlib import Path
import youtube_extractor as yt
from annotated_text import annotated_text

"""
This code contains default URL, URI keys should not be disclosed. 
protected using secrets.toml file to keep secrets locally.
for API it will generate random 24char API key, sql database default to SQLite3.
Mongo will be set none.

use your YouTube API credentials to use this application. 
you don't need to enter the credentials directly here. unless using permanently.
But your can add it at the time of execution in UI.
"""

MAX_CHANNELS = 10
directory_settings = {
    'extracted json folder' : r'./extracted_data',
    'SQLite3 database storge folder' : r'./Database_storage',
    'Debug logs folder' : r'./logs',
}

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


def pick_random_color(unused_colors):
    if len(unused_colors) == 0:
        unused_colors = light_colors.copy()
    random_number = random.randrange(0, len(unused_colors))
    remaining = unused_colors.pop(random_number)
    return remaining


def custom_annotation(t_list):
    my_list = []
    colors = []
    for count, item in enumerate(t_list):
        if count != (len(t_list)-1):
            e_str = " , "
        else:
            e_str = " "
        f_str = list(("  ", (item, '', pick_random_color(colors)), e_str)) # str(count+1)
        my_list.append(f_str)
    annotated_text(my_list)


def generate_api_key(length=24):
    """
    Generate a YouTube-like API key.

    Args:
        length (int): The length of the key, default is 24.

    Returns:
        str: A randomly generated API key.
    """
    characters = string.ascii_letters + string.digits
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


def get_secret(Key_name):
    secret_val = None
    try:
        secret_val = st.secrets[Key_name]
    except KeyError:
        st.info(f".streamlit/secrets.toml is missing {Key_name}")
    finally:
        return secret_val


try:
    d_channel = st.secrets["default_settings"]["default_channel"]
except KeyError:
    st.info(f".streamlit/secrets.toml is missing default channel list")
    d_channel = ['UCY0zAYs-eOP7rguMWkJ6L-g', 'guvi']  # Madras foodie channel id and GUVI channel name.

API_key = get_secret("api_key")
database_URI = get_secret("database_uri")
MongoDB_URI = get_secret("mongo_uri")

if not API_key:
    API_key = generate_api_key()
if not database_URI:
    database_URI = "sqlite:///Database_storage/Utube_DHW-5.db"

# Streamlit session state initialization
configurations = {
    "first_run": True,
    "api_key":API_key,
    "mysql_config":database_URI,
    "mongo_config":MongoDB_URI,

    "youTube_API":None,
    "MySQL_URL":None,
    "MongoDB_URI":None,

    "file_lists":None,
    "json_result":None,
    "Selected_files": None,
}

for key, value in configurations.items():
    if key not in st.session_state:
        st.session_state[key] = value


folder_path =[ r'./extracted_data',
               r'./logs',
               r'./Database_storage' ]

for folder_name_str in folder_path:
    folder_name=Path(folder_name_str)
    if not folder_name.exists():
        folder_name.mkdir(parents=True, exist_ok=True)
        print(f"Folder '{folder_name}' created successfully.")
    else:
        # print(f"Folder '{folder_name}' already exists.")
        pass

