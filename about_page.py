from config_and_auxiliary import *

about_html = """
<div class="container">
    <h1>Utube DHW 5 - Application Guide</h1>
    <p>This program was written by <strong>Elamparithi</strong>.</p>
    <p>GitHub Repository: <a href="https://github.com/Elam-parithi/Utube_DHW_5" target="_blank">Fork the Application</a></p>
    <p>LinkedIn: <a href="https://www.linkedin.com/in/elamparithi-t" target="_blank">Elamparithi T</a></p>

    <h2>How to Use the Application</h2>
    <ul>
        <li>1. <a href="#config">Config</a></li>
        <li>2. <a href="#home">Home</a></li>
        <li>3. <a href="#storage">Storage</a></li>
        <li>4. <a href="#analysis">Analysis</a></li>
        <li>5. <a href="#plot">Plot</a></li>
        <li>6. <a href="#about">About</a></li>
    </ul>

    <div id="config" class="section">
        <h2>1. Config</h2>
        <p>The Config tab is used to configure the YouTube API, MySQL connections, and MongoDB URI. This step is crucial for the application to work.</p>
    </div>

    <div id="home" class="section">
        <h2>2. Home</h2>
        <p>For extracting YouTube data:</p>
        <ul>
            <li>Go to the homepage and enter the channel name.</li>
            <li>If you have the channel ID, you can use that too.</li>
            <li>Click <strong>Proceed</strong> and wait for the data to be downloaded.</li>
            <li>The download time taken for the specific channel will be displayed.</li>
        </ul>
        <p>The extracted data is stored in JSON format in the <code>extracted_data</code> folder with date and time format.</p>
    </div>

    <div id="storage" class="section">
        <h2>3. Storage</h2>
        <p>To move the data to SQL and MongoDB servers:</p>
        <ul>
            <li>Use the <strong>"Yes, Upload"</strong> button to upload the data.</li>
            <li>Sentiment analysis is performed and uploaded to SQL separately.</li>
            <li>MongoDB upload is optional.</li>
            <li>Buttons for downloading specific channels are also provided.</li>
            <li>The downloaded JSON file can be used with Tableau and Power BI when SQL and MongoDB connections are not accessible.</li>
        </ul>
    </div>

    <div id="analysis" class="section">
        <h2>4. Analysis</h2>
        <p>This page is used to retrieve data for specific questions using a dropdown menu.</p>
    </div>

    <div id="plot" class="section">
        <h2>5. Plot</h2>
        <p>This page displays various metrics using Matplotlib and Streamlit.</p>
        <p>Multiple charts can be used, but due to constraints, other data visualization tools are recommended for a detailed view.</p>
    </div>

    <div id="about" class="section">
        <h2>6. About</h2>
        <p>This page provides information on how to use the application and details about the owner.</p>
    </div>
</div>
"""
def about_page():
    with open(css_file) as f:
        st.html(f"<style>{format(f.read)}<style>")
    st.html(about_html)
    