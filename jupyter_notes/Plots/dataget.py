import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from os import getenv

load_dotenv('../../.secrets')

pre_conn = getenv('pre_conn')
schema_name = getenv('DB_NAME')
connection_string = f'{pre_conn}{schema_name}'

engine = create_engine(connection_string)


def get_query(query):
    try:
        df = pd.read_sql_query(text(query), engine)
        if df.empty:
            print("The query executed successfully, but returned no data.")
        else:
            print("RETURNED SOME DATA")
            return df
    except Exception as e:
        print(f"Error executing query: {e}")
