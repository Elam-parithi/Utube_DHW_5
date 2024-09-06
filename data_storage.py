# data_storage.py
import random
# This is data_storage here we process the data we extracted in home page.

from os import path
import streamlit as st
from data_con import *
import streamlit_tags
from config_and_auxiliary import light_colors
from annotated_text import annotated_text


def unique_picker():
    items = light_colors.copy()
    seen = []
    for item in items:
        if item not in seen:  # Check if the item is unique
            seen.append(item)    # Add the item to the seen set
            yield item        # Yield the unique item


def create_download_buttons(filepaths):
    for filepath in filepaths:
        filename = path.basename(filepath)
        with open(filepath, "rb") as file:
            file_data = file.read()
        st.download_button(
            label=f"Download {filename}",
            data=file_data,
            file_name=filename,
            mime="application/octet-stream"
        )


def visible_check(status_key):
    match_case = st.session_state[status_key]
    if match_case:
        op = "visible"
    elif match_case is None:
        op = "hidden"
    else:
        op = "hidden"
    return op


def Data_storage_tab():
    # Data_storage_processing. processing the data in streamlit.
    st.subheader("Non-Volatile Data Storage processing.")
    # default attribute, change to none
    st.session_state["file_lists"] = ["extracted_data/Madras foodie-20240821-181855.json",
                                      "extracted_data/Madras foodie-20240821-190137.json"]
    file_columns, storage_columns = st.columns(2)
    with file_columns:
        selected_files = streamlit_tags.st_tags(
            label="Extracted filenames:",
            maxtags=10,
            key="keywords",
            value=st.session_state.get("file_lists")
        )
        create_download_buttons(selected_files)

    with storage_columns:
        storage_option = ['SQL', 'MongoDB']
        st.header("select Storage option")
        storage_sql = st.checkbox(storage_option[0], True, label_visibility=visible_check("sql_state"))
        storage_mon = st.checkbox(storage_option[1], False, label_visibility=visible_check("mongo_state"))
        # check this option is ready or not
        st.write("uploading:")
        if st.button("pick"):
            st.write(unique_picker())
        annotated_text('by ', ('texting', 'writing', "#8ef"))
        for file_name in selected_files:
            annotated_text(((path.basename(file_name),"",unique_picker())))
        procced_storage = st.button(f"upload")
        # Custom CSS for styling the button
        button_style = """
            <style>
            .custom-button {
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
                outline: none;
                color: #fff;
                background-color: lightgreen;
                border: none;
                border-radius: 15px;
                box-shadow: 0 9px #999;
            }

            .custom-button:hover {background-color: lightyellow}

            .custom-button:active {
                background-color: #3e8e41;
                box-shadow: 0 5px #666;
                transform: translateY(4px);
            }
            </style>
        """

        # Display the button using HTML
        clicked = st.html(f"""{button_style}<a href="#" class="custom-button">Click Me</a>""")

        # Detecting click (using a workaround)
        if st.session_state.get('button_clicked') == 'clicked':
            st.write("Button clicked!")

        # Workaround for button click (using a hidden Streamlit button)
        if st.button('Hidden button', key='button_click_trigger'):
            st.session_state['button_clicked'] = 'clicked'

        # button to procced with option.
        if procced_storage:
            if storage_sql:
                sql_store_con = sql_tube(st.session_state["mysql_config"])
                for json_filepath in selected_files:
                    sql_store_con.json_2_sql(str(path.basename(json_filepath)), json_filepath)
            elif storage_mon:
                mongo_tube(st.session_state["mongo_config"])
            else:
                raise KeyError
