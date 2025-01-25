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
    """
    A function to control html status banner using streamlit.session_state
    @param value_key: value state
    @param constructor: constructor state
    """
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
        pass


def repeater_entry(paragraphs: str, value_key, constructor: str):
    # "youTube_API", "MySQL_URL", "MongoDB_URI"
    """
    Function for managing tabs in config page.
    Also, The initiation for API, SQL, Mongo are done here with session state.
    @param paragraphs: string
    @param value_key: value state
    @param constructor: constructor state
    """
    st.text(paragraphs)
    init_value = ""
    try:
        init_value = st.session_state[value_key]
    except KeyError:
        print("SessionState key error ", value_key)
    entry_val = st.text_input(label=constructor, type="password", value=init_value)
    if st.button("connect", key=f"{constructor}_button"):
        st.session_state[value_key] = entry_val
        # stores the entry key like api,sql url, mongo connection_string on session
        # constructor is for  initiating class for the whole program.
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


paragraph_1 = """
You need a Google API key to use this application. Go get yours bellow is just a default key on streamlit secrets. 
Follow below for more info. 🔗https://developers.google.com/youtube/v3/getting-started
"""
paragraph_2 = """
I'm going to request only SQL server URL, Because it provides convince of writing all the config into one. 
Be secure, ⚠️Your URL might contain password. for external  SQL: mysql+pymysql://username:password@host:port/dbname.
For note: my previous configuration of using SQLite string was removed. because BigInteger is required for 
saving channel views, likes and more. so. I'm sticking with MySQL only. 
"""
paragraph_3 = """
Enter MongoDB details in following format or just copy paste the URI. Be secure,⚠️Your URI might contain password.
i.e: mongodb://username:password@host:port/dbname
"""


def config_page():
    st.subheader("⚙️ Configuration")

    tab1, tab2, tab3 = st.tabs(['👩🏻‍💻 YouTube API key', '🛢️ SQL URL', '🗃️ MongoDB URI'])
    with tab1:
        # TODO: issue with youtube API, passed without internet connections.
        repeater_entry(paragraph_1, value_key="api_key", constructor="youTube_API")
        status_banner(value_key="api_key", constructor="youTube_API")

    with tab2:
        repeater_entry(paragraph_2, value_key='mysql_config', constructor="MySQL_URL")
        status_banner(value_key='mysql_config', constructor="MySQL_URL")

    with tab3:
        repeater_entry(paragraph_3, value_key='mongo_config', constructor="MongoDB_URI")
        status_banner(value_key='mongo_config', constructor="MongoDB_URI")
