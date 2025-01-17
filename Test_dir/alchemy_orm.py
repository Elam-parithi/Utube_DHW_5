from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, String, DateTime, Integer

import os
from datetime import datetime

Base = declarative_base()
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///" + os.path.join(BASE_DIR, "test_orm_1810.db")
engine = create_engine(connection_string, echo=True)
Session=sessionmaker()


class User(Base):
    __tablename__ = 'users_table'
    id = Column(Integer(), primary_key=True)
    username = Column(String(25), nullable=False, unique=True)
    email = Column(String(80), unique=True, nullable=False)
    date_created = Column(DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"<User username={self.username} email={self.email}>"


new_user = User(id=1, username="Jonathan", email="jona@jona.com")
print(new_user)
