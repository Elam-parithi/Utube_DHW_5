import streamlit as st


def colour_pick(constructor):
    no_state = "orange"
    valid_state = "lightgreen"
    invalid_state = "red"  # "rgb(253, 109, 109)"
    try:
        colour_status = st.session_state[constructor].is_connected
    except AttributeError:
        return no_state
    if colour_status is True:
        output_colour = valid_state
    elif colour_status is False:
        output_colour = invalid_state
    else:
        output_colour = no_state
    return output_colour


download_button = """
    <style>
        .stDownloadButton {
            font-size: small !important;
            background-color: lightblue !important;
            color: black !important;
            border-radius: 5px !important;
            padding: 8px 12px !important;
            border: 1px solid black !important;
            font-weight: bold !important;
        }
        .stDownloadButton:hover {
            background-color: deepskyblue !important;
        }
    </style>
"""


def statusbar():
    api_color = colour_pick("youTube_API")
    sql_color = colour_pick("MySQL_URL")
    mdb_color = colour_pick("MongoDB_URI")
    repeated = " width: 250px; height: 40px; display: flex; justify-content: center; align-items: center; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-size: 18px; text-align: center;"
    html_code = f"""
        <div id="status-container" style="display: flex; gap: 20px; border:50px; align-items: center; justify-content: center; border-radius: 8px; box-shadow: 0 4px 8px lightblue;
        background-color: rgba(215, 218, 231, 0.918);">
            <div><h3 style="color: black;"> Status: </h3></div> 
            <div style="background-color: {api_color}; {repeated}"><h4>API Key</h4></div>
            <div style="background-color: {sql_color}; {repeated}"><h4>SQL URL</h4></div>
            <div style="background-color: {mdb_color}; {repeated}"><h4>Mongo URI</h4></div>
        </div>
        """
    st.html(html_code)
    return
