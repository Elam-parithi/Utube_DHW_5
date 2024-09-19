import json
import streamlit
import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer, Text, Table, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(255), unique=True, nullable=False)
    channel_name = Column(String(255), nullable=False)
    subscription_count = Column(Integer, nullable=False)
    channel_views = Column(Integer, nullable=False)
    channel_description = Column(Text, nullable=True)
    playlist_id = Column(String(255), nullable=True)

    videos = relationship("Video", back_populates="channel")


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String(255), unique=True, nullable=False)
    video_name = Column(String(255), nullable=False)
    video_description = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    published_at = Column(String(255), nullable=False)
    view_count = Column(Integer, nullable=False)
    like_count = Column(Integer, nullable=False)
    dislike_count = Column(Integer, nullable=False)
    favorite_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)
    duration = Column(String(255), nullable=False)
    thumbnail = Column(String(255), nullable=True)
    caption_status = Column(String(255), nullable=True)
    channel_id = Column(Integer, ForeignKey('channels.id'))

    comments = relationship("Comment", back_populates="video")
    channel = relationship("Channel", back_populates="videos")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment_id = Column(String(255), unique=True, nullable=False)
    comment_text = Column(Text, nullable=False)
    comment_author = Column(String(255), nullable=False)
    comment_published_at = Column(String(255), nullable=False)
    video_id = Column(Integer, ForeignKey('videos.id'))

    video = relationship("Video", back_populates="comments")

