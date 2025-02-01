# home_page.py

# this is the default landing page for my application.
# This python code contains a function called home_page()
# which is called in extractor_app.py

import time, os
import streamlit as st
from streamlit_tags import st_tags
from googleapiclient.errors import HttpError
from httplib2 import ServerNotFoundError
import youtube_extractor as yt
from config_and_auxiliary import basic_settings, d_channel, custom_annotation
from youtube_extractor import save_dict_to_json


@st.dialog("Youtube API Quota Exceeded.", width="large")
def quota_popup():
    dialog_text = """
    Your YouTube API quota has been exceeded. Please check your quota usage and try again later. OR use Another key.
    For more info.</p> <a href="https://console.developers.google.com/">Google Developers Console</a>
    """
    st.write(dialog_text)
    text_input = st.text_input("Enter another API if available.")
    c1, c2, c3 = st.columns(3)
    with c3:
        if st.button("Submit"):
            st.session_state.api_key = text_input
            st.rerun()
    with c1:
        if st.button("exit"):
            st.rerun()


def home_page():
    """
    This is the Home page where you enter channel name/ID and get details.
    """
    st.subheader("🏠 Home")
    st.write("❗ select channels that are small. If you select bigger channels they take more time to "
             "extract, upload to MySQL and Sentiment Analysis.")
    with st.form(key="ChannelID_names", clear_on_submit=False):
        keywords = st_tags(
            label="Youtube channel ID/names (max 10):",
            maxtags=basic_settings['MAX_CHANNELS'],
            key="keywords",
            value=d_channel
        )
        if st.form_submit_button("Proceed"):
            print("Proceeding")
            chid_list = []
            utube_generator = yt.YouTubeDataExtractor(st.session_state["api_key"])

            for item in keywords:
                if not utube_generator.check_input_type(check_text=item):
                    # Convert channel name to channel ID if necessary
                    try:
                        channel_id = utube_generator.get_channel_id(item)
                    except AttributeError as e:
                        quota_popup()
                        # st.error(f"Error converting channel name to ID: {e}")
                        continue
                    except HttpError as e:
                        error_content = e.content.decode("utf-8")
                        if "quotaExceeded" in error_content:
                            print("Quota exceeded: You cannot make more requests at this time.")
                            quota_popup()
                            continue
                else:
                    channel_id = item
                chid_list.append(channel_id)

            st.write('All channel ID: ')
            if len(chid_list) == 0:
                pass
            else:
                custom_annotation(chid_list)
            file_list = []

            import time

            for item in chid_list:
                start_time = time.time()  # Start the timer
                with st.status(f"Extracting data from channel ID: {item}", expanded=True) as extraction_status:
                    try:
                        # Perform the data extraction
                        channel_data_e = utube_generator.guvi_format(item)  # stocks_data is a JSON dict.
                        st.write("Channel data was extracted and stored as Dictionary.")

                        # Save the data to a JSON file
                        first_key = next(iter(channel_data_e))
                        channel_name_filename = channel_data_e[first_key]["Channel_Name"]
                        filename = save_dict_to_json(channel_data_e, channel_name_filename)
                        st.write("Dictionary was converted to JSON file.")
                        file_list.append(filename)
                        st.write(f"Data saved to '{filename}'.")
                        # Calculate elapsed time
                        elapsed_time = time.time() - start_time
                        minutes = int(elapsed_time // 60)
                        seconds = elapsed_time % 60
                        filename = os.path.basename(filename)
                        extraction_status.update(
                            label=f"{filename} extraction completed => Time taken {minutes}:{seconds:.2f} seconds.",
                            state="complete",
                            expanded=False
                        )
                    except ValueError as e:
                        print(f"ValueError as {e}")
                    except Exception as e:
                        extraction_status.update(label=f"Error occurred: {str(e)}", state="error", expanded=True)
                    except ServerNotFoundError:
                        quota_popup()
                    except HttpError as e:
                        if e.resp.status == 403:
                            quota_popup()
                        else:
                            st.error(f"An error occurred: e.resp.status==>>{e.resp.status}")
                            st.error(f"Error extracting data for channel ID {item}: {e}")

            st.session_state.file_lists = file_list
            st.write("Files:")
            annotation_list = []
            for item in file_list:
                annotation_list.append(os.path.basename(item))
            custom_annotation(annotation_list)
