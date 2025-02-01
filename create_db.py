#!Utube_DHW_5\.venv\Scripts\python

"""
create_db.py for creating Schema and Tables.
"""

from sqlalchemy import Column, String, Integer, BigInteger, Text, DateTime, Float
from sqlalchemy import ForeignKey, create_engine, exc
from sqlalchemy.orm import relationship, declarative_base
from config_and_auxiliary import locate_log
from sqlalchemy.schema import CreateSchema
from dotenv import load_dotenv
import logging
import os

"""
    Author: Elamparithi 
    Last Update: 17 nov 24
    Fully functional as of last update.
"""

log_file = locate_log('app', 'create_db.log')
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(log_file, encoding='utf-8')])
logger = logging.getLogger('create_db')

Base = declarative_base()


class Channel_class(Base):
    __tablename__ = 'channels'
    channel_id = Column(String(255), unique=True, primary_key=True, comment="Unique identifier for the table")
    channel_name = Column(String(255), nullable=False, comment="Name of the channel")
    channel_type = Column(String(255), nullable=False, comment="Type of the channel")
    channel_views = Column(BigInteger, nullable=False, comment="Total number of views for the channel")
    channel_description = Column(Text, nullable=False, comment="Description of the channel")
    channel_status = Column(String(255), nullable=False, comment="Status of the channel")

    playlists = relationship("Playlist_class", back_populates="channel_relation", cascade="all, delete-orphan")
    videos = relationship("Video_class", back_populates="channel_relation", cascade="all, delete-orphan")


class Playlist_class(Base):
    __tablename__ = 'playlists'
    playlist_id = Column(String(255), nullable=False, primary_key=True, comment="Unique identifier for the playlist")
    channel_id = Column(String(255), ForeignKey("channels.channel_id"), nullable=False, comment="Channel reference")
    playlist_name = Column(String(255), nullable=False, comment="Name of the playlist")

    channel_relation = relationship("Channel_class", back_populates="playlists")
    videos = relationship("Video_class", back_populates="playlist_relation", cascade="all, delete-orphan")


class Video_class(Base):
    __tablename__ = 'videos'
    video_id = Column(String(255), nullable=False, primary_key=True, comment="Unique identifier for the video")
    playlist_id = Column(String(255), ForeignKey('playlists.playlist_id'), comment="Playlist reference")
    channel_id = Column(String(255), ForeignKey("channels.channel_id"), nullable=False, comment="Channel reference")
    video_name = Column(String(255), nullable=False, comment="Name of the video")
    video_description = Column(Text, comment="Description of the video")
    published_date = Column(DateTime, nullable=False, comment="Date and time when the video was published")
    view_count = Column(Integer, nullable=False, comment="Total number of views for the video")
    like_count = Column(Integer, nullable=False, comment="Total number of likes for the video")
    dislike_count = Column(Integer, nullable=False, comment="Total number of dislikes for the video")
    favorite_count = Column(Integer, nullable=False,
                            comment="Total number of times the video has been marked as a favorite")
    comment_count = Column(Integer, nullable=False, comment="Total number of comments on the video")
    duration = Column(Integer, nullable=False, comment="Duration of the video in seconds")
    thumbnail = Column(String(255), comment="URL of the thumbnail for the video")
    caption_status = Column(String(255), comment="Status of the video caption")

    channel_relation = relationship("Channel_class", back_populates="videos")
    playlist_relation = relationship("Playlist_class", back_populates="videos")
    comments = relationship("Comment_class", back_populates="video_relation", cascade="all, delete-orphan")


class Comment_class(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Primary key ID for unique identification")
    comment_id = Column(String(255), nullable=False, comment="Unique identifier for the comment")
    video_id = Column(String(255), ForeignKey('videos.video_id'), nullable=False, comment="Video reference")
    comment_text = Column(Text, nullable=False, comment="Text of the comment")
    comment_author = Column(String(255), nullable=False, comment="Name of the comment author")
    comment_published_date = Column(DateTime, nullable=False, comment="Date and time when the comment was published")
    sentiment = Column(Float, comment="sentiment value for given comment comments.")
    sentiment_type = Column(String(20), comment="sentiment type for given comments.")

    video_relation = relationship("Video_class", back_populates="comments")


def separate_connection_string(conn_string: str):
    """
    Function to separate connection URL and connection schema.
    Connection string that contains all server creds and schema name
    i.e.mysql+pymysql://username:password@localhost:3306/dbname

    @param conn_string: connection URL as string
    @return conn_url (str): URL without dbname
    @return conn_schema (str): database name (schema)
    """
    last_slash_index = conn_string.rfind('/')
    if last_slash_index != -1:
        conn_url = conn_string[:last_slash_index]  # Everything before the last '/'
        conn_schema = conn_string[last_slash_index + 1:]  # Everything after the last '/'
    else:
        conn_url = conn_string  # No '/' found
        conn_schema = ''
    logger.info('connection string separated')
    return conn_url, conn_schema


# Create Database Function
def check_create_database(connection_string: str):
    """
    Check for the schema in the string is already exists.
    if not create it.
    @param connection_string: connection string with schema
    @return engine_tabled: engine with tables created
    """
    connection_URL, connection_Schema = separate_connection_string(connection_string)
    logger.info(f"Connection URL: {connection_URL}")
    logger.info(f"Connection Schema: {connection_Schema}")
    engine_local = create_engine(connection_URL, echo=False)
    with engine_local.connect() as conn:
        try:
            conn.execute(CreateSchema(connection_Schema))
            logger.info(f"Schema '{connection_Schema}' created successfully.")
        except exc.ProgrammingError:
            logger.info(f"Schema '{connection_Schema}' already exists, skipping creation.")
        finally:
            conn.close()
            engine_local.dispose()
            logger.info("Connection closed.")
    # create Schema. If above try run well. no problem running below.
    engine_tabled = create_engine(connection_string, echo=False)
    Base.metadata.create_all(engine_tabled, checkfirst=True)
    logger.info("all Tables created.")
    return engine_tabled


if __name__ == '__main__':
    load_dotenv('.secrets')  # another local secret instead of st.secrets just for running it offline.
    db_precon = os.getenv('pre_conn')
    DB_name = os.getenv('DB_NAME')  # "youtube_dhw"

    engine = check_create_database(f'{db_precon}{DB_name}')
    engine.dispose()
    print("Program completed.")
