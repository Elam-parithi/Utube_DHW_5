def guvi_format(self, channel_id):
    channel_infos = self.get_channel_info(channel_id)
    if not channel_infos:
        return {}

    plt_info = self.get_playlists_from_channel(channel_id)
    play_list = []
    for i, item in enumerate(plt_info):
        vlt = self.get_videos_from_playlist(item['id'])
        videos_list = []
        for video_counter, video_ID in enumerate(vlt, start=1):
            vlt_info = self.get_video_info(video_ID)
            comment_info_response = self.get_video_comments(video_ID)
            comment_data_dict = {}
            for cdx, comment_items in enumerate(comment_info_response, start=1):
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
                        "Comments":comment_data_dict
                    }
                }
                videos_list.append(video_dict)

        plt_dict = {
            "playlist_title":item['snippet']['title'],
            "playlist_ID":item['id'],
            "playlist_description":item['snippet']['description'],
            "playlist_videos":vlt,
            "playlist_video_count":len(vlt),
            "videos":videos_list
        }
        play_list.append(plt_dict)
    guvi_format_data: dict = {
        channel_infos['snippet']['title']:{
            "Channel_Name":channel_infos['snippet']['title'],
            "Channel_Id":channel_infos['id'],
            "Subscription_Count":channel_infos['statistics'].get('subscriberCount', 0),
            "Channel_Views":channel_infos['statistics'].get('viewCount', 0),
            "Channel_Description":channel_infos['snippet']['description'],
            "Channel_Status":channel_infos['status'],
            "playlist":play_list
        }
    }
    return guvi_format_data