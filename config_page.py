# config_page.py
"""
page one of the application not default page.
But, API_key verification is done here and SQL configuration done here.
# key="api-key" is not working
"""
import streamlit as st
from data_con import sql_tube, mongo_tube
from config_and_auxiliary import key_hide
import youtube_extractor as yt


def status_banner(value_key, constructor):
    try:
        state_key = st.session_state[constructor].is_connected
        hidden_key = key_hide(st.session_state[value_key], 9)
        if state_key is True:
            st.success(f"{constructor} passed. \n{hidden_key}", icon="✔️")
        elif state_key is False:
            st.error(f"Invalid {constructor} !!! \n{hidden_key}", icon="❌")
        elif state_key is None:
            st.info(f"Just loaded the page configure the {constructor} !!!", icon="⚙️")
    except AttributeError:
        # print('status_banner error')
        pass


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


def status_update():
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


def repeater_entry(paragraphs, value_key, constructor: str):
    # "youTube_API", "MySQL_URL", "MongoDB_URI"
    st.text(paragraphs)
    init_value = ""
    try:
        init_value = st.session_state[value_key]
    except KeyError:
        print("SessionState key error ", value_key)
    entry_val = st.text_input(label=constructor, type="password",
                              value=init_value)
    if st.button("connect", key=f"{constructor}_button"):
        st.session_state[value_key] = entry_val
        with st.spinner(text="Verifying>>>>"):
            if constructor == "youTube_API":
                st.session_state[constructor] = yt.YouTubeDataExtractor(st.session_state[value_key])
            elif constructor == "MySQL_URL":
                st.session_state[constructor] = sql_tube(st.session_state[value_key])
            elif constructor == "MongoDB_URI":
                st.session_state[constructor] = mongo_tube(st.session_state[value_key])
            else:
                raise ValueError("Invalid constructor, only (youTube_API, MySQL_URL, MongoDB_URI)")
    return None


def config_page():
    st.subheader("⚙️ Configuration")

    tab1, tab2, tab3 = st.tabs(['👩🏻‍💻 YouTube API key', '🛢️ SQL URL', '🗃️ MongoDB URI'])
    with tab1:
        paragraphs = """
                You need a Google API key to use this application. Go get yours bellow is just a default key on streamlit secrets. 
                Follow below for more info.      🔗https://developers.google.com/youtube/v3/getting-started
                """
        repeater_entry(paragraphs, value_key="api_key", constructor="youTube_API")
        status_banner(value_key="api_key", constructor="youTube_API")

    with tab2:
        paragraphs = """
        I'm going to request only SQL server URL, because it will select between local and external DB.
        And no need for multiple user input. Be secure, ⚠️Your URL might contain password.
        i.e: for local DB: sqlite:///Database_storage/Utube_DHW-5.db
        for external  SQL: mysql+pymysql://username:password@host:port/dbname
        """
        repeater_entry(paragraphs, value_key='mysql_config', constructor="MySQL_URL")
        status_banner(value_key='mysql_config', constructor="MySQL_URL")

    with tab3:
        paragraphs = """
        Enter MongoDB server details in following format or just copy paste the URI. Be secure, ⚠️Your URI might contain password.
        i.e: mongodb://username:password@host:port/dbname
        """
        repeater_entry(paragraphs, value_key='mongo_config', constructor="MongoDB_URI")
        status_banner(value_key='mongo_config', constructor="MongoDB_URI")
