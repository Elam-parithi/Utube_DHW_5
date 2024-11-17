# youtube_extractor.py

# This module only extract the YouTube data and present it as GUVI formated json file.
# Additionally, it has a function to check api keys.

import requests
from re import compile
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# TODO: update GUVI formater check with doc for verification.
# Fixme: upload playlist name was getting conflict with playlist[0] resolve it sooner.


def check_api_key(function_api_key):
    try:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=id&mine=true&key={function_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except HttpError as e:
        raise ConnectionError(e)


class YouTubeDataExtractor:
    def __init__(self, youtube_api_key):
        self.channel_id_pattern = compile(r'^UC[a-zA-Z0-9-_]{22}$')
        self.youtube = None
        self.is_connected = None
        self.default_upload_playlistID = None
        try:
            self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
            self.is_connected = True
        except HttpError as e:
            self.is_connected = False
            print(f"API key validation failed. Error:{e}")

    def get_channel_id(self, channel_name):
        request = self.youtube.search().list(part='snippet', q=channel_name, type='channel', maxResults=1)
        response = request.execute()
        if response['items']:
            return response['items'][0]['snippet']['channelId']
        else:
            return None

    def get_channel_info(self, channel_id):
        request = self.youtube.channels().list(
            part='snippet,statistics,contentDetails,status',
            id=channel_id
        )
        response = request.execute()
        return response['items'][0] if response['items'] else None

    def get_playlists_from_channel(self, channel_id):
        request = self.youtube.playlists().list(
            part='snippet,contentDetails',
            channelId=channel_id,
            maxResults=50
        )
        response = request.execute()
        return response['items'] if response['items'] else []

    def get_videos_from_playlist(self, playlist_id):
        try:
            videos = []
            request = self.youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50
            )
            while request:
                response = request.execute()
                videos.extend(response['items'])
                request = self.youtube.playlistItems().list_next(request, response)
            return [video['contentDetails']['videoId'] for video in videos]
        except HttpError as e:
            print(f"Error fetching videos from playlist {playlist_id}:{e}")
            return []

    def get_video_info(self, video_id):
        request = self.youtube.videos().list(
            part='statistics,snippet,contentDetails',
            id=video_id
        )
        response = request.execute()
        return response['items'][0] if response['items'] else None

    def check_input_type(self, check_text):
        return bool(self.channel_id_pattern.match(check_text))

    def get_video_comments(self, video_id):
        comments = []
        request = self.youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        )
        try:
            response = request.execute()
            comments.extend(response['items'])
            while 'nextPageToken' in response:
                request = self.youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=100,
                    pageToken=response['nextPageToken']
                )
                response = request.execute()
                comments.extend(response['items'])
            return comments
        except HttpError as e:
            if e.resp.status == 403 and e.error_details[0]['reason'] == 'commentsDisabled':
                print(f"Comments are disabled for video ID:{video_id}")
                return None
            else:
                print(f"Error fetching comments for video {video_id}:{e}")
                return []

    def __comment_dict(self, video_id):
        comment_info_response = self.get_video_comments(video_id)
        comment_data_dict = {}
        for cdx, comment_items in enumerate(comment_info_response or [], start=1):
            comment_data = {
                f"Comment_Id_{cdx}":{
                    "Comment_Id":comment_items['id'],
                    "Comment_Text":comment_items['snippet']['topLevelComment']['snippet']['textOriginal'],
                    "Comment_Author":comment_items['snippet']['topLevelComment']['snippet'][
                        'authorDisplayName'],
                    "Comment_PublishedAt":comment_items['snippet']['topLevelComment']['snippet']['publishedAt']
                }
            }
            comment_data_dict.update(comment_data)
        return comment_data_dict

    def __video_dict(self, playlist_ids):
        vlt = self.get_videos_from_playlist(playlist_ids)
        videos_list = []
        for video_counter, video_ID in enumerate(vlt, start=1):
            vlt_info = self.get_video_info(video_ID)
            if vlt_info is None:
                print(f"vlt info of {video_ID} is :=> {vlt_info}")
                return videos_list, vlt  # if that video is deleted videos_list is empty list and vlt is None
                # Again use channel name 'GUVI' for testing this one.
            Vid_comment_count = vlt_info['statistics'].get('commentCount')
            if Vid_comment_count == '0':
                # For testing use GUVI, It has blocked comments in its videos.
                print(f'There is no comments in this video{video_ID} = {vlt_info['snippet']['title']}, '
                      f'comment count {Vid_comment_count}')
                comment_dict: dict = {}
            else:
                comment_dict = self.__comment_dict(video_ID)
            if vlt_info:
                video_dict = {
                    f"Video_Id_{video_counter}":{
                        "Video_Id":vlt_info['id'],
                        "Video_Name":vlt_info['snippet']['title'],
                        "Video_Description":vlt_info['snippet']['description'],
                        "Tags":vlt_info['snippet'].get('tags', []),
                        "PublishedAt":vlt_info['snippet']['publishedAt'],
                        "View_Count":vlt_info['statistics'].get('viewCount', 0),
                        "Like_Count":vlt_info['statistics'].get('likeCount', 0),
                        "Dislike_Count":vlt_info['statistics'].get('dislikeCount', 0),
                        "Favorite_Count":vlt_info['statistics'].get('favoriteCount', 0),
                        "Comment_Count":vlt_info['statistics'].get('commentCount', 0),
                        "Duration":vlt_info['contentDetails']['duration'],
                        "Thumbnail":vlt_info['snippet']['thumbnails']['default']['url'],
                        "Caption_Status":'Available' if vlt_info['contentDetails']['caption'] == 'true' else "Unavailable",
                        "Comments":comment_dict
                    }
                }
                videos_list.append(video_dict)
        return videos_list, vlt

    def __playlist_dict(self, channel_id):
        plt_info = self.get_playlists_from_channel(channel_id)
        play_list = [self.default_upload_playlistID]
        for i, item in enumerate(plt_info):
            videos_list, vlt = self.__video_dict(item['id'])
            plt_dict = {
                "playlist_title":item['snippet']['title'],
                "playlist_ID":item['id'],
                "playlist_description":item['snippet']['description'],
                "playlist_videos":vlt,
                "playlist_video_count":len(vlt),
                "videos":videos_list
            }
            play_list.append(plt_dict)
        return play_list

    def guvi_format(self, channel_id):
        channel_infos = self.get_channel_info(channel_id)
        if not channel_infos:
            return {}
        self.default_upload_playlistID = channel_infos["contentDetails"]["relatedPlaylists"]["uploads"]
        play_list = self.__playlist_dict(channel_id)
        guvi_format_data: dict = {
            channel_infos['snippet']['title']:{
                "Channel_Name":channel_infos['snippet']['title'],
                "Channel_Id":channel_infos['id'],
                # Fixme: Fix channel type in youtube_extractor.py, SQL create-db and write-db are good.
                # "Channel_type":
                "Subscription_Count":channel_infos['statistics'].get('subscriberCount', 0),
                "Channel_Views":channel_infos['statistics'].get('viewCount', 0),
                "Channel_Description":channel_infos['snippet']['description'],
                "Channel_Status":channel_infos['status'],
                "playlist":play_list
            }
        }
        return guvi_format_data


if __name__ == "__main__":
    yt = YouTubeDataExtractor('AIzaSyCS-NnHQKO65o2RYWejYSbE_PFSWucU1z0')
    cid = yt.get_channel_id(channel_name='guvi')
    dt = yt.guvi_format(cid)
    import json
    file_path = r'extracted_data/guvi3.json'
    with open(file_path, 'w') as file:
        json.dump(dt, file, indent=4)  # The indent argument is optional, it just makes the output more readable
    print("Program was completed.")

