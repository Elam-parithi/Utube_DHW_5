
# Reasons For choosing MySQL

When I initially tried to write program with DataBase I tried to include multiple different database types.
But, Upon programming more and more with Alchemy, Handling all those database for this project alone not worth it.
So, I remove all those previously added code after taking decision.
Here are few issues I faced with it in the beginning. 

## Issues faced on this project
- ### **BigInt Format Compatibility**
  On trying out new channel names with this program I found in a lot of channel's likes, subscription, views are in 
BigInt format. SQLite does not support BigInt format. you can convert it as str and go ahead. 
But MySQL has other trade-offs.
- ### **Write Limitations with SQLite**
    If you are using it with SQLite it only allows one person to write to it. But multiple reads. 
This writing limitation will bring issues when you run another run command.

- ### **Handling Duplicate Errors**
    handling duplicate error messages in different Databases
  - MySQL: `"Duplicate entry"` is standard for duplicate key violations.
  - SQLite: `"UNIQUE constraint failed"` in the exception message.
  - PostgreSQL: `"unique_violation"` in the error code or message.

## Conclusion:
Those above have different results. so, I need to try out all those database and program all those errors in a program.
When even using SQLAlchemy ORM.

So, for sake of making it more **readable** and keeping it **simple**.

I'm Sticking with my familiar SQL variant MySQL.