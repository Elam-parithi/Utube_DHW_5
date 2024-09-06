# home_page.py

# this is the default landing page for my application.
# This python code contains a function called home_page()
# which is called in extractor_app.py


import os
import json
import streamlit as st
from datetime import datetime
from streamlit_tags import st_tags
from config_and_auxiliary import yt, key_hide

directory_path = r"extracted_data"


def save_dict_to_json(channel_data_e, item):
    json_filename = f"{item}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    file_path = os.path.join(directory_path, json_filename)
    with open(file_path, "w") as extractfile:
        json.dump(channel_data_e, extractfile, indent=4)
    return file_path


def home_page():
    """
    This is the Home page where you enter channel name/ID and get details.
    """
    # Check if the API key is valid
    if st.session_state.get("API_key_pass") is None:
        st.info("Just loaded the page, set the API key in ⚙️ Configuration page.")
    elif st.session_state.get("API_key_pass"):
        api_key = key_hide(st.session_state["api_key"])
        st.success(f'✔️ API key is valid. {api_key}')
    elif not st.session_state.get("API_key_pass"):
        api_key = key_hide(st.session_state["api_key"])
        st.error(f'❌ API key is invalid. {api_key}')
    else:
        st.error("Session state API key error.")

    st.subheader("Home")
    file_list = []
    with st.form(key="ChannelID_names", clear_on_submit=False):
        keywords = st_tags(
            label="Channel ID/names (programmed-limit 10):",
            maxtags=10,
            key="keywords",
            value=st.secrets.settings.defalt_channel
        )
        if st.form_submit_button("Proceed"):
            chid_list = []
            utube_generator = yt.YouTubeDataExtractor(st.session_state["api_key"])

            for item in keywords:
                if not utube_generator.check_input_type(check_text=item):
                    # Convert channel name to channel ID if necessary
                    try:
                        channel_id = utube_generator.get_channel_id(item)
                    except AttributeError as e:
                        st.error(f"Error converting channel name to ID: {e}")
                        continue
                else:
                    channel_id = item
                chid_list.append(channel_id)

            st.write('All channel ID: ', chid_list)
            file_list = []

            for item in chid_list:
                with st.status(f"Extracting data from channel ID: {item}", expanded=True) as extraction_status:
                    try:
                        channel_data_e = utube_generator.guvi_format(item)  # channel_data_e is a JSON dict.
                        st.write("Channel data was extracted and stored as Dictionary.")
                        first_key = next(iter(channel_data_e))
                        channel_name_filename = channel_data_e[first_key]["Channel_Name"]
                        filename = save_dict_to_json(channel_data_e, channel_name_filename)
                        st.write("Dictionary was converted to JSON file.")
                        file_list.append(filename)
                        st.write(f"Data saved to '{filename}'.")
                        extraction_status.update(label="Extraction completed.", state="complete", expanded=False)
                    except Exception as e:
                        st.error(f"Error extracting data for channel ID {item}: {e}")

    # st.session_state.file_lists = file_list
    st.write("Files:", file_list)
