# data_con.py

# this module is to connect with SQL server and upload data.

import os
import json
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


class sql_tube:
    def __init__(self, url=None):
        self.connection_str = url
        self.connection = None
        self.is_connected = None
        """
        Creates and returns a SQLAlchemy engine based on the database type and configuration.
        local DB: sqlite:///Database_storage/Utube_DHW-5.db
        MySQL: mysql+pymysql://username:password@host:port/dbname
        """
        try:
            engine = create_engine(self.connection_str)
            self.connection = engine.connect()
            self.is_connected = True
            # print("sql_tube connected")
        except SQLAlchemyError as e:
            self.is_connected = False
            print(f"Error: {e}")

    def json_2_sql(self, table_name, json_filepath):
        if not os.path.isfile(json_filepath):
            print("File not found!")
            return
        with open(json_filepath, 'r') as file:
            data = json.load(file)
        df = pd.DataFrame(data)
        df.to_sql(table_name, con=self.connection, if_exists='append', index=False)
        print(f"SQL upload successfully")
        return table_name

    def sql_read(self, query):
        # Reads data from SQL database using the provided query.
        try:
            with self.connection as connection:
                result = pd.read_sql(query, con=connection)
                return result
        except SQLAlchemyError as e:
            print(f"Error reading data: {e}")
            return pd.DataFrame()

    def close_sql(self):
        # closing connection
        if self.connection is not None:
            self.connection.close()


class mongo_tube:
    def __init__(self, uri=None):
        self.mongo_uri = uri
        self.client = None
        self.is_connected = None
        try:
            self.client = MongoClient(self.mongo_uri)
            self.client.server_info()
            self.is_connected = True
            # print("mongo_tube connected")
        except Exception as e:
            self.is_connected = False
            print(f"Failed to connect to MongoDB: {e}")

    def close_mongo(self):
        self.client.close()
