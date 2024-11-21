
-- Question 8

/*
 What are the names of all the channels that have published videos in the year 2022?
*/

SELECT DISTINCT channels.channel_name FROM channels
        JOIN Videos ON Videos.channel_id = channels.channel_id
        WHERE YEAR(Videos.published_date) = 2022;