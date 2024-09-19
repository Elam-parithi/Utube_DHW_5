from config_and_auxiliary import *


def analyze_page():
    """
        In this page instead of getting the data directly it will get the last 10 data from the MySQL DB
        which is extracted from Home page and stored in the database mentioned above.
    """
    st.subheader("Analyze")
