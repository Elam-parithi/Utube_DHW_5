#!Utube_DHW_5\.venv\Scripts\python

import datetime
import json
import os
import re
import time

import sqlalchemy.orm

from create_db import *

"""
    Signature:
    Author: Elamparithi
    Last Update: 4 nov 24
"""


def iso_duration_to_seconds(iso_duration: str) -> int:
    """
    Function to convert ISO duration to seconds.

    @param iso_duration: str
    @return: int
    """
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
    if not match:
        if iso_duration == "P0D":
            return 0
        else:
            raise ValueError(f"Invalid ISO 8601 duration format: {iso_duration}")
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def convert_to_datetime(date_string: str) -> datetime.datetime:
    """
    Function to return SQL friendly date and time.

    @param date_string:
    @return:
    """
    # this is for use in Video_class
    date_string = date_string.rstrip('Z')
    return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')


def write_to_sql(Session_name, json_file):
    """
    Function to write JSON data into SQL server using session. and jsonfile_list as input.

    @param Session_name:
    @param json_file: JSON file path.
    @return:
    """
    start_time = time.time()
    session = Session_name()
    filename = os.path.basename(json_file)
    with open(json_file, 'r') as file_data:
        print(f'processing {filename}...')
        data = json.load(file_data)
    channel_data = data[next(iter(data))]
    channel_chid = channel_data["Channel_Id"]
    channel_record = Channel_class(
        channel_id=channel_chid,
        channel_name=channel_data["Channel_Name"],
        channel_type="Place_Holding_NoType",  # need to make up for it. look fo it in chatGPT.
        channel_views=channel_data["Channel_Views"],
        channel_description=channel_data["Channel_Description"],
        channel_status=str(channel_data["Channel_Status"])
    )
    existing_channel = session.query(Channel_class).filter_by(channel_id=channel_chid).first()
    """
    if existing_channel:
        function_str = "
        Channel already exists in the database.
        Don't insert duplicates into the database. 
        Comments and videos have duplicates, duplicate prevention was not included."
        return function_str
    else:
        print(channel_record)
        session.add(channel_record)
    """

    print(channel_record)
    for playlist_data in channel_data["playlist"]:
        playlist_plid = playlist_data["playlist_ID"]
        playlist_record = Playlist_class(
            playlist_id=playlist_plid,
            channel_id=channel_chid,
            playlist_name=playlist_data["playlist_title"]
        )
        session.add(playlist_record)
        for videos_dict in playlist_data["videos"]:
            video_data = videos_dict[next(iter(videos_dict))]
            video_vid = video_data['Video_Id']
            video_record = Video_class(
                video_id=video_vid,
                playlist_id=playlist_plid,
                channel_id=channel_chid,
                video_name=video_data["Video_Name"],
                video_description=video_data["Caption_Status"],
                published_date=convert_to_datetime(video_data["PublishedAt"]),
                view_count=video_data["View_Count"],
                like_count=video_data["Like_Count"],
                dislike_count=video_data["Dislike_Count"],
                favorite_count=video_data["Favorite_Count"],
                comment_count=video_data["Comment_Count"],
                duration=iso_duration_to_seconds(video_data["Duration"]),
                thumbnail=video_data["Thumbnail"],
                caption_status=video_data["Caption_Status"],

            )
            if session.query(Video_class).filter_by(video_id=video_vid).first() is not None:
                session.add(video_record)
            else:
                pass
                # print(f"Video with ID {video_record.video_id}<:=:>{video_record.video_name} already exists.
                # Skipping insertion.")

            for comment_dict in video_data["Comments"].values():
                comment_cid = comment_dict["Comment_Id"]
                comment_record = Comment_class(
                    comment_id=comment_cid,
                    video_id=video_vid,
                    comment_text=comment_dict["Comment_Text"],
                    comment_author=comment_dict["Comment_Author"],
                    comment_published_date=convert_to_datetime(comment_dict["Comment_PublishedAt"])
                )
                session.add(comment_record)
    session.commit()
    end_time = time.time()
    process_time = end_time - start_time
    # Convert process time to HH:MM:SS format
    hours, remainder = divmod(int(process_time), 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"Time taken for {filename}: {formatted_time}"


if __name__ == "__main__":
    DB_name = "gemini_db"
    start_time = time.time()
    con_str = f'mysql+pymysql://guvi_user:1king#lanka@localhost:3306/{DB_name}'
    extracted_dir: str = r"C:\Users\Elamparithi\PycharmProjects\Utube_DHW_5\extracted_data"
    # check_create_database(con_str, DB_name)
    engine = create_engine(con_str, echo=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)

    filepath = ['GUVI-20240907-154356.json',
                'Sahi Siva-20240913-032253.json',
                'Behindwoods TV-20240825-115545.json',
                'SHIVA SAI ENTERTAINMENT CHANNEL-20240824-190244.json']
    for file in filepath:
        full_path = os.path.join(extracted_dir, file)
        result_op = write_to_sql(Session, full_path)
        print(result_op)
    engine.dispose()
    print("Session closed and engine disposed.")
    end_time = time.time()
    process_time = end_time - start_time
    hours, remainder = divmod(int(process_time), 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    print(f"The entire program took {formatted_time}")
