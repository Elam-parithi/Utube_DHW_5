# [YouTube Data Harvesting and Warehousing](https://elam-parithi.github.io/Utube_DHW_5/)

<a href="https://www.linkedin.com/in/elamparithi-t/"><img src="Icons/LI-Logo.png" alt="linkedin.com" width="120" height="40"></a>

## Overview
This project focuses on harvesting data from YouTube and warehousing it using SQL, with a frontend interface built using Streamlit. It allows users to efficiently collect, store, and analyze YouTube data. Additional details available on [Utube_DHW_5](https://elam-parithi.github.io/Utube_DHW_5/) hosted using GitHub pages.

## Utube_DHW link
[elam-parithi.github.io/Utube_DHW_5](https://elam-parithi.github.io/Utube_DHW_5/)

## Tech used
- MySQL 
- Streamlit
- Google YouTube API
- NLTK (Natural Language ToolKit)
- pandas
- matplotlib and Seaborn
- HTML and CSS
## Features
- Multipage streamlit website with ability to get credentials for user.
- Harvest YouTube data using the YouTube API
- Store data in an SQL database
- Interactive dashboards and data visualization using Streamlit
- comment `sentiment analysis` on the plots page. 
## Getting Started
### Prerequisites
- Make sure you have `Python 3.12.0` installed on your system. You can download it from [python.org](https://www.python.org/).
- Create a project and obtain YouTube Data API v3 API key from [Google Developers Console](https://console.developers.google.com/)
- you also need Access credentials to SQL DB. Anything similar to MySQL would be better.
- MongoDB URI is optional. There is option to go for it. 
- And little knowledge on how to use those tech mentioned above. 
### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/Elam-parithi/Utube_DHW_5.git
    cd Utube_DHW_5
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
   if you are facing installing with this file. go with `manual_requirenments.txt` file.
   Installing with different operating system or environment leads to this error.
5. set '.streamlit/secrets.toml' file:
   - Read [secret_configuration.md](secret_configuration.md) for configuring secrets.toml file.
### Running the Application
To run the application, initiate `main.py`:
   ```bash
   python run main.py
   ```
OR directly run the application file `Utube_website.py`:
   ```bash
   streamlit run extractor_app.py
   ```
## Contact
Feel free to reach out via 

<img src="Icons/LI-In-Bug.png" alt="linkedin.com" width="42" height="38"></a>
<a href="https://github.com/Elam-parithi">
<img src="Icons/github-mark-white.png" alt="linkedin.com" width="42" height="38"></a>

---
Developed by [Elamparithi](https://www.linkedin.com/in/elamparithi-t/)
