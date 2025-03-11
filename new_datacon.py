# data_con.py

# this module is to connect with SQL server and upload data.

import re
import json
import datetime
import pymysql.err
import pandas as pd
import sqlalchemy.orm
import sqlalchemy.exc
from pathlib import Path

from sqlalchemy import text
from pandas import DataFrame
from sqlalchemy.exc import SQLAlchemyError
from create_db import *
from create_db import Comment_class
from NLTK_Sentiment import CommentAnalyzer
from config_and_auxiliary import directory_settings

"""
    Author: Elamparithi 
    Last Update: 04 feb 2025
    Not functional as of last update.
"""
# todo: parse full code to chatgpt and get this code completed.
#  or try using gemini, if not leave it on time consuming code and move on to other projects.

# Logging setup
for handler in logging.getLogger("sqlalchemy").handlers:
    logging.getLogger("sqlalchemy").removeHandler(handler)

write3_log = locate_log('oth', 'datacon.log')
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(write3_log, encoding='utf-8')])
write3_logger = logging.getLogger('datacon')

# Directory loaded.
extracted_dir = directory_settings['extracted json folder']


class sql_tube:
    def __init__(self, url=None):
        self.connection_str = url
        self.engine = None
        try:
            self.engine = check_create_database(self.connection_str)
            Class_Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
            self.session = Class_Session()
        except pymysql.err.OperationalError as e:
            write3_logger.error(f"OperationalError: {e}")
            print("Database access error! Check user permissions.")
            self.engine = None  # Ensure engine is set to None if connection fails
        except SQLAlchemyError as e:
            print(f"SQLAlchemy Error: {e}")

    @staticmethod
    def iso_duration_to_seconds(iso_duration: str) -> int:
        """
        Function to convert ISO duration to ss.
        @param iso_duration: str
        @return: int
        """
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
        if not match:
            if iso_duration == "P0D":
                return 0
            else:
                raise ValueError(f"Invalid ISO 8601 duration format: {iso_duration}")
        hh = int(match.group(1) or 0)
        mm = int(match.group(2) or 0)
        ss = int(match.group(3) or 0)
        total_seconds = hh * 3600 + mm * 60 + ss
        return total_seconds

    @staticmethod
    def convert_to_datetime(date_string: str) -> datetime.datetime:
        """
        Function to return SQL friendly date and time.

        @param date_string:
        @return: SQL Data and Time format
        """
        # this is for use in Video_class
        date_string = date_string.rstrip('Z')
        return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')

    def write_handler(self, data_for_table):
        """
        Optimized function for batch inserting data into SQL.
        """
        try:
            if isinstance(data_for_table, list):
                # self.session.add_all(data_for_table)
                for item in data_for_table:
                    print(**item)
            else:
                self.session.add(data_for_table)
        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()
            write3_logger.warning(f"Integrity Error: {e}")
            print(f"Integrity Error")
        except Exception as e:
            self.session.rollback()
            write3_logger.error(f"Unexpected error: {e}")
            print("Unexpected error")
        finally:
            self.session.commit()
            self.session.expunge_all()

    def write_to_sql(self, json_datum: dict):
        """
        Write json data to SQL with for loop.
        @param json_datum: entire json file as nested dict. (GUVI format only: from youtube_extractor.py)
        @return: None
        """
        self.session.execute(text("SET FOREIGN_KEY_CHECKS=0;"))

        channel_data = json_datum[next(iter(json_datum))]
        channel_chid = channel_data["Channel_Id"]

        # Insert Channel
        channel_record = {
            "channel_id":channel_chid,
            "channel_name":channel_data["Channel_Name"],
            "channel_type":channel_data["Channel_type"],
            "channel_views":channel_data["Channel_Views"],
            "channel_description":channel_data["Channel_Description"],
            "channel_status":str(channel_data["Channel_Status"])
        }

        # Check if the channel exists
        existing_channel = self.session.query(Channel_class).filter_by(channel_id=channel_chid).first()

        if not existing_channel:
            write3_logger.info(f"Adding new channel: {channel_record}")
            insert_channel_sql = text("""
                INSERT INTO channel (channel_id, channel_name, channel_type, channel_views, channel_description, channel_status)
                VALUES (:channel_id, :channel_name, :channel_type, :channel_views, :channel_description, :channel_status)
            """)
            self.session.execute(insert_channel_sql, channel_record)
            self.session.commit()
            print(f"\t├── Channel written")
        else:
            write3_logger.debug(f"Channel {channel_chid} already exists. Skipping addition.")

        # Prepare records
        playlist_records = []
        video_records = []
        comment_records = []

        # Process Playlists, Videos, and Comments
        for playlist_data in channel_data["playlist"]:
            playlist_plid = playlist_data["playlist_ID"]
            playlist_record = {
                "playlist_id":playlist_plid,
                "channel_id":channel_chid,
                "playlist_name":playlist_data["playlist_title"]
            }
            playlist_records.append(playlist_record)

            for videos_dict in playlist_data["videos"]:
                video_data = videos_dict[next(iter(videos_dict))]
                video_vid = video_data['Video_Id']

                video_record = {
                    "video_id":video_vid,
                    "playlist_id":playlist_plid,
                    "channel_id":channel_chid,
                    "video_name":video_data["Video_Name"],
                    "video_description":video_data["Video_Description"],
                    "published_date":self.convert_to_datetime(video_data["PublishedAt"]),
                    "view_count":video_data["View_Count"],
                    "like_count":video_data["Like_Count"],
                    "dislike_count":video_data["Dislike_Count"],
                    "favorite_count":video_data["Favorite_Count"],
                    "comment_count":video_data["Comment_Count"],
                    "duration":self.iso_duration_to_seconds(video_data["Duration"]),
                    "thumbnail":video_data["Thumbnail"],
                    "caption_status":video_data["Caption_Status"]
                }

                # Insert only if the video does not already exist
                if not self.session.query(Video_class).filter_by(video_id=video_vid).first():
                    video_records.append(video_record)
                else:
                    vid_dbug = (f"Video with ID {video_vid} - {video_record['video_name']} "
                                f"already exists. Skipping insertion.")
                    write3_logger.debug(vid_dbug)

                # Process Comments
                for comment_dict in video_data.get("Comments", {}).values():
                    comment_records.append({
                        "comment_id":comment_dict["Comment_Id"],
                        "video_id":video_vid,
                        "comment_text":comment_dict["Comment_Text"],
                        "comment_author":comment_dict["Comment_Author"],
                        "comment_published_date":self.convert_to_datetime(comment_dict["Comment_PublishedAt"])
                    })

        # Helper function to count records
        def por_lites(gemini: list):
            act_len = len(gemini)
            uni_len = len({frozenset(item.items()) for item in gemini})  # Handle dicts correctly
            mis_len = act_len - uni_len
            return f"{act_len} - {mis_len}"

        # Bulk Insert Playlists
        if playlist_records:
            try:
                insert_playlist_sql = text("""
                    INSERT INTO playlist (playlist_id, channel_id, playlist_name)
                    VALUES (:playlist_id, :channel_id, :playlist_name)
                """)
                self.session.execute(insert_playlist_sql, playlist_records)  # executemany internally
                self.session.commit()
                print(f"\t├── {por_lites(playlist_records)} playlists written")
            except Exception as e:
                self.session.rollback()
                print(f"Bulk insert error (Playlists): {e}")

        # Bulk Insert Videos
        if video_records:
            try:
                insert_video_sql = text("""
                    INSERT INTO video (
                        video_id, playlist_id, channel_id, video_name, video_description,
                        published_date, view_count, like_count, dislike_count, 
                        favorite_count, comment_count, duration, thumbnail, caption_status
                    )
                    VALUES (
                        :video_id, :playlist_id, :channel_id, :video_name, :video_description,
                        :published_date, :view_count, :like_count, :dislike_count,
                        :favorite_count, :comment_count, :duration, :thumbnail, :caption_status
                    )
                """)
                self.session.execute(insert_video_sql, video_records)
                self.session.commit()
                print(f"\t├── {por_lites(video_records)} videos written")
            except Exception as e:
                self.session.rollback()
                print(f"Bulk insert error (Videos): {e}")

        # Bulk Insert Comments
        if comment_records:
            try:
                insert_comment_sql = text("""
                    INSERT INTO comment (comment_id, video_id, comment_text, comment_author, comment_published_date)
                    VALUES (:comment_id, :video_id, :comment_text, :comment_author, :comment_published_date)
                """)
                self.session.execute(insert_comment_sql, comment_records)
                self.session.commit()
                print(f"\t└── {por_lites(comment_records)} comments written")
            except Exception as e:
                self.session.rollback()
                print(f"Bulk insert error (Comments): {e}")

    def sentiment_analysis_update(self):
        """
        separate method for reading and updating the table with sentiment and sentiment_type.
        processing the comment text when running the extraction
        will increase the extraction time. Also, might lead to other issues.
        """
        nltk_analyzer = CommentAnalyzer()
        comments = self.session.query(Comment_class).all()
        for comment in comments:
            content_text = comment.comment_text
            compound_result = nltk_analyzer.analyze_sentiment(content_text)
            if compound_result:
                sentiment_string = nltk_analyzer.sentiment_type(compound_result)
                comment.sentiment = compound_result['compound']
                comment.sentiment_type = sentiment_string
                self.session.add(comment)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            write3_logger.debug(f"Error Commenting: {e}")

    def json_2_sql(self, file_paths: list) -> bool:
        for file_name in file_paths:
            extr_fullpath = str(os.path.join(extracted_dir, file_name))
            joined_fullpath = Path(extr_fullpath).with_suffix(".json")
            json_fullpath = str(joined_fullpath)
            with open(json_fullpath, 'r') as opened_file:
                dictionary_data = json.load(opened_file)
                self.write_to_sql(dictionary_data)
        self.sentiment_analysis_update()
        return True

    def sql_read(self, query: str) -> DataFrame | None:
        """
        Gets the SQLquery and provides the result.
        @param query: str
        @return: DataFrame | None
        """
        try:
            return pd.read_sql_query(text(query), self.engine)
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def close_sql(self):
        """
        Closing session and engine.
        @return: None
        """
        self.session.close()
        if self.engine:
            self.engine.dispose()


# Example usage
if __name__ == "__main__":
    extracted_dir: str = r"extracted_data"
    load_dotenv('.secrets')
    URL_word = os.getenv('URL_word')

    writer = sql_tube(url=URL_word)
    filepath = ['SpaceRex-20250131-095147.json',  # 'Akshay Expeditions-20250202-144107.json',
                'The Regent-20250202-143959.json', 'Elamparithi -20250202-144134.json',
                'GUVI-20250202-114916.json']
    for file in filepath:
        full_path = os.path.join(extracted_dir, file)
        filename = os.path.basename(full_path)
        with open(full_path, 'r') as file_data:
            print(f' preprocessing {filename}...')
            data = json.load(file_data)
            writer.write_to_sql(data)
    print("Data writen to sql, updating sentiment")
    writer.sentiment_analysis_update()
    print("Sentiment update complete")
    writer.close_sql()
    print("Session closed and engine disposed.")
