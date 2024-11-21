
-- Question 7

/*
What is the total number of views for each channel, and what are their corresponding channel names?
*/

SELECT channels.channel_name, channels.channel_views AS Total_Views FROM channels
        ORDER BY channels.channel_views DESC;