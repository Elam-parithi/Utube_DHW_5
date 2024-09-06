from config_and_auxiliary import *


def about_page():
    """
        Users to get a glance and then how to use this app.
        """
    st.subheader("About")
    st.write("""
                This application allows you to extract data from YouTube channels, store it in a JSON file or upload it to a SQL database,
                and analyze the extracted data. Here's how to use it:
            """)

    st.subheader("Steps to Use:")
    st.write("""
                1. Navigate to the Config page to set up your API key and MySQL connection details.
                2. Enter the channel IDs or names in the Home page, and click proceed to extract data.
                3. Once extraction is complete, you can upload the data to your SQL server.
                4. Visit the Analyze page to view analytics about the extracted channels.
                5. Explore the different features of the application and analyze YouTube data efficiently!
            """)

    st.subheader("About Developer:")

    st.write("""
        I'm [Elamparithi](https://www.linkedin.com/in/elamparithi-t/) Neo Data Scientist: Transforming Complexity into Insight with Precision and Purpose.
        Neo Data Scientist: Driven and passionate about leveraging data to uncover insights and solve complex problems with Precision and Purpose, I am transitioning into the field of Data Science after completing an intensive course at GUVI. The curriculum covered Machine Learning, Deep Learning, Artificial Intelligence, Prompt Engineering, Data Visualization, Tableau, PowerBI and more, providing me with a versatile and comprehensive skill set.

        During my career break, I immersed myself in the rapidly evolving world of data science. Inspired by the potential of technology to drive business transformations, I committed to upskilling and pivoting my career towards this exciting field. My objective is to apply my new skills to deliver data-driven solutions that optimize processes, enhance decision-making, and drive growth.

        Throughout my studies, I built and fine-tuned models for predictive analytics, created deep learning models for tasks such as Flat price prediction and text analysis, and developed AI-driven applications to solve real-world problems. I also designed interactive dashboards to facilitate data-driven decision-making for stakeholders.""")



