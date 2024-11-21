
-- Question 2

/*
Which channels have the most number of videos, and how many videos do they have?
*/

SELECT DISTINCT channels.channel_name, COUNT(Videos.video_id) AS Total_Videos FROM channels 
        JOIN Videos ON channels.channel_id = Videos.channel_id GROUP BY channels.channel_name 
        ORDER BY Total_Videos DESC;