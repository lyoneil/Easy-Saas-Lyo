# _*_ coding: utf-8 _*_

"""
test models and schemas
"""

import logging

from pydantic import EmailStr

from core import security
from data import SessionMaker
from data.dmysql import init_db
from data.models import *
from data.schemas import *

# init db
init_db()

with SessionMaker() as session:
    # user info =========================================================================
    email = EmailStr("admin@easysaas.com")
    password = security.get_password_hash("a123456")

    # create user -- schema of UserCreate
    user_schema = UserCreate(email=email, password=password)

    # create user -- model of User
    user_model = User(id=100000, name=email, **user_schema.dict(exclude_unset=True))
    session.add(user_model)
    session.commit()
    logging.warning(user_model.to_dict())

    # update user -- schema of UserUpdate
    user_schema = UserUpdate(name="admin", avatar="http://www.easysaas.com")
    for field in user_schema.dict(exclude_unset=True):
        setattr(user_model, field, getattr(user_schema, field))
    user_model.system_admin = True
    user_model.system_role = {"role": "admin", "scopes": ["user:read", ]}
    session.merge(user_model)
    session.commit()
    logging.warning(user_model.to_dict())
