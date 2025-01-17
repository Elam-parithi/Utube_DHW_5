import json
import streamlit as st


# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data


# Streamlit app
st.title("Display JSON Data in Streamlit")

# File uploader to allow user to upload a JSON file
uploaded_file = st.file_uploader("Choose a JSON file", type="json")

if uploaded_file is not None:
    # Load the JSON data
    data = json.load(uploaded_file)

    # Display the JSON content
    st.subheader("JSON Data:")
    st.json(data)
