# data_storage.py

# This is data_storage here we process the data we extracted in home page.

from os import path
import streamlit as st
from data_con import *
import streamlit_tags


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


def Data_storage_tab():
    # Data_storage_processing. processing the data in streamlit.
    st.subheader("Non-Volatile Data Storage processing.")
    # default attribute, change to none
    st.session_state["file_lists"] = ["extracted_data/Madras foodie-20240821-181855.json", "extracted_data/Madras foodie-20240821-190137.json"]
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
        storage_selection = st.selectbox('select Storage option', storage_option)
        # check this option is ready or not
        st.write("uploading:", *[path.basename(file_name)+',   ' for file_name in selected_files])
        st.success(storage_selection)
        procced_storage = st.button(f"{storage_selection} upload")
        # button to procced with option.
        if procced_storage:
            if storage_selection == storage_option[0]:
                sql_store_con = sql_tube(st.session_state["mysql_config"])
                for json_filepath in selected_files:
                    sql_store_con.json_2_sql(str(path.basename(json_filepath)), json_filepath)
            elif storage_selection == storage_option[1]:
                mongo_tube(st.session_state["mongo_config"])
            else:
                raise KeyError

