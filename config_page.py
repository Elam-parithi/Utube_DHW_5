# config_page.py
# page one of the application not default page. but API_key verification is done here and SQL configuration done here.

from utube_DHW_aux_modules import *
import data_con as my_sql
from pymongo import MongoClient


def config_page():
    st.subheader("Config")

    with st.form(key='API_form'):
        api_key = st.text_input("API key:", type="password", key="api_key",
                                value=st.session_state["api_key"])
        if st.form_submit_button(label='Verify'):
            if yt.check_api_key(api_key, method=0):
                st.session_state["API_key_pass"] = True
            else:
                st.session_state["API_key_pass"] = False
    with st.empty():
        if st.session_state["API_key_pass"]:
            hidden_key = key_hide(st.session_state["api_key"])
            st.success(f"API key passed. \n{hidden_key}", icon="✔️")
        elif not st.session_state["API_key_pass"]:
            hidden_key = key_hide(st.session_state["api_key"])
            st.error(f"Invalid API key !!! \n{hidden_key}", icon="❌")
        else:
            st.info("Just loaded the page configure the API key !!!", icon=":gear")

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
            st.code(paragraphs, language= 'text')
            sql_url = st.text_input("Database_URL", key="url",
                                    value=st.session_state['mysql_config'])
            if st.button(label='Verify', key='sql-verify'):
                st.write("Verifying>>>>")
                mysql_status_check = my_sql.check_database_availability(sql_url)
                if mysql_status_check:
                    st.session_state['mysql_config'] = sql_url
                    st.success('Successfully connected to the database URI.')
                else:
                    st.error("SQL credentials failed.")
        with tab2:
            st.write("**MongoDB server**")
            paragraphs = """
            Enter MongoDB server details in following format or just copy paste the URI.
            i.e: mongodb://username:password@host:port/dbname
            """
            st.code(paragraphs, language= 'text')
            mongo_uri = st.text_input("MongoDB URI:", key="mongo-url",
                                      value=st.session_state['mongo_config'])
            if st.button(label='Verify', key='mongo-verify'):
                st.write("Verifying>>>>")
                try:
                    client = MongoClient(mongo_uri)
                    client.server_info()
                    st.session_state['mongo_config'] = mongo_uri
                    st.success("Connected to MongoDB!")
                except Exception as e:
                    st.error(f"Failed to connect to MongoDB: {e}")

