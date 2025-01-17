from alchemy_orm import Session, engine, User

local_session = Session(bind=engine)
user_to_update = local_session.query(User).filter(User.username == "jona").first()

user_to_update.username = "jonathan"
user_to_update.email = "jonathanc@ompany.com"

local_session.commit()
