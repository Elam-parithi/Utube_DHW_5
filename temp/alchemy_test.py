from sqlalchemy import create_engine, Column, String, Integer, Text, ForeignKey  # Table, MetaData,
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError

import json
import os

engine = create_engine("sqlite:///Database_storage/Utube_DHW-20-jupyter.db")
connection = engine.connect()
Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channels'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(255), unique=True, nullable=False)
    channel_name = Column(String(255), nullable=False)
    subscription_count = Column(Integer, nullable=False)
    channel_views = Column(Integer, nullable=False)
    channel_description = Column(Text, nullable=True)

    # Relationship to Playlists
    playlists = relationship('Playlists', back_populates='channel')


class Playlists(Base):
    __tablename__ = 'playlists'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    playlist_title = Column(String(255), nullable=False)
    playlist_ID = Column(String(255), unique=True, nullable=False)
    playlist_description = Column(Text, nullable=True)
    playlist_video_count = Column(Integer, nullable=False)
    channel_id = Column(String(255), ForeignKey('channels.channel_id'))

    # Relationship to Channel
    channel = relationship('Channel', back_populates='playlists')
    # Relationship to Videos
    videos = relationship('Video', back_populates='playlist')


class Video(Base):
    __tablename__ = 'videos'
    __table_args__ = {'extend_existing':True}
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
    playlist_ID = Column(String(255), ForeignKey('playlists.playlist_ID'))

    # Relationship to Playlist
    playlist = relationship('Playlist', back_populates='videos')
    # Relationship to Comments
    comments = relationship('Comment', back_populates='video')


class Comment(Base):
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment_id = Column(String(255), unique=True, nullable=False)
    comment_text = Column(Text, nullable=False)
    comment_author = Column(String(255), nullable=False)
    comment_published_at = Column(String(255), nullable=False)
    video_id = Column(Integer, ForeignKey('videos.video_id'))

    # Relationship to Video
    video = relationship('Video', back_populates='comments')


Base.metadata.create_all(engine)
print("All tables created.")
Session = sessionmaker(bind=engine, autoflush=False)
session = Session()


def _rollback(error_name: str):
    session.rollback()
    print(f"Failed to insert due to {error_name}.")


def channel_write(channel_datum):
    print(f"Channel write called.")
    """if session.query(Channel).filter_by(channel_id=channel_datum["Channel_Id"]).first():
        print(f"Channel with ID {channel_datum['Channel_Id']} already exists. Skipping insertion.")
        # _rollback(f"Channel with ID {channel_datum['Channel_Id']} already exists. Skipping insertion.")
        session.rollback()
        print("_rollback completed")
        #return"""
    # If not exists, insert the new channel
    print("channel try-except statement.")
    try:
        print("channel try running")
        channel = Channel(
            channel_id=channel_datum["Channel_Id"],
            channel_name=channel_datum["Channel_Name"],
            subscription_count=channel_datum["Subscription_Count"],
            channel_views=channel_datum["Channel_Views"],
            channel_description=channel_datum["Channel_Description"])
        print("Channel loaded")
        session.add(channel)
        session.commit()
        print("Channel commited")
        # print(f"Channel {channel_datum['Channel_Name']} inserted successfully.")
    except Exception as channel_exception:
        print(channel_exception)
    finally:
        print("channel write completed.")
        return


def playlists_write(playlist_datum, chid):
    match_it = playlist_datum["playlist_ID"]
    if session.query(Playlists).filter_by(playlist_ID=match_it).first():
        return
    try:
        play = Playlists(
            playlist_title=playlist_datum["playlist_title"],
            playlist_ID=playlist_datum["playlist_ID"],
            playlist_description=playlist_datum["playlist_description"],
            playlist_video_count=playlist_datum["playlist_video_count"],
            channel_id=chid
        )
        session.add(play)
        session.commit()
    except IntegrityError:
        _rollback("Playlists-IntegrityError")
    finally:
        return


def video_write(video_datum, plid):
    match_it = video_datum['Video_Id']
    if session.query(Video).filter_by(video_id=match_it).first():
        # _rollback(f"Video with ID {match_it} already exists. Skipping insertion.")
        return
    try:
        # Convert the tags list to a JSON string. tags here is a list. passing to sql was raising interface error.
        video_tags = json.dumps(video_datum.get("Tags", []))  # video_datum["Tags"]
        vid = Video(
            video_id=video_datum['Video_Id'],
            video_name=video_datum["Video_Name"],
            video_description=video_datum["Video_Description"],
            tags=video_tags,
            published_at=video_datum["PublishedAt"],
            view_count=video_datum["View_Count"],
            like_count=video_datum["Like_Count"],
            dislike_count=video_datum["Dislike_Count"],
            favorite_count=video_datum["Favorite_Count"],
            comment_count=video_datum["Comment_Count"],
            duration=video_datum["Duration"],
            thumbnail=video_datum["Thumbnail"],
            caption_status=video_datum["Caption_Status"],
            playlist_ID=plid)
        session.add(vid)
        session.commit()
        # print(f"{video_datum['Video_Name']} - Video inserted successfully.")
    except IntegrityError:
        _rollback("Video-IntegrityError")
        return


def comment_write(comment_datum, vid):
    match_it = comment_datum['Comment_Id']
    if session.query(Comment).filter_by(comment_id=match_it).first():
        # _rollback(f"Comment with ID {match_it} already exists. Skipping insertion.")
        return
    try:
        cmt = Comment(
            comment_id=match_it,
            comment_text=comment_datum['Comment_Text'],
            comment_author=comment_datum['Comment_Author'],
            comment_published_at=comment_datum['Comment_PublishedAt'],
            video_id=vid)

        session.add(cmt)
        session.commit()
        # print(f"Comment {match_it} inserted successfully.")
    except IntegrityError:
        _rollback("Comment-IntegrityError")
        return


extracted_dir = r"/extracted_data"

filepath = ['Behindwoods TV-20240825-115545.json', 'GUVI-20240907-154356.json',
            'Sahi Siva-20240913-032253.json',
            'SHIVA SAI ENTERTAINMENT CHANNEL-20240824-190244.json']

for files in filepath:
    print(f"processing {files}...")
    full_path = os.path.join(extracted_dir, files)
    with open(full_path, 'r') as file:
        data = json.load(file)

    channel_data = data[next(iter(data))]
    channel_chid = channel_data["Channel_Id"]
    channel_cnme = channel_data['Channel_Name']
    print(f"{channel_cnme}:{channel_chid}")
    chanel_write_pass = True
    try:
        channel_write(channel_data)
    except Exception as e:
        chanel_write_pass = False
    finally:
        print(f"channel_write {chanel_write_pass}")

    for playlist_data in channel_data["playlist"]:
        try:
            playlists_write(playlist_data, chid=channel_chid)
        except InvalidRequestError:
            print("playlists_write-InvalidRequestError")

        playlist_plid = playlist_data["playlist_ID"]
        for videos_dict in playlist_data["videos"]:
            video_data = videos_dict[next(iter(videos_dict))]
            try:
                video_write(video_data, plid=playlist_plid)
            except Exception as e:
                pass
            video_vid = video_data['Video_Id']

            for comment_dict in video_data["Comments"]:
                comment_write(comment_dict, video_vid)
