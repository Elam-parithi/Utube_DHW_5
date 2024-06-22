
# data_con.py
# this module is to connect with SQL server and upload data.

import re
import sqlite3
import mysql.connector
from datetime import datetime
from mysql.connector import Error


def check_database_availability(mysql_hostname, mysql_port, mysql_username, mysql_password, mysql_database):
    try:
        connection = mysql.connector.connect(
            host=mysql_hostname,
            user=mysql_username,
            password=mysql_password,
            database=mysql_database,
            port=mysql_port
        )
        if connection.is_connected():
            print(f"Successfully connected to the database '{mysql_database}' on the MySQL server '{mysql_hostname}'")
            connection.close()
            return True
    except Error as e:
        print(f"Error: {e}")
        return False


def convert_iso_to_mysql_datetime(iso_datetime_str):
    """
    Convert an ISO 8601 date-time string to MySQL DATETIME format.
    :param iso_datetime_str: ISO 8601 date-time string to convert (e.g., '2024-02-13T13:30:29Z').
    :return: Date-time string in MySQL DATETIME format.
    """
    # Parse the ISO 8601 date-time string to a datetime object
    date_obj = datetime.strptime(iso_datetime_str, '%Y-%m-%dT%H:%M:%SZ')

    # Convert the datetime object to MySQL DATETIME format string
    mysql_datetime_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')

    return mysql_datetime_str


def convert_iso_duration_to_mysql_time(iso_duration_str):
    """
    Convert an ISO 8601 duration string to MySQL TIME format.

    :param iso_duration_str: ISO 8601 duration string to convert (e.g., 'PT5M15S').
    :return: Duration in MySQL TIME format (HH:MM:SS).
    """
    # Regular expression to extract hours, minutes, and seconds
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(iso_duration_str)

    if not match:
        raise ValueError("Invalid ISO 8601 duration format")

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0

    # Format to MySQL TIME format (HH:MM:SS)
    mysql_time_str = f'{hours:02}:{minutes:02}:{seconds:02}'
    return mysql_time_str


def parse_duration(duration_str):
    # Extract hours, minutes, and seconds from the duration string
    pattern = re.compile(r'PT(\d+H)?(\d+M)?(\d+S)?')
    match = pattern.match(duration_str)
    if not match:
        return convert_iso_duration_to_mysql_time(duration_str)
        # raise ValueError("Invalid duration format")
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    # Convert the duration to total seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def convert_iso_duration_to_seconds(iso_duration_str):
    """
    Convert an ISO 8601 duration string to total seconds.
    :param iso_duration_str: ISO 8601 duration string to convert (e.g., 'PT5M15S').
    :return: Total duration in seconds as an integer.
    """
    # Regular expression to extract hours, minutes, and seconds
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(iso_duration_str)
    if not match:
        raise ValueError("Invalid ISO 8601 duration format")
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


class CustomConnector:
    def __init__(self, host, host_port, con_username, con_password, database_name="Utube_DHW4",
                 use_local_db=False):
        self.connection = None
        self.cursor = None
        if not use_local_db:
            try:
                self.connection = sqlite3.connect(database_name)
                self.cursor = self.connection.cursor()
                print(f"Successfully connected to the SQLite database '{database_name}'")
            except sqlite3.Error as e:
                print(f"An error occurred while connecting to the SQLite database: {e}")
        elif use_local_db:
            try:
                self.connection = mysql.connector.connect(
                    host=host,
                    user=con_username,
                    password=con_password,
                    database=database_name,
                    port=host_port
                )
            except Error as e:
                print(f"Error: {e}")
        else:
            raise AttributeError

    def create_tables(self):
        if self.connection and self.connection.is_connected():
            self.cursor = self.connection.cursor()

            # Create Channel table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Channel (
                    channel_id VARCHAR(255) PRIMARY KEY,
                    channel_name VARCHAR(255),
                    channel_type VARCHAR(255),
                    channel_views INT,
                    channel_description TEXT,
                    channel_status VARCHAR(255)
                )
            """)

            # Create Playlist table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Playlist (
                    playlist_id VARCHAR(255) PRIMARY KEY,
                    playlist_name VARCHAR(255),
                    channel_id VARCHAR(255)
                )
            """)

            # Create Video table
            self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS Video (
                                video_id VARCHAR(255) PRIMARY KEY,
                                playlist_id VARCHAR(255),
                                video_name VARCHAR(255),
                                video_description TEXT,
                                publish_date DATETIME,
                                view_count INT,
                                like_count INT,
                                dislike_count INT,
                                favourite_count INT,
                                comment_count INT,
                                duration INT,
                                thumbnail VARCHAR(255),
                                caption_status VARCHAR(255)
                            )
                        """)

            # Create Comment table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Comment (
                    comment_id VARCHAR(255) PRIMARY KEY,
                    video_id VARCHAR(255),
                    comment_text TEXT,
                    comment_author VARCHAR(255),
                    comment_published_date DATETIME
                )
            """)

            self.connection.commit()
            print("Tables created successfully")
        else:
            print("Database connection is not established")

    def upload_channel_data(self, channel_id, name, channel_type, views, description, status):
        if self.connection and self.connection.is_connected():
            self.cursor = self.connection.cursor()
            # Insert data into Channel table
            query = "INSERT INTO Channel (channel_id, channel_name, channel_type, channel_views, channel_description, channel_status) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (channel_id, name, channel_type, views, description, status))
            self.connection.commit()
            print("Data uploaded to Channel table successfully")
        else:
            print("Database connection is not established")

    def upload_playlist_data(self, playlist_name, playlist_id, channel_id):
        if self.connection and self.connection.is_connected():
            self.cursor = self.connection.cursor()
            # Insert data into Playlist table
            query = "INSERT INTO Playlist (playlist_name, playlist_id, channel_id) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (playlist_name, playlist_id, channel_id))
            self.connection.commit()
            print("Data uploaded to Playlist table successfully")
        else:
            print("Database connection is not established")

    def upload_video_data(self, video_id, playlist_id, video_name, video_description, publish_date, view_count,
                          like_count, dislike_count, favourite_count, comment_count, duration, thumbnail,
                          caption_status):
        if self.connection and self.connection.is_connected():
            self.cursor = self.connection.cursor()
            # Insert data into Video table
            query = "INSERT INTO Video (video_id, playlist_id, video_name, video_description, publish_date, view_count, like_count, dislike_count, favourite_count, comment_count, duration, thumbnail, caption_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (
                video_id, playlist_id, video_name, video_description, convert_iso_to_mysql_datetime(publish_date),
                view_count,
                like_count, dislike_count, favourite_count, comment_count, convert_iso_duration_to_seconds(duration),
                thumbnail,
                caption_status))
            self.connection.commit()
            print("Data uploaded to Video table successfully")
        else:
            print("Database connection is not established")

    def upload_comment_data(self, comment_id, video_id, comment_text, comment_author, comment_published_date):
        if self.connection and self.connection.is_connected():
            self.cursor = self.connection.cursor()
            # Insert data into Comment table
            query = "INSERT INTO Comment (comment_id, video_id, comment_text, comment_author, comment_published_date) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (comment_id, video_id, comment_text, comment_author, comment_published_date))
            self.connection.commit()
            print("Data uploaded to Comment table successfully")
        else:
            print("Database connection is not established")
