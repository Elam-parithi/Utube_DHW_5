import json
from datetime import datetime
import streamlit as st
import temp_credentials
import youtube_extractor as yt

# Get the current date for file naming
current_date = datetime.now().strftime("%Y-%m-%d")


def save_dict_to_json(data):
    # Extract the channel name as the first key from the dictionary
    channel_name = next(iter(data))
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # Filename in the format "extracted_data/ChannelName-DateTime.json"
    filename = f"extracted_data/{channel_name}-{current_datetime}.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data successfully saved to {filename}")
    return filename


def key_hide(api_key, visible_chr=5):
    hidden_key = '*' * (len(api_key) - visible_chr) + api_key[-visible_chr:]
    return hidden_key


API_key = temp_credentials.api_key
database_URI = temp_credentials.database_uri
MongoDB_URI = temp_credentials.mongo_uri

# Streamlit session state initialization
if "api_key" not in st.session_state:
    st.session_state["api_key"] = API_key
if "API_key_pass" not in st.session_state:
    st.session_state["API_key_pass"] = None
if "mysql_config" not in st.session_state:
    st.session_state["mysql_config"] = database_URI
if "mongo_config" not in st.session_state:
    st.session_state['mongo_config'] = MongoDB_URI


# Instantiate YouTubeDataExtractor if API key is available
if st.session_state["API_key_pass"]:
    tube = yt.YouTubeDataExtractor(API_key)

