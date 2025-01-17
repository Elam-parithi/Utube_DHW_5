import streamlit as st
from code_editor import code_editor

st.title("MySQL Query Editor with Extracted Code")

default_sql = """
-- Example SQL Query
SELECT * FROM your_table
WHERE condition = 'value';
"""

custom_button_setting = [{"name":"Run",
                          "hasText":True,
                          "alwaysOn":True,
                          "feather":"Play",
                          "commands":["returnSelection"],
                          "style":{"bottom":"0.44rem", "right":"0.4rem"}
                          }]

response = code_editor(
    code=default_sql,
    lang="sql",
    height=300,
    key="sql_editor",
    buttons=custom_button_setting,
    theme="dark"
)
# Extract the code text from the response dictionary

if response:
    print(response)

if st.button("Execute Query"):
    sql_query = response.get('text', '')  # Default to an empty string if 'text' key is missing
    st.write("Executed SQL:", sql_query)  # Use the extracted code string
