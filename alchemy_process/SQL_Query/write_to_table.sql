use	gemini_db;

insert into channels(roll_id, channel_id, channel_name, channel_type, channel_views, channel_description, channel_status)
values (2,'channel_id', 'channel_name', 'channel_type', 33245324, 'lkshdflakjshdlkjfhaslkdjhflaksjhdlf','Active');

insert into playlists(playlist_id, channel_id, playlist_name)
values('playlist_id','channel_id','playlist_name');

insert into videos(id, video_id, playlist_ID, channel_id, video_name, video_description, published_date, view_count, like_count, dislike_count, favorite_count, comment_count, duration, thumbnail, caption_status)
values (10,'video_id','playlist_id','channel_id','videoname','video description',now(),1232344,2383876,3245,23455,234, 23455,'alsdflakjhsd','alsdfhlaksdhf');

insert into comments(id, comment_id, video_id, comment_text, comment_author, comment_published_date)
values (1,'comment_id','video_id','comment_text','comment_author',now());

