# Utube_website.py

# This is a streamlit website run this directly on command prompt using streamlit run Utube_website.py
from utube_DHW_aux_modules import *
from streamlit_option_menu import option_menu
from annotated_text import annotated_text

from config_page import config_page
from home_page import home_page
from data_storage import Data_storage_tab
from SQL_Analysis import query_sql
from ploting_page import analyze_page
from about_page import about_page


# Streamlit page configuration
st.set_page_config(
    page_title="Utube DHW 5",
    page_icon=r"Icons/Calendula.ico",
    layout='wide',
)


# Streamlit page title and author annotation
st.title("YouTube Data Harvesting and Warehousing")
annotated_text('by ', ('[Elamparithi T](https://www.linkedin.com/in/elamparithi-t/)',
                       'Data Scientist', "#8ef"))
st.divider()
selected_option = option_menu('', ["config", "home", "storage", "analysis", "plot", "about"],
                              icons=['gear', 'house', "database", "list-task", 'bi-bar-chart', 'info-square'],
                              default_index=0, menu_icon="cast", orientation="horizontal")  # orientation="horizontal"

if selected_option == "config":
    config_page()

elif selected_option == "home":
    home_page()

elif selected_option == "storage":
    Data_storage_tab()

elif selected_option == "analysis":
    query_sql()

elif selected_option == "plot":
    analyze_page()

elif selected_option == "about":
    about_page()

