from alchemy_orm import Session, engine, User
from sqlalchemy import desc

local_session = Session(bind=engine)

# ascending
user_asc = local_session.query(User).order_by(User.username).all()

# descending order
users_desc = local_session.query(User).order_by(desc(User.username)).all()

for user in users_desc:
    print(f"User {user.username}")

for user in user_asc:
    print(f"User {user.username}")
