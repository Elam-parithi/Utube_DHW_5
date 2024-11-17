# youtube_extractor.py

# This module only extract the YouTube data and present it as GUVI formated json file.
# Additionally, it has a function to check api keys.

import requests
from re import compile
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

# TODO: update GUVI formater check with doc for verification.

logger = logging.getLogger('Youtube_Extractor')


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
        try:
            self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
            self.is_connected = True
        except HttpError as e:
            self.is_connected = False
            logger.warning(f"API key validation failed. Error:{e}")

    @staticmethod
    def process_urls(url_list: list) -> str:
        """
        For using in Channel Type. Mentioned as URLs Need for channel video categories. keep the last category and
        return it as comma(,) separated string.
        @param url_list: list of URL
        @return result: comma(,) separated string.
        """
        prefix = 'https://en.wikipedia.org/wiki/'
        processed_parts = [url.replace(prefix, '') for url in url_list]
        result = ', '.join(processed_parts)
        return result

    def get_channel_id(self, channel_name: str):
        """
        Extract channel ID for the given channel name. Returns the first possible result only.
        @param channel_name: channel name with string.
        @return: matching channel ID or None
        """
        request = self.youtube.search().list(part='snippet', q=channel_name, type='channel', maxResults=1)
        response = request.execute()
        if response['items']:
            return response['items'][0]['snippet']['channelId']
        else:
            return None

    def get_channel_info(self, channel_id: str):
        """
        Information about channel are provided here.
        @param channel_id:
        @return: dict or None
        """
        request = self.youtube.channels().list(
            part='snippet,statistics,contentDetails,status,topicDetails',
            id=channel_id)
        response = request.execute()
        return response['items'][0] if response['items'] else None

    def get_playlists_from_channel(self, channel_id: str) -> list:
        """
        Returns all the playlist info from the channel. except uploads.
        @param channel_id: channel ID string
        @return list: empty or dictionary of info on playlist in that channel.
        """
        playlist_response = []
        request = self.youtube.playlists().list(part='snippet', channelId=channel_id, maxResults=50)
        try:
            response = request.execute()
            if response is None or response is {}:
                return playlist_response
            playlist_response.extend(response['items'])
            while 'nextPageToken' in response:
                request = self.youtube.playlists().list(part='snippet', channelId=channel_id, maxResults=50,
                                                        pageToken=response['nextPageToken'])
                response = request.execute()
                playlist_response.extend(response['items'])
        finally:
            return playlist_response

    def get_videos_from_playlist(self, playlist_id: str) -> list:
        """
        returns all the list of videos in the playlist.
        @param playlist_id: YouTube channel's playlist ID
        @return: empty list or list of videos.
        """
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
            logger.warning(f"Error fetching videos from playlist {playlist_id}:{e}")
            return []

    def get_video_info(self, video_id: str):
        """
        get video info using video ID
        @param video_id: YouTube Video ID
        @return: dictionary of items or None
        """
        request = self.youtube.videos().list(
            part='statistics,snippet,contentDetails',
            id=video_id
        )
        response = request.execute()
        return response['items'][0] if response['items'] else None

    def check_input_type(self, check_text: str) -> bool:
        """
        Check weather the given string is in channel id format.
        @param check_text: the string to be tested.
        @return: True if match
        """
        return bool(self.channel_id_pattern.match(check_text))

    def get_video_comments(self, video_id: str):
        """
        Get comments using the given video ID and return the dictionary or None
        @param video_id: YouTube Video ID
        @return: empty list or none or list of video comments as dictionary.
        """
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
                logger.info(f"Comments are disabled for video ID:{video_id}")
                return None
            else:
                logger.warning(f"Error fetching comments for video {video_id}:{e}")
                return []

    def __comment_dict(self, video_id: str) -> dict:
        """
        creates nested dictionary of comments for a video dict.
        @param video_id: YouTube video ID
        @return: empty dictionary or nested dictionary of comments.
        """
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

    def __video_dict(self, playlist_ids: str):
        """
        creates a nested dictionary of video info and comments.
        @param playlist_ids: YouTube channel's playlist ID
        @return: videos_list, vlt
        """
        vlt = self.get_videos_from_playlist(playlist_ids)
        videos_list = []
        for video_counter, video_ID in enumerate(vlt, start=1):
            vlt_info = self.get_video_info(video_ID)
            if vlt_info is None:
                logger.debug(f"video info of {video_ID} is :=> {vlt_info}")
                return videos_list, vlt
                # if that video is deleted/blocked/censored videos_list is empty list and vlt is None
                # Again use channel name 'GUVI' for testing this one.
            Vid_comment_count = vlt_info['statistics'].get('commentCount')
            if Vid_comment_count == '0':
                # For testing use GUVI, It has blocked comments in its videos.
                logger.info(f'There is no comments in this video{video_ID} = {vlt_info['snippet']['title']}, '
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
                        "Caption_Status":'Available' if vlt_info['contentDetails'][
                                                            'caption'] == 'true' else "Unavailable",
                        "Comments":comment_dict
                    }
                }
                videos_list.append(video_dict)
        return videos_list, vlt

    def get_playlist_info(self, playlist_ids: str) -> list:
        """
        playlist info for give id. only for use with uploads playlist. works with other playlist ids too.
        @param playlist_ids: YouTube Playlist ID
        @return: list with dictionary in it.
        """
        request = self.youtube.playlists().list(part='snippet', id=playlist_ids)
        response = request.execute()
        item = response['items'][0]
        videos_list, vlt = self.__video_dict(item['id'])
        uploads_plt_dict = {
            "playlist_title":item['snippet']['title'],
            "playlist_ID":item['id'],
            "playlist_description":item['snippet']['description'],
            "playlist_videos":vlt,
            "playlist_video_count":len(vlt),
            "videos":videos_list
        }
        return [uploads_plt_dict]

    def __playlist_dict(self, channel_id: str, uploads_id: str) -> list:
        """
        Returns a list with dictionary of items in list including uploads folder.
        @param channel_id: YouTube channel ID
        @param uploads_id: Uploads playlist id for the same channel.
        @return: list of dictionaries.
        """
        plt_info = self.get_playlists_from_channel(channel_id)
        play_list = self.get_playlist_info(uploads_id)
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

    def guvi_format(self, channel_id: str) -> dict:
        """
        guvi formatted output.
        @param channel_id: YouTube channel ID
        @return: nested dictionary
        """
        channel_infos = self.get_channel_info(channel_id)
        if not channel_infos:
            return {}
        upload_playlistID = channel_infos["contentDetails"]["relatedPlaylists"]["uploads"]
        play_list = self.__playlist_dict(channel_id, upload_playlistID)
        guvi_format_data: dict = {
            channel_infos['snippet']['title']:{
                "Channel_Name":channel_infos['snippet']['title'],
                "Channel_Id":channel_infos['id'],
                "Channel_type":self.process_urls(channel_infos['topicDetails']['topicCategories']),
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
    cid = yt.get_channel_id(channel_name='madras foodie')
    dt = yt.guvi_format(cid)
    import json

    file_path = r'extracted_data/guvi4.json'
    with open(file_path, 'w') as file:
        json.dump(dt, file, indent=4)  # The indent argument is optional, it just makes the output more readable
    print("Program was completed.")
