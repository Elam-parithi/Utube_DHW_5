
# YouTube Data Harvesting and Warehousing

![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?logo=linkedin&style=social) [Elamparithi T](https://www.linkedin.com/in/elamparithi-t/)

## Overview

This project focuses on harvesting data from YouTube and warehousing it using SQL, with a frontend interface built using Streamlit. It allows users to efficiently collect, store, and analyze YouTube data.

## Tech used
- MySQL 
- Streamlit
- Google YouTube API
- NLTK (Natural Language Toolkit)
- pandas
- matplotlib and Seaborn 


## Features

- Multi page streamlit website with ability to get credentials for user.
- Harvest YouTube data using the YouTube API
- Store data in an SQL database
- Interactive dashboards and data visualization using Streamlit
- comment `sentiment analysis` on the same page. 

## Getting Started

### Prerequisites

- Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).
- Create a project and obtain YouTube Data API v3 API key from [Google Developers Console](https://console.developers.google.com/)
- you also need Access credentials to SQL DB. anything similar to MySQL would be better.
- And little knowledge on how to use those tech mentioned above.


### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/Elam-parithi/Utube_DHW_4.git
    cd YouTube-Data-Harvesting-and-Warehousing
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To run the application, initiate `main.py`:

   ```bash
   python run main.py
   ```

OR directly run the application file `Utube_website.py`:

   ```bash
   streamlit run Utube_website.py
   ```


## Contact

Feel free to reach out via [LinkedIn](https://www.linkedin.com/in/elamparithi-t/).

---
Developed by Elamparithi T