
-- Question 1

/*
What are the names of all the videos and their corresponding channels?
*/

SELECT channels.channel_name, videos.video_name FROM videos 
        JOIN channels ON channels.channel_id = videos.channel_id
        ORDER BY channels.channel_name;