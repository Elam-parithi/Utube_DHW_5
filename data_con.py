# data_con.py
# this module is to connect with SQL server and upload data.

import re
from datetime import datetime
import pandas as pd
import json
from sqlalchemy import create_engine


def check_database_availability(mysql_uri):
    try:
        engine = create_engine(mysql_uri)
        connection = engine.connect()
        connection.close()
        print(f"Successfully connected to the database URI.")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False


def convert_iso_to_mysql_datetime(iso_datetime_str):
    date_obj = datetime.strptime(iso_datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    mysql_datetime_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return mysql_datetime_str


def convert_iso_duration_to_seconds(iso_duration_str):
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(iso_duration_str)
    if not match:
        raise ValueError("Invalid ISO 8601 duration format")
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


# database_url = 'sqlite:///my_database.db'  # SQLite
# database_url = 'mysql+pymysql://user:password@host/dbname'
def upload_json(table_name, json_data, database_url):
    data = json.loads(json_data)
    df = pd.DataFrame(data)
    engine = create_engine(database_url)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    return True

