
from os import path, listdir
from pathlib import Path
import streamlit_tags
import streamlit as st
from data_con import *

# Custom CSS for styling the button
button_style = """
    <style>
    .custom-button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        outline: none;
        color: #fff;
        background-color: lightgreen;
        border: none;
        border-radius: 15px;
        box-shadow: 0 9px #999;
    }

    .custom-button:hover {background-color: lightyellow}

    .custom-button:active {
        background-color: #3e8e41;
        box-shadow: 0 5px #666;
        transform: translateY(4px);
    }
    </style>
"""

# Display the button using HTML
clicked = st.html(f"""{button_style}<a href="#" class="custom-button">Click Me</a>""")

# Detecting click (using a workaround)
if st.session_state.get('button_clicked') == 'clicked':
    st.write("Button clicked!")

# Workaround for button click (using a hidden Streamlit button)
if st.button('Hidden button', key='button_click_trigger'):
    st.session_state['button_clicked'] = 'clicked'

# button to procced with option.
if procced_storage:
    if storage_sql:
        sql_store_con = sql_tube(st.session_state["mysql_config"])
        for json_filepath in selected_files:
            sql_store_con.json_2_sql(str(path.basename(json_filepath)), json_filepath)
    elif storage_mon:
        mongo_tube(st.session_state["mongo_config"])
    else:
        raise KeyError


import streamlit as st

# Custom CSS for the button styling
st.html(
    """
    <style>
    .custom-button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        color: white;
        background-color: #3498db;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        transition: background-color 0.3s, transform 0.2s;
    }

    .custom-button:hover {
        background-color: #2980b9;
    }

    .custom-button:active {
        background-color: #1d6fa5;
        transform: translateY(2px);
    }
    </style>
    """
)

# Function to handle the button click event
def button_clicked():
    st.write("Streamlit button pressed")

# HTML for the button
button_html = '<button class="custom-button" onclick="window.streamlitButtonClick()">Press Me!</button>'

# Display the button using Streamlit's HTML component
st.html(button_html)

# JavaScript code to connect the button click to Streamlit
st.html(
    """
    <script>
    window.streamlitButtonClick = function() {
        // Call Streamlit function via button click
        window.parent.postMessage({isStreamlitEvent: true, type: 'buttonClicked'}, '*');
    }
    </script>
    """
)

# Streamlit listener for custom button click event
if 'buttonClicked' not in st.session_state:
    st.session_state.buttonClicked = False

# JavaScript callback handler for the button click
def js_event_listener():
    st.session_state.buttonClicked = True
    button_clicked()

st.html(
    """
    <script>
    window.addEventListener('message', function(event) {
        if (event.data && event.data.isStreamlitEvent && event.data.type === 'buttonClicked') {
            window.parent.streamlitWebSocketSend({type: 'streamlitCustomButton', value: true});
        }
    });
    </script>
    """,
)

# Listen to the WebSocket event
if st.session_state.buttonClicked:
    js_event_listener()
