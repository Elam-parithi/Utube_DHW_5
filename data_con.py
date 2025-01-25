# data_con.py

# this module is to connect with SQL server and upload data.

import os
import re
import json
import write_3
import pandas as pd
from pathlib import Path
import streamlit as st
from sqlalchemy import text
from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy.exc import SQLAlchemyError
from create_db import check_create_database
from config_and_auxiliary import directory_settings


class sql_tube:
    @staticmethod
    def URL_unmatch_toast():
        st.error("Invalid MySQL URL format! Please use a format like:"
                 "mysql+pymysql://<username>:<password>@<host>:<port>/<dbname>")

    def validate_sql_url(self, url):
        """
        Validates a given URL to ensure it follows the MySQL connection URL format.
        Displays Streamlit pop-up errors if the URL is invalid.

        Args:
            url (str): The MySQL connection URL.
        """

        mysql_pattern = r'^mysql\+pymysql://.+@.+/.+$'
        sqlite_pattern = r'^sqlite:///?.+\.db$'

        if re.match(mysql_pattern, url):
            mysql_url_pattern = re.compile(
                r"^mysql\+pymysql://"
                r"(?P<username>[^:@]+):(?P<password>[^@]+)@"
                r"(?P<host>[^:/]+):(?P<port>[0-9]+)/(?P<dbname>[a-zA-Z0-9_]+)$"
            )
            match = mysql_url_pattern.match(url)
            if not match:
                self.URL_unmatch_toast()
                return False
            else:
                return True
        elif re.match(sqlite_pattern, url):
            st.error("Already, removed support of SQLite. Because, "
                     "when running test on channels likes and others has big integer sqlite does not support it. "
                     "work around is possible. But, I'm sticking with MySQL")
            self.URL_unmatch_toast()
            return False

    def __init__(self, url=None):
        self.connection_str = url
        self.connection = None
        self.is_connected = None
        self.writer = None
        self.engine = None
        """
        Creates and returns a SQLAlchemy engine based on the database type and configuration.
        local DB: sqlite:///Database_storage/Utube_DHW-5.db
        MySQL: mysql+pymysql://username:password@host:port/dbname
        """
        if True:
            try:
                self.engine = check_create_database(self.connection_str)
                self.writer = write_3.DB_writer(self.engine)
                self.connection = self.engine.connect()
                self.is_connected = True
            except SQLAlchemyError as e:
                self.is_connected = False
                print(f"Error: {e}")

    def json_2_sql(self, filepath):  # st.session_state["MySQL_URL"].json_2_sql(filename, file_name)
        extracted_dir = directory_settings['extracted json folder']
        for file in filepath:
            full_path = os.path.join(extracted_dir, file)
            filename = os.path.basename(full_path)
            full_path = str(Path(full_path).with_suffix(".json"))
            print(full_path)

            with open(full_path, 'r') as file_data:
                print(f'processing {filename}...')
                data = json.load(file_data)
                self.writer.write_to_sql(data)
        self.writer.close_it()

    def sql_read(self, query):
        df = None
        try:
            df = pd.read_sql_query(text(query), self.engine)
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            return df

    def close_sql(self):
        # closing connection
        if self.connection is not None:
            self.connection.close()
            self.is_connected = False
            self.engine.dispose()


class mongo_tube:
    """
    This class is for writing the data to the Mongo database.
    """
    def __init__(self, connection_string=None):
        self.mongo_uri = connection_string
        self.client = None
        self.is_connected = False  # Set to False initially
        try:
            self.client = MongoClient(self.mongo_uri)
            self.client.server_info()  # Check if the connection is successful
            self.is_connected = True
            print("mongo_tube connected successfully.")
        except Exception as e:
            self.is_connected = False
            print(f"Failed to connect to MongoDB: {e}")

    def JSON_2_mongo(self, JSON_filename, DB_name, collection) -> None:
        """
        This method call the json file and read it then write to the database and collection
        in Database.
        @param JSON_filename: JSON file path or the file name in the current dir.
        @param DB_name: Database name in the MongoDB
        @param collection: Collection Name in the DB
        @return: None
        """
        if not self.is_connected:
            print("Not connected to MongoDB. Cannot upload data.")
            return
        try:
            db = self.client[DB_name]
            collection = db[collection]
            # Load the JSON file
            with open(JSON_filename, 'r') as file:
                data = json.load(file)
            # Handle single vs. multiple documents
            if isinstance(data, list):
                collection.insert_many(data)
                print(f"Inserted {len(data)} documents into '{collection}' collection.")
            else:
                collection.insert_one(data)
                print(f"Inserted one document into '{collection}' collection.")
        except Exception as e:
            print(f"An error occurred while uploading JSON to MongoDB: {e}")

    def close_mongo(self):
        """
        closes the MongoDB connection and the client.
        @return: None
        """
        if self.client:
            self.client.close()
            self.is_connected = False  # Update the connection status
            print("MongoDB connection closed.")


# Example usage
if __name__ == "__main__":
    load_dotenv('.secrets')
    uri = os.getenv('uri')
    json_file = 'your_json_file.json'  # Update with your file path
    db_name = 'YouTube_DHW'
    collection_name = 'your_collection_name'

    mongo_instance = mongo_tube(uri)

    if mongo_instance.is_connected:
        mongo_instance.JSON_2_mongo(json_file, db_name, collection_name)
        mongo_instance.close_mongo()
