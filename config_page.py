# config_page.py
# page one of the application not default page. but API_key verification is done here and SQL configuration done here.

import streamlit as st
from data_con import sql_tube, mongo_tube
from config_and_auxiliary import key_hide
from youtube_extractor import check_api_key


def status_banner(session_key, session_state_key, op_string: str):
    with st.empty():
        state_key = st.session_state[session_state_key]
        hidden_key = key_hide(st.session_state[session_key])
        if state_key == True:
            st.success(f"{op_string} passed. \n{hidden_key}", icon="✔️")
        elif state_key == False:
            st.error(f"Invalid {op_string} !!! \n{hidden_key}", icon="❌")
        elif state_key == None:
            st.info(f"Just loaded the page configure the {op_string} !!!", icon="⚙️")
        else:
            raise AttributeError("value should be bool or none")


def colour_pick(session_status_key):
    colour_status = st.session_state[session_status_key]
    no_state = "orange"
    valid_state = "lightgreen"
    invalid_state = "rgb(253, 109, 109)"
    if colour_status is True:
        output_colour = valid_state
    elif colour_status is False:
        output_colour = invalid_state
    else:
        output_colour = no_state
    return output_colour


def config_page():
    st.subheader("⚙️ Configuration")

    tab1, tab2, tab3 = st.tabs(['👩🏻‍💻 YouTube API key', '🛢️ SQL URL', '🗃️ MongoDB URI'])
    with tab1:
        st.write("**YouTube API key:**")
        paragraphs = """
                You need a Google API key to use this application. Go get yours bellow is 
                just a default key on streamlit secrets. Follow below for more info.
                https://developers.google.com/youtube/v3/getting-started
                """
        st.code(paragraphs, language='text')
        api_key = st.text_input("API key:", type="password", key="api_key",
                                value=st.session_state["api_key"])
        st.write("")
        st.write("")
        st.write("")
        if st.button(label='Verify'):
            st.session_state["API_key_pass"] = check_api_key(api_key, method=0)
        status_banner(session_key="api_key", session_state_key="API_key_pass", op_string="API key")

    with tab2:
        st.write("**SQL server URL:**")
        paragraphs = """
        I'm going to request only SQL server URL, because it will select between local and external DB.
        And no need for multiple user input.
        i.e: for local DB: sqlite:///Database_storage/Utube_DHW-5.db
        for external  SQL: mysql+pymysql://username:password@host:port/dbname
        """
        st.code(paragraphs, language='text')
        sql_url = st.text_input("Database_URL", key="url",
                                value=st.session_state['mysql_config'])
        if st.button(label='Verify', key='sql-verify'):
            st.write("Verifying>>>>")
            sql_db = sql_tube(sql_url)
            if sql_db:
                st.session_state['mysql_config'] = sql_url
                st.session_state["sql_state"] = True
                sql_db.close_sql()
        status_banner(session_key="mysql_config", session_state_key="sql_state", op_string="SQL URI")

    with tab3:
        st.write("**MongoDB server URI**")
        paragraphs = """
        Enter MongoDB server details in following format or just copy paste the URI.
        i.e: mongodb://username:password@host:port/dbname
        """
        st.code(paragraphs, language='text')
        mongo_uri = st.text_input("MongoDB URI:", key="mongo-url",
                                  value=st.session_state['mongo_config'])
        if st.button(label='Verify', key='mongo-verify'):
            st.write("Verifying>>>>")
            mongo_connection = mongo_tube(mongo_uri)
            if mongo_connection:
                st.session_state['mongo_config'] = mongo_uri
                st.session_state["mongo_state"] = True
                mongo_connection.close_mongo()
        status_banner('mongo_config', "mongo_state", "MongoDB URI")
    st.empty()
    st.divider()
    api_colour = colour_pick("API_key_pass")
    sql_colour = colour_pick("sql_state")
    mon_colour = colour_pick("mongo_state")
    repeated = "width: 350px; height: 50px; color: #000; display: flex; justify-content: center; align-items: center; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-size: 18px; text-align: center;"
    html_code = f"""
    <h1 style="colour"> Activation Status: </h1>
    <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f4f4f4;">
    <div style="display: flex; gap: 20px;">
        <div style="background-color: {api_colour}; {repeated}"><h2>API Key</h2></div>
        <div style="background-color: {sql_colour}; {repeated}"><h2>SQL URL</h2></div>
        <div style="background-color: {mon_colour}; {repeated}"><h2>Mongo URI</h2></div>
    </div>
    </body>
    """
    st.html(html_code)
