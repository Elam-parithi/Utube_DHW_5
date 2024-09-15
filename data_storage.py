# data_storage.py
# This is data_storage here we process the data we extracted in home page.
from os import path
import zipfile
from pathlib import Path
import streamlit as st
from data_con import *
from annotated_text import annotated_text
from config_and_auxiliary import custom_annotation

directory = Path(r'./extracted_data')


def zip_files(file_list, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in file_list:
            # Check if the file exists
            if os.path.exists(file):
                # Add file to the zip
                zipf.write(file, os.path.basename(file))
            else:
                print(f"File {file} does not exist")


def create_download_buttons(filepaths):
    for file_name in filepaths:
        filepath = directory / f"{file_name}.json"
        filename = path.basename(filepath)
        with open(filepath, "rb") as file:
            file_data = file.read()
        st.download_button(
            label=f"{file_name}",
            data=file_data,
            file_name=filename,
            mime="application/octet-stream")


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
    st.header("Storage processing:")
    # default attribute, change to none
    st.divider()
    with st.container():
        file_columns, storage_columns = st.columns(2)
        with file_columns:
            json_files = []
            for file_name in os.listdir(r'./extracted_data'):
                if file_name.endswith(".json"):
                    json_files.append(os.path.splitext(file_name)[0])
            st.session_state.Selected_files = st.multiselect("Extracted filenames:",
                                                             options=json_files, default=None,
                                                             help="select only the required one",
                                                             placeholder="Choose an option")

        with storage_columns:
            storage_option = ['SQL', 'MongoDB']
            st.subheader("select Storage option:")
            storage_sql = st.checkbox(storage_option[0], True, disabled=True)
            checkbox_state = False
            m1, m2 = st.columns([3, 7])
            try:
                checkbox_state = st.session_state.MongoDB_URI.is_connected
            except AttributeError:
                with m2:
                    annotated_text(("MongoDB URI is not Connected.", "", "pink"))
            with m1:
                storage_mon = st.checkbox(storage_option[1], False, disabled=not checkbox_state,
                                          label_visibility='visible')

    st.divider()
    create_download_buttons(st.session_state.Selected_files)
    custom_annotation(st.session_state.Selected_files)
    if st.button("Upload selected"):
        if storage_sql:
            for file_name in st.session_state.Selected_files:
                filename = path.basename(file_name)
                st.session_state.MySQL_URL.json_2_sql(filename, file_name)
            st.write("storage_sql")
        if storage_mon:
            st.write("storage_mon")
