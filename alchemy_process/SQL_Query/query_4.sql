
-- Question 4

/*
How many comments were made on each video, and what are their corresponding video names?
*/

SELECT videos.video_name, videos.comment_count AS Total_Comments FROM videos
        ORDER BY videos.comment_count DESC;