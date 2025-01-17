# extractor_app.py

# This is a streamlit website run this directly on command prompt using "streamlit run extractor_app.py"

from PIL import Image
from config_and_auxiliary import *
from streamlit_option_menu import option_menu
from annotated_text import annotated_text

from config_page import config_page
from home_page import home_page
from data_storage import Data_storage_tab
from sql_analysis import query_sql
from plotting_page import analyze_page
from about_page import about_page
from html_addon import statusbar

import logging
from logging.handlers import RotatingFileHandler

logfile = locate_log('app', 'youtube_dhw.log')
logger = logging.getLogger('extractor_app')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logfile, maxBytes=5 * 1024 * 1024, backupCount=20)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


img = Image.open(basic_settings['image_path'])
img = img.resize((16, 16))

# Streamlit page configuration
st.set_page_config(
    page_title="Utube DHW 5",
    page_icon=img,
    layout='wide'
)
st.header(":sunglasses: :red[YouTube] :blue[DataHarvesting] and :green[WareHosing]")
annotated_text('by ', ('[Elamparithi T](https://www.linkedin.com/in/elamparithi-t/)',
                       'Data Scientist  |  Former System Administrator', "#d08cf8"))
with open(css_file) as f:
    st.markdown(f"<style>{format(f.read())}<style>",
                unsafe_allow_html=True)

statusbar()
selected_option = option_menu('', ["config", "home", "storage", "analysis", "plot", "about"],
                              icons=['gear', 'house', "database", "list-task", 'bi-bar-chart', 'info-square'],
                              default_index=basic_settings['default_index'], orientation="horizontal")

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
