# Configure page 

In this page we will see how to get Google YouTube API key and MySQL URL and MongoDB URI.
Where we can get those credentials and how to make it.

### Google YouTube API Key:
- Go to the [Google Cloud Console](URL).
- Create a new project or select an existing one.
- Navigate to APIs & Services > Library.
- Search for YouTube Data API v3 and enable it.
- Go to APIs & Services > Credentials.
- Click Create Credentials and choose API Key.
- Copy the generated API key and use it in your application.
    
     
### MySQL DB URL:
For more URL details follow the link [Connection URL Syntax](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-jdbc-url-format.html)

```bash
mysql://username:password@ip_address/database_name
```
    
Example
    
```bash
mongodb://user123:pass456@mydb.example.com:27017/mydb
```

### Mongo DB URI:
For more details on connection URI link [Connection Strings](https://www.mongodb.com/docs/manual/reference/connection-string/)
   ```bash
   mongodb://username:password@domain:port/database_name
   ```