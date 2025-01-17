from alchemy_orm import User, Session, engine

users_list = [
    {
        "username":"jerry",
        "email":"jerry@company.com"
    }, {
        "username":"jordan",
        "email":"jordan@company.com"
    }, {
        "username":"jackson",
        "email":"jackson@company.com"
    }, {
        "username":"jarden",
        "email":"jarden@company.com"
    }, {
        "username":"jhon",
        "email":"jhon@company.com"
    }, {
        "username":"jack",
        "email":"jack@company.com"
    },
]

local_session = Session(bind=engine)
"""
new_user = User(username="jona", email="jona@company.com")

local_session.add(new_user)

local_session.commit()
"""

for u in users_list:
    new_user = User(username=u["username"], email=u["email"])

    local_session.add(new_user)
    local_session.commit()
    print(f"Added{u['username']}")
