
# config_page.py
# page one of the application not default page. but API_key verification is done here and SQL configuration done here.

import sqlite3
from utube_DHW_aux_modules import *
import data_con as my_sql


def config_page():
    # here I made Streamlit configuration page for getting apikey and SQL connection data.
    st.subheader("Config")

    # Form 1 for getting API key and validating it.
    with st.form(key='API_form'):
        api_key = st.text_input("API key:", type="password", key="api_key",
                                value=st.session_state["API_key"])
        if st.form_submit_button(label='Verify'):
            if yt.check_api_key(api_key, method=0):
                st.session_state["API_key_pass"] = True
                log.info(f'Tube loaded, API key = {api_key}')
            else:
                st.session_state["API_key_pass"] = False
                log.info(f'API key failed, API key = {api_key}')

    if st.session_state["API_key_pass"]:
        hidden_key = key_hide(st.session_state["API_key"])
        st.success(f"API key passed. \n{hidden_key}", icon="✔️")
    elif not st.session_state["API_key_pass"]:
        hidden_key = key_hide(st.session_state["API_key"])
        st.error(f"Invalid API key !!! \n{hidden_key}", icon="❌")
    else:
        st.info("Just loaded the page configure the api_key !!!", icon=":gear")

# by default for YouTube data extraction API key is a must for extracting the data and uploading to sql and then
# processing it. still, if you skip sql-host details you still can get the Extracted data as Json file with
# channel name as its file_name. but you will lose Analytics page. Form 2 for getting MySQL configuration.

    with st.form(key='SQL_configuration'):
        Selected_DB = st.radio("Select DB option", sql_db_option, horizontal=True)
        if st.form_submit_button(label='Select DB'):
            st.session_state["DB_type"] = Selected_DB

    if st.session_state["DB_type"] == sql_db_option[0]:
        st.info(f"Selected {sql_db_option[0]}")
        with st.form(key='MySQL_cred_form'):
            st.write("⚙️ Enter MySQL server Host details:")
            ls, rs = st.columns(2)
            sql_host = ls.text_input("Hostname/ IP:", key="SQL_host", value=st.session_state['config']['SQL_host'])
            sql_port = ls.text_input("SQL port no :", key="SQL_port", value=st.session_state['config']['SQL_port'])
            sql_user = rs.text_input("SQL Username:", key="SQL_user", value=st.session_state['config']['SQL_user'])
            sql_pswd = rs.text_input("SQL password:", key="SQL_pswd", value=st.session_state['config']['SQL_pswd'],
                                     type="password")
            sql_DB = st.text_input("SQL Database:", key="SQL_DB", value=st.session_state['config']['SQL_DB'])
            if st.form_submit_button(label='Verify'):
                st.write("Verifying>>>>")
                mysql_status_check = my_sql.check_database_availability(sql_host, sql_port, sql_user, sql_pswd, sql_DB)
                if mysql_status_check:
                    st.session_state['config'] = {
                        'SQL_host': sql_host,
                        'SQL_port': sql_port,
                        'SQL_user': sql_user,
                        'SQL_pswd': sql_pswd,
                        'SQL_DB': sql_DB
                    }
                    st.session_state["Active_SQL_connection"] = True
                elif not mysql_status_check:
                    st.error("SQL credentials failed.")
                else:
                    pass

        if st.session_state["Active_SQL_connection"]:
            st.success("Active SQL connection!!!...____")
            st.write("System state configuration ready")
            sql_con_status = "✔️"
        elif not st.session_state["Active_SQL_connection"]:
            sql_con_status = "❌"
        else:
            sql_con_status = "⚠️"
        st.write(f"{sql_con_status} Hostname/ IP: {st.session_state['config']['SQL_host']}")
        st.write(f"{sql_con_status} Host port no: {st.session_state['config']['SQL_port']}")
        st.write(f"{sql_con_status} SQL Username: {st.session_state['config']['SQL_user']}")
        st.write(f"{sql_con_status} SQL password: ", "*" * len(st.session_state['config']['SQL_pswd']))
        st.write(f"{sql_con_status} SQL Database: {st.session_state['config']['SQL_DB']}")

    elif st.session_state["DB_type"] == sql_db_option[1]:
        st.info(f"Selected {sql_db_option[1]}")
        st.success(f"SQLite version : {sqlite3.sqlite_version}")
        st.session_state["Active_SQL_connection"] = True

