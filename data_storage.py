# data_storage.py

# This is data_storage here we process the data we extracted in home page.

import pandas as pd
import streamlit as st
import json
from data_con import upload_json
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def get_sqlalchemy_engine(db_type, config):
    """
    Creates and returns a SQLAlchemy engine based on the database type and configuration.
    """
    if db_type == 'MySQL':
        host = config['SQL_host']
        port = config['SQL_port']
        username = config['SQL_user']
        password = config['SQL_pswd']
        database_name = config['SQL_DB']
        connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}"
    else:  # Assuming SQLite as default
        connection_string = f"sqlite:///{config.get('default_localDB_filename', 'local.db')}"

    return create_engine(connection_string)


def upload_data_to_sql(engine, table_name, data):
    """
    Uploads data to the specified table in the SQL database.
    """
    try:
        with engine.connect() as connection:
            data.to_sql(table_name, con=connection, if_exists='append', index=False)
            print(f"Data uploaded to table {table_name}.")
    except SQLAlchemyError as e:
        print(f"Error uploading data: {e}")


def read_data_from_sql(engine, query):
    """
    Reads data from SQL database using the provided query.
    """
    try:
        with engine.connect() as connection:
            result = pd.read_sql(query, con=connection)
            return result
    except SQLAlchemyError as e:
        print(f"Error reading data: {e}")
        return pd.DataFrame()


def save_json_to_file(data, filename):
    """
    Saves data to a JSON file.
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving data to file: {e}")


def load_json_from_file(filename):
    """
    Loads data from a JSON file.
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading data from file: {e}")
        return {}


def Data_storage_tab():
    """
    Data_storage_processing. processing the data in streamlit.
    """
    st.subheader("Non-Volatile Data Storage processing.")
    extracted_json_data = "daat"
    storage_option = st.selectbox('select Storage option', ['sqlite', 'MySQL', 'MongoDB', 'JSON'])
    if storage_option == 'sqlite':
        pass
    st.json(extracted_json_data)
