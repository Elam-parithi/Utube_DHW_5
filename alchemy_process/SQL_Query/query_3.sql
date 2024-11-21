
-- Question 3

/*
What are the top 10 most viewed videos and their respective channels?
*/

SELECT channels.channel_name, Videos.video_name, Videos.view_count AS Total_Views FROM Videos
        JOIN channels ON channels.channel_id = Videos.channel_id
        ORDER BY Videos.view_count DESC LIMIT 10;