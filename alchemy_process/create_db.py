
import os, re
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Text, DateTime, Index
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

import json
Base = declarative_base()

DB_name = "guvi_test_orm.db"
"""
db_file = os.path.join(os.path.curdir, DB_name)
if os.path.exists(db_file):
    os.remove(db_file)
    print(f'File Already Exists => {db_file}')
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///" + os.path.join(BASE_DIR, DB_name)
"""

engine = create_engine('mysql+pymysql://guvi_user:1king#lanka@localhost:3306/guvi_test_orm', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def fstr_transcoder(fstring_dict: dict) -> str:
    return pd.DataFrame(fstring_dict, index=[0]).to_string()


def iso_duration_to_seconds(iso_duration: str) -> int:
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


def convert_to_datetime(date_string: str) -> datetime:
    # this is for use in Video_class
    date_string = date_string.rstrip('Z')
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')


class Channel_class(Base):
    __tablename__ = 'channels'
    __table_args__ = (Index('ix_id_name', 'channel_id', 'channel_name'),
                      {'extend_existing':True})
    # Index on both name and age
    channel_id = Column(String(255), unique=True, primary_key=True, comment="Unique identifier for the table")
    channel_name = Column(String(255), nullable=False, comment="Name of the channel")
    channel_type = Column(String(255), nullable=False, comment="Type of the channel")
    channel_views = Column(Integer, nullable=False, comment="Total number of views for the channel")
    channel_description = Column(Text, nullable=False, comment="Description of the channel")
    channel_status = Column(String(255), nullable=False, comment="Status of the channel")

    def __repr__(self):
        repr_pretty_ = {
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'channel_type': self.channel_type,
            'channel_views': self.channel_views,
            'channel_description': self.channel_description,
            'channel_status': self.channel_status
        }
        return fstr_transcoder(repr_pretty_)


class Playlist_class(Base):
    __tablename__ = 'playlists'
    __table_args__ = {'extend_existing':True}
    playlist_id = Column(String(255), nullable=False, index=True, primary_key=True,
                         comment='Unique identifier for the playlist')
    channel_id = Column(String(255), ForeignKey('channels.channel_id'),
                        comment='Foreign key referencing the channel table', )
    playlist_name = Column(String(255), comment='Name of the playlist')

    def __repr__(self):
        repr_pretty_ = {
            "playlist_id":self.playlist_id,
            "channel_id":self.channel_id,
            "playlist_name":self.playlist_name
        }
        return fstr_transcoder(repr_pretty_)


class Video_class(Base):
    __tablename__ = 'videos'
    __table_args__ = {'extend_existing':True}
    video_no = Column(Integer, primary_key=True,nullable=True, comment='video serial number')
    video_id = Column(String(255), nullable=False, primary_key=True, index=True, comment='Unique identifier for the video')
    playlist_ID = Column(String(255), ForeignKey('playlists.playlist_id'),
                         comment='Foreign key referencing the playlist table')
    video_name = Column(String(255), nullable=False, comment='Name of the video')
    video_description = Column(Text, nullable=True, comment='Description of the video')
    published_date = Column(DateTime, nullable=False, comment='Date and time when the video was published')
    view_count = Column(Integer, nullable=False, comment='Total number of views for the video')
    like_count = Column(Integer, nullable=False, comment='Total number of likes for the video')
    dislike_count = Column(Integer, nullable=False, comment='Total number of dislikes for the video')
    favorite_count = Column(Integer, nullable=False,comment='Total number of times the video has been marked as a favorite')
    comment_count = Column(Integer, nullable=False, comment='Total number of comments on the video')
    duration = Column(Integer, nullable=False, comment='Duration of the video in seconds')
    thumbnail = Column(String(255), nullable=True, comment='URL of the thumbnail for the video')
    caption_status = Column(String(255), nullable=True, comment='Status of the video caption')

    def __repr__(self):
        repr_pretty_ = {
            "video_id":self.video_id,
            "playlist_ID":self.playlist_ID,
            "video_name":self.video_name,
            "video_description":self.video_description,
            "published_date":self.published_date,
            "view_count":self.view_count,
            "like_count":self.like_count,
            "dislike_count":self.dislike_count,
            "favorite_count":self.favorite_count,
            "comment_count":self.comment_count,
            "duration":self.duration,
            "thumbnail":self.thumbnail,
            "caption_status":self.caption_status
        }
        return fstr_transcoder(repr_pretty_)


class Comment_class(Base):
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing':True}
    comment_no = Column(Integer,primary_key=True,comment='comments having same id, so separate colum of primary key.')
    comment_id = Column(String(255), nullable=False, index=True,
                        comment='Unique identifier for the comment')
    video_id = Column(String(255), ForeignKey('videos.video_id'), nullable=False, index=True,
                      comment='Foreign key referencing the video table')
    comment_text = Column(Text, nullable=False, comment='Text of the comment')
    comment_author = Column(String(255), nullable=False, comment='Name of the comment author')
    comment_published_date = Column(DateTime, nullable=False, comment='Date and time when the comment was published')

    def __repr__(self):
        repr_pretty_ = {
            "comment_id":self.comment_id,
            "video_id":self.video_id,
            "comment_text":self.comment_text,
            "comment_author":self.comment_author,
            "comment_published_date":self.comment_published_date
        }
        return fstr_transcoder(repr_pretty_)


# _____________________________________program start here_______________________________

Base.metadata.create_all(engine)
print("All tables created.")
extracted_dir = r"C:\Users\Elamparithi\PycharmProjects\Utube_DHW_5\extracted_data"

filepath = ['Behindwoods TV-20240825-115545.json',
            'GUVI-20240907-154356.json',
            'Sahi Siva-20240913-032253.json',
            'SHIVA SAI ENTERTAINMENT CHANNEL-20240824-190244.json']

for files in filepath:
    print(f"processing {files}...")
    full_path = os.path.join(extracted_dir, files)
    with open(full_path, 'r') as file:
        data = json.load(file)

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
    # print(channel_record)
    session.add(channel_record)
    session.commit()

    for playlist_data in channel_data["playlist"]:
        playlist_plid = playlist_data["playlist_ID"]
        playlist_record = Playlist_class(
            playlist_id=playlist_plid,
            channel_id=channel_chid,
            playlist_name=playlist_data["playlist_title"]
        )
        session.add(playlist_record)
        session.commit()
        for videos_dict in playlist_data["videos"]:
            video_data = videos_dict[next(iter(videos_dict))]
            video_vid = video_data['Video_Id']
            video_record = Video_class(
                video_id=video_vid,
                playlist_ID=playlist_plid,
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
                session.commit()
            else:
                pass    # print(f"Video with ID {video_record.video_id}<:=:>{video_record.video_name} already exists. Skipping insertion.")

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

