# data_storage.py
# This is data_storage here we process the data we extracted in home page.
from os import path
import zipfile
from data_con import *
import streamlit as st
from annotated_text import annotated_text
from html_addon import download_button
from config_and_auxiliary import directory_settings

directory = Path(directory_settings['extracted json folder'])
mongodb_name = 'YouTube_DHW'
mongo_collection = "extration_upload"


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
    cols_per_row = 3  # Number of columns per row
    rows = [filepaths[i:i + cols_per_row] for i in range(0, len(filepaths), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for i, file_name in enumerate(row):
            filepath = Path(directory) / f"{file_name}.json"
            filename = path.basename(filepath)

            with open(filepath, "rb") as file:
                file_data = file.read()

            with cols[i]:  # Place button in the respective column
                st.html(download_button)
                st.download_button(
                    label=f"{file_name}.json",
                    data=file_data,
                    file_name=filename,
                    mime="application/octet-stream"
                )


def Data_storage_tab():
    # Data_storage_processing. processing the data in streamlit.
    st.header("🛢 Storage processing:")
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

    if len(st.session_state.Selected_files) != 0:
        st.divider()
        st.subheader("Download extracted data:")
        st.write("for keeping files on json format. use download buttons below.")
        create_download_buttons(st.session_state.Selected_files)
        st.divider()
        st.write("upload selected files to SQL ?")
        if st.button("yes, Upload"):
            with st.status(f"Uploading Data", expanded=True) as upload_status:
                if storage_sql:
                    us_sql = time.time()
                    st.session_state["MySQL_URL"].json_2_sql(st.session_state.Selected_files)
                    ue_sql = time.time()
                    elapsed_time = us_sql - ue_sql
                    minutes = int(elapsed_time // 60)
                    seconds = elapsed_time % 60
                    st.write(f"Time Taken (MySQL DB): {minutes} min {seconds:.2f} sec")

                if storage_mon:
                    us_mon = time.time()
                    if st.session_state["MongoDB_URI"].is_connected:
                        for json_filed in st.session_state.Selected_files:
                            st.session_state["MongoDB_URI"].JSON_2_mongo(JSON_filename=Path(f"{directory}/{json_filed}.json"),
                                                                         DataBase_name=mongodb_name,
                                                                         collection=mongo_collection)
                        st.session_state["MongoDB_URI"].close_mongo()
                        ue_mon = time.time()
                        elapsed_time = us_mon - ue_mon
                        minutes = int(elapsed_time // 60)
                        seconds = elapsed_time % 60
                        st.write(f"Time Taken (Mongo DB): {minutes} min {seconds:.2f} sec")

                upload_status.update(
                    label=f"Upload completed.",
                    state="complete",
                    expanded=False
                )
    else:
        pass
