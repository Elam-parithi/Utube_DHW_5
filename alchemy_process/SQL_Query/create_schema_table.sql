drop schema if exists gemini_db;
create database if not exists gemini_db;
use	gemini_db;

CREATE TABLE if not exists channels (
	roll_id int primary key comment 'roll id for primary key',
	channel_id VARCHAR(255) unique UNIQUE not NULL  COMMENT 'Unique identifier for the table', 
	channel_name VARCHAR(255) COMMENT 'Name of the channel', 
	channel_type VARCHAR(255) COMMENT 'Type of the channel', 
	channel_views BIGINT COMMENT 'Total number of views for the channel', 
	channel_description TEXT COMMENT 'Description of the channel', 
	channel_status VARCHAR(255) COMMENT 'Status of the channel'
);

CREATE TABLE if not exists playlists (
	playlist_id VARCHAR(255) primary key NOT NULL COMMENT 'Unique identifier for the playlist', 
	channel_id VARCHAR(255) COMMENT ' channel table', 
	playlist_name VARCHAR(255) COMMENT 'Name of the playlist',
	FOREIGN KEY(channel_id) REFERENCES channels (channel_id)
);

CREATE TABLE if not exists videos (
	id INTEGER primary key unique auto_increment comment 'Primary key ID for unique identification', 
	video_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the video', 
	playlist_ID VARCHAR(255) COMMENT 'Foreign key referencing the playlist table', 
	channel_id VARCHAR(255) COMMENT ' channel table', 
	video_name VARCHAR(255) NOT NULL COMMENT 'Name of the video', 
	video_description TEXT COMMENT 'Description of the video', 
	published_date DATETIME NOT NULL COMMENT 'Date and time when the video was published', 
	view_count INTEGER NOT NULL COMMENT 'Total number of views for the video', 
	like_count INTEGER NOT NULL COMMENT 'Total number of likes for the video', 
	dislike_count INTEGER NOT NULL COMMENT 'Total number of dislikes for the video', 
	favorite_count INTEGER NOT NULL COMMENT 'Total number of times the video has been marked as a favorite', 
	comment_count INTEGER NOT NULL COMMENT 'Total number of comments on the video', 
	duration INTEGER NOT NULL COMMENT 'Duration of the video in seconds', 
	thumbnail VARCHAR(255) COMMENT 'URL of the thumbnail for the video', 
	caption_status VARCHAR(255) COMMENT 'Status of the video caption', 

	FOREIGN KEY(playlist_ID) REFERENCES playlists (playlist_id), 
	FOREIGN KEY(channel_id) REFERENCES channels (channel_id)
);

CREATE TABLE if not exists comments (
	id INTEGER NOT NULL COMMENT 'Primary key ID for unique identification' AUTO_INCREMENT primary key, 
	comment_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the comment', 
	video_id VARCHAR(255) COMMENT 'Foreign key referencing the video table', 
	comment_text TEXT NOT NULL COMMENT 'Text of the comment', 
	comment_author VARCHAR(255) NOT NULL COMMENT 'Name of the comment author', 
	comment_published_date DATETIME NOT NULL COMMENT 'Date and time when the comment was published'
);

