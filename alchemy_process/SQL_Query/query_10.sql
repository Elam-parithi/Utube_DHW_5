
-- Question 10

/*
Which videos have the highest number of comments, and what are their corresponding channel names?
*/

SELECT channels.channel_name, videos.video_name, videos.comment_count AS Total_Comments FROM videos
        JOIN channels ON channels.channel_id = videos.channel_id ORDER BY videos.comment_count DESC;