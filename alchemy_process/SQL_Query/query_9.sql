
-- Question 9

/*
What is the average duration of all videos in each channel, and what are their corresponding channel names?
*/

SELECT channels.channel_name, TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(TIME(videos.duration)))), "%H:%i:%s") AS Duration FROM Videos
        JOIN channels ON videos.channel_id = channels.channel_id
        GROUP BY channels.channel_name;