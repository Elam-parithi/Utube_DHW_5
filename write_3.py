#!Utube_DHW_5\.venv\Scripts\python

"""
Module for writing a json dictionary to MySQL DataBase.
"""

import re
import json
import datetime
import pymysql.err
import sqlalchemy.orm
import sqlalchemy.exc
from create_db import *
from NLTK_Sentiment import *
from config_and_auxiliary import locate_log
import logging


"""
    Author: Elamparithi 
    Last Update: 24 nov 24
    Fully functional as of last update.
"""

# SADeprecationWarning: The Session.close_all() method is deprecated and will be removed in a future release.
# Please refer to session.close_all_sessions(). (deprecated since: 1.3)

for handler in logging.getLogger("sqlalchemy").handlers:
    logging.getLogger("sqlalchemy").removeHandler(handler)

write3_log = locate_log('app', 'write_3.log')
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(write3_log, encoding='utf-8')])
write3_logger = logging.getLogger('write_3')


class DB_writer:
    def __init__(self, engine_name):
        self.engine = engine_name
        Class_Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = Class_Session()

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
        For handling auto flush, errors and rollback.
        @param data_for_table: record to add in session, then commiting.
        @return: None
        """
        try:
            with self.session.no_autoflush:
                if isinstance(data_for_table, list):
                    self.session.bulk_save_objects(data_for_table)
                else:
                    self.session.add(data_for_table)
        except sqlalchemy.exc.IntegrityError as e:  # sqlalchemy.exc.IntegrityError
            self.session.rollback()  # Roll back the session after an error
            matches = re.findall(r"Duplicate entry", str(e))
            if 0 < len(matches):
                write3_logger.debug("Duplicate entry detected, passing the error up.")
                pass
            else:
                write3_logger.warning("foreign relations not found.")
                write3_logger.warning(f"Error occurred: {e}")
        except pymysql.err.IntegrityError:
            self.session.rollback()
            write3_logger.warning("Pymysql error")

    def write_to_sql(self, json_datum: dict):
        """
        Write json data to SQL with for loop.
        @param json_datum: entire json file as nested dict. (GUVI format only: from youtube_extractor.py)
        @return: None
        """
        channel_data = json_datum[next(iter(json_datum))]
        channel_chid = channel_data["Channel_Id"]
        channel_record = Channel_class(
            channel_id=channel_chid,
            channel_name=channel_data["Channel_Name"],
            channel_type="Place_Holding_NoType",  # need to make up for it. look for it in chatGPT.
            channel_views=channel_data["Channel_Views"],
            channel_description=channel_data["Channel_Description"],
            channel_status=str(channel_data["Channel_Status"])
        )
        existing_channel = self.session.query(Channel_class).filter_by(channel_id=channel_chid).first()
        if not existing_channel:
            write3_logger.info(f"Adding new channel: {channel_record}")
            self.write_handler(channel_record)
            # self.session.commit()  # prevents integrity error

        else:
            write3_logger.debug(f"Channel {channel_chid} already exists. Skipping addition.")

        playlist_records = []
        video_records = []
        comment_records = []

        for playlist_data in channel_data["playlist"]:
            playlist_plid = playlist_data["playlist_ID"]
            playlist_record = Playlist_class(
                playlist_id=playlist_plid,
                channel_id=channel_chid,
                playlist_name=playlist_data["playlist_title"]
            )
            # self.write_handler(playlist_record)
            playlist_records.append(playlist_record)

            for videos_dict in playlist_data["videos"]:
                video_data = videos_dict[next(iter(videos_dict))]
                video_vid = video_data['Video_Id']
                video_record = Video_class(
                    video_id=video_vid,
                    playlist_id=playlist_plid,
                    channel_id=channel_chid,
                    video_name=video_data["Video_Name"],
                    video_description=video_data["Caption_Status"],
                    published_date=self.convert_to_datetime(video_data["PublishedAt"]),
                    view_count=video_data["View_Count"],
                    like_count=video_data["Like_Count"],
                    dislike_count=video_data["Dislike_Count"],
                    favorite_count=video_data["Favorite_Count"],
                    comment_count=video_data["Comment_Count"],
                    duration=self.iso_duration_to_seconds(video_data["Duration"]),
                    thumbnail=video_data["Thumbnail"],
                    caption_status=video_data["Caption_Status"],

                )
                if not self.session.query(Video_class).filter_by(video_id=video_vid).first():
                    video_records.append(video_record)
                    # self.write_handler(video_record)
                    # self.session.commit()  # prevents integrity error on adding comments record
                    # both playlist and videos writen here(commit)
                else:
                    vid_dbug = (f"Video with ID {video_record.video_id} - {video_record.video_name} "
                                f"already exists. Skipping insertion.")
                    write3_logger.debug(vid_dbug)

                for comment_dict in video_data["Comments"].values():
                    comment_cid = comment_dict["Comment_Id"]
                    comment_ctext = comment_dict["Comment_Text"]
                    comment_record = Comment_class(
                        comment_id=comment_cid,
                        video_id=video_vid,
                        comment_text=comment_ctext,
                        comment_author=comment_dict["Comment_Author"],
                        comment_published_date=self.convert_to_datetime(comment_dict["Comment_PublishedAt"])
                        # sentiment and sentiment_type will be processed separately for speed.
                    )
                    # self.write_handler(comment_record)
                    comment_records.append(comment_record)
        if playlist_records:
            self.write_handler(playlist_records)
        if video_records:
            self.write_handler(video_records)
        if comment_records:
            self.write_handler(comment_records)
        self.session.commit()  # for playlist as it is flushed on video processing. this only process comments records.

    def sentiment_analysis_update(self):
        """
        separate method for reading and updating the table with sentiment and sentiment_type.
        processing the comment text when running the extraction
        will increase the extraction time. Also, might lead to other issues.
        """
        # print("Sentiment analysis started.")
        nltk_analyzer = CommentAnalyzer()
        comments = self.session.query(Comment_class).all()
        # print(len(comments))
        for comment in comments:
            content_text = comment.comment_text
            # print(content_text)
            compound_result = nltk_analyzer.analyze_sentiment(content_text)
            if compound_result:
                sentiment_string = nltk_analyzer.sentiment_type(compound_result)
                comment.sentiment = compound_result['compound']
                # print(f"Got compound result {comment.sentiment}")
                comment.sentiment_type = sentiment_string
                self.session.add(comment)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            write3_logger.debug(f"Error Commenting: {e}")

    def close_it(self):
        """
        Closing session and engine.
        @return: None
        """
        self.session.close()
        if self.engine:
            self.engine.dispose()


if __name__ == "__main__":
    load_dotenv('.secrets')
    db_precon = os.getenv('pre_conn')
    DB_name = os.getenv('DB_NAME')
    extracted_dir: str = r"extracted_data"

    filepath = ['Behindwoods TV-20240825-115545.json',
                'Madras foodie-20241124-040846.json','Sahi Siva-20240913-032253.json',
                'SHIVA SAI ENTERTAINMENT CHANNEL-20240824-190244.json']   # list of files here.

    engine = check_create_database(f'{db_precon}{DB_name}')
    writer = DB_writer(engine)
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
    writer.close_it()
    print("Session closed and engine disposed.")
