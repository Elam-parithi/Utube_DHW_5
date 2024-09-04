# config_page.py
# page one of the application not default page. but API_key verification is done here and SQL configuration done here.


from data_con import *
import streamlit as st
from youtube_extractor import check_api_key
from utube_DHW_aux_modules import key_hide


def success_banner(session_key, session_state_key, status: bool, op_string: str):
    if status is bool:
        st.session_state[session_state_key] = status
    else:
        raise AttributeError
    with st.empty():
        state_key = st.session_state[session_state_key]
        hidden_key = key_hide(st.session_state[session_key])
        if state_key:
            st.success(f"{op_string} passed. \n{hidden_key}", icon="✔️")
        elif not state_key:
            st.error(f"Invalid {op_string} !!! \n{hidden_key}", icon="❌")
        else:
            st.info(f"Just loaded the page configure the {op_string} !!!", icon=":gear")


def config_page():
    st.subheader("Config")

    with st.form(key='API_form'):
        api_key = st.text_input("API key:", type="password", key="api_key",
                                value=st.session_state["api_key"])
        if st.form_submit_button(label='Verify'):
            check_status = check_api_key(api_key, method=0)
    success_banner("api_key","API_key_pass", check_status,"API key")

    st.divider()
    with st.container():
        tab1, tab2 = st.tabs(['SQL', 'MongoDB'])
        with tab1:
            st.write("**SQL server Host details:**")
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
                    st.success('Successfully connected to the database URI.')
                    sql_db.close_sql()
                else:
                    st.error("SQL credentials failed.")
        with tab2:
            st.write("**MongoDB server**")
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
                    st.success("Connected to MongoDB!")
                    mongo_connection.close_mongo()
                else:
                    st.error(f"Failed to connect to MongoDB.")
