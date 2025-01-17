import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://guvi_user:1king#lanka@localhost:3306/youtube_local")


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
