from config_and_auxiliary import *
import streamlit as st


def analyze_page():
    """
        In this page instead of getting the data directly it will get the last 10 data from the MySQL DB
        which is extracted from Home page and stored in the database mentioned above.
    """
    st.subheader("Analyze")

    
    # A_cursor.execute(sql_query)
    # sql_query_output = A_cursor.fetchall()
