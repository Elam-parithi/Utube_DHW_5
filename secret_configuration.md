# Configuring .streamlit/secrets.toml
If you don't create this secrets file, no problem. Its optional.
The YouTube API key is important, you can enter that one in the application manually.
## Overview
When I'm programming I included my `.streamlit\secrets.toml` in `.gitignore` file.
So, it is not available in the repo. you need to create one. This file is for keeping
secrets away when it comes to deployment on streamlit cloud and working with teams and locally.

you can also keep this .streamlit folder in your users folder as
`C:\Users\%username%\.streamlit\secrets.toml` this one is considered as global.

The another on the local projects folder was considered as per-project secrets.
When both file co-exists the local one will overwrite the global.
Example of Streamlit.toml
```bash
# .streamlit\secrets.toml
                                                              
database_uri = 'mysql+pymysql://user:password@host:port/database' 
api_key = '<YouTube API Key>'
mongo_uri = '<MongoDB URI>'

[default-settings]
defalt_channel = ['madras foodie','guvi', 'vice','<other channel names>']    # Max=10
```
## configuration
### SQL configuration
For SQL, you have two options one is using the SQLite which comes with built-in with 
python no complex requirements for this. another one is for locally hosted and
externally hosted, That will be required some bit of knowledge in the field. 

** **SQL URL should be set to `database_uri`**.
 - ***SQLite:***
If you need to change the folder name 
and filename you can do it here itself. `Database_storage` is folder name. 
And `Utube_DHW-5.db` is filename. Even if you don't create this one,
It will default to following example :->`sqlite:///Database_storage/Utube_DHW-5.db`.
 - ***MySQL:***
For this you should host a SQL server locally or user the URL of externally hosted SQL server.
You can use the IP or DNS with port number and username, Following is the syntax.
`mysql+pymysql://<user>:<password>@<host>:<port>/<dbname>`
### MongoDB configuration
** **Database URI should be set to `mongo_uri`**.

MongoDB's configuration is optional. For MongoDB The only option is URI, 
This URI is available with MongoDB cloud free host, or your self-hosted service.
It is upto you. Following is the example `mongodb://192.168.0.88:27017/?tls=false`.
### YouTube API key
** **YouTube API key should be set to `api_key`**.

Obtain YouTube Data API v3 API key from [Google Developers Console](https://console.developers.google.com/). 
And manage configure it here. Note: Configure here if you decided on using it permanently.
### Default_channel
Here, You can configure it on your default channel name and the max should be 10. 
```bash
[default-settings]
max_channels=10
defalt_channel = ['madras foodie','guvi', 'vice']
```
