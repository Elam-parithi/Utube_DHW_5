# Utube_website.py

# This is a streamlit website run this directly on command prompt using streamlit run Utube_website.py
# or Run main.py that will directly redirect this to here.

from utube_DHW_aux_modules import *
from streamlit_option_menu import option_menu
from config_page import config_page
from home_page import home_page
from SQL_Analysis import query_sql
from analyze_page import analyze_page
from about_page import about_page


with st.sidebar:
    selected_option = option_menu('Menu', ["Config", "Home", "MySQL Analysis", "Analyze", "About"],
                                  icons=['gear', 'house', "list-task", 'info-square'],
                                  default_index=1, menu_icon="cast")  # orientation="horizontal"


if selected_option == "Config":
    config_page()

elif selected_option == "Home":
    home_page()

elif selected_option == "MySQL Analysis":
    query_sql()

elif selected_option == "Analyze":
    analyze_page()

elif selected_option == "About":
    about_page()


    

