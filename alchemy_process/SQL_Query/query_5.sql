
-- Question 5

/*
Which videos have the highest number of likes, and what are their corresponding channel names?
*/

SELECT channels.channel_name, videos.video_name, videos.like_count AS Highest_Likes FROM videos 
        JOIN channels ON videos.channel_id = channels.channel_id
        WHERE videos.like_count = (SELECT MAX(v.like_count) FROM videos v WHERE videos.channel_id = v.channel_id)
        ORDER BY Highest_Likes DESC;