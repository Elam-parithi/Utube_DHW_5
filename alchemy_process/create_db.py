#!Utube_DHW_5\.venv\Scripts\python
import pandas as pd
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, ForeignKey, exc
from sqlalchemy import Column, String, Integer, BigInteger, Text, DateTime, Index

"""
Author: Elamparithi
Last_update: 04 Nov 24 06:54pm
Note: This code is working without problems.
"""

schema_name = 'guvi_orm3'
connection_string = f'mysql+pymysql://guvi_user:password@localhost:3306/{schema_name}'
Base = declarative_base()


def fstr_transcoder(fstring_dict: dict) -> str:
    return pd.DataFrame(fstring_dict, index=[0]).to_string()


class Channel_class(Base):
    __tablename__ = 'channels'
    __table_args__ = (Index('ix_id_name', 'channel_id', 'channel_name'), {'extend_existing':True})
    channel_id = Column(String(255), unique=True, primary_key=True, comment="Unique identifier for the table")
    channel_name = Column(String(255), nullable=False, comment="Name of the channel")
    channel_type = Column(String(255), nullable=False, comment="Type of the channel")
    channel_views = Column(BigInteger, nullable=False, comment="Total number of views for the channel")
    channel_description = Column(Text, nullable=False, comment="Description of the channel")
    channel_status = Column(String(255), nullable=False, comment="Status of the channel")

    def __repr__(self):
        repr_pretty_ = {
            'channel_id':self.channel_id,
            'channel_name':self.channel_name,
            'channel_type':self.channel_type,
            'channel_views':self.channel_views,
            'channel_description':self.channel_description,
            'channel_status':self.channel_status
        }
        return fstr_transcoder(repr_pretty_)


class Playlist_class(Base):
    __tablename__ = 'playlists'
    __table_args__ = {'extend_existing':True}
    playlist_id = Column(String(255), nullable=False, index=True,
                         primary_key=True, comment='Unique identifier for the playlist')
    channel_id = Column(String(255), ForeignKey('channels.channel_id'),
                        comment='Foreign key referencing the channel table')
    playlist_name = Column(String(255), comment='Name of the playlist')

    def __repr__(self):
        repr_pretty_ = {
            "playlist_id":self.playlist_id,
            "channel_id":self.channel_id,
            "playlist_name":self.playlist_name
        }
        return fstr_transcoder(repr_pretty_)


# Class table with __repr__
class Video_class(Base):
    __tablename__ = 'videos'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, autoincrement=True, comment='Primary key ID for unique identification')
    video_id = Column(String(255), nullable=False, index=True, primary_key=True,
                      comment="Unique identifier for the video")
    playlist_ID = Column(String(255), ForeignKey('playlists.playlist_id'),
                         comment='Foreign key referencing the playlist table')
    video_name = Column(String(255), nullable=False, comment='Name of the video')
    video_description = Column(Text, comment='Description of the video')
    published_date = Column(DateTime, nullable=False, comment='Date and time when the video was published')
    view_count = Column(Integer, nullable=False, comment='Total number of views for the video')
    like_count = Column(Integer, nullable=False, comment='Total number of likes for the video')
    dislike_count = Column(Integer, nullable=False, comment='Total number of dislikes for the video')
    favorite_count = Column(Integer, nullable=False,
                            comment='Total number of times the video has been marked as a favorite')
    comment_count = Column(Integer, nullable=False, comment='Total number of comments on the video')
    duration = Column(Integer, nullable=False, comment='Duration of the video in seconds')
    thumbnail = Column(String(255), comment='URL of the thumbnail for the video')
    caption_status = Column(String(255), comment='Status of the video caption')

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


# Class table with __repr__
class Comment_class(Base):
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='Primary key ID for unique identification')
    comment_id = Column(String(255), nullable=False, comment='Unique identifier for the comment')
    video_id = Column(String(255), index=True, comment='Foreign key referencing the video table')
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


def separate_connection_string(conn_string: str):
    """
    Function to separate connection URL and connection schema
    """
    last_slash_index = conn_string.rfind('/')
    if last_slash_index != -1:
        conn_url = conn_string[:last_slash_index]  # Everything before the last '/'
        conn_schema = conn_string[last_slash_index + 1:]  # Everything after the last '/'
    else:
        conn_url = conn_string  # No '/' found
        conn_schema = ''
    return conn_url, conn_schema


connection_URL, connection_Schema = separate_connection_string(connection_string)
print(f"Connection URL: {connection_URL}")
print(f"Connection Schema: {connection_Schema}")

engine = create_engine(connection_URL, echo=False)
with engine.connect() as conn:
    try:
        conn.execute(CreateSchema(schema_name))
        print(f"Schema '{schema_name}' created successfully.")
    except exc.ProgrammingError:
        print(f"Schema '{schema_name}' already exists, skipping creation.")
    finally:
        conn.close()
        print("Connection closed.")

# create Schema. If above try run well. no problem running below.
engine = create_engine(connection_string, echo=False)
Base.metadata.create_all(engine)
print("all Tables created.")
