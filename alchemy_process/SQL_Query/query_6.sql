
-- Question 6

/*
What is the total number of likes and dislikes for each video, and what are their corresponding video names?
*/

SELECT videos.video_name, videos.like_count AS Likes FROM videos
        ORDER BY videos.like_count DESC;