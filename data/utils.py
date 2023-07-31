# _*_ coding: utf-8 _*_

"""
utility functions
"""

import time

from pydantic import constr
from sqlalchemy.orm import Session

from core.utils import get_id_string
from .models import FileTag, User
from .schemas import FileTagCreate, UserCreate

# define filetags of system
FILETAG_SYSTEM_SET = {"untagged", "favorite", "collect", "trash"}

# define type of PhoneStr
PhoneStr = constr(pattern=r"^\+\d{1,3}-\d{7,15}$")


def init_db_table(model=None) -> None:
    """
    initialize database or table
    """
    from .dmysql import engine
    from .models.base import Model
    if not model:
        Model.metadata.drop_all(engine, checkfirst=True)
        Model.metadata.create_all(engine, checkfirst=True)
    else:
        model.__table__.drop(engine, checkfirst=True)
        model.__table__.create(engine, checkfirst=True)
    return None


def init_user_object(user_schema: UserCreate, session: Session) -> User:
    """
    initialize user object based on create schema
    """
    try:
        # create user model and add to database
        user_id = get_id_string(f"{user_schema.password}-{time.time()}")
        user_model = User(id=user_id, **user_schema.model_dump(exclude_unset=True))
        session.add(user_model)

        # create filetag model
        user_id = user_model.id
        for filetag_name in FILETAG_SYSTEM_SET:
            # create filetag_id and filetag schema
            filetag_id = get_id_string(f"{user_id}-{filetag_name}-{time.time()}")
            filetag_schema = FileTagCreate(name=filetag_name, icon="default", color="default")

            # create filetag model and add to database, ttype="system"
            filetag_kwargs = filetag_schema.model_dump(exclude_unset=True)
            filetag_model = FileTag(id=filetag_id, user_id=user_id, **filetag_kwargs, ttype="system")
            session.add(filetag_model)

        # commit session
        session.commit()
        return user_model
    except Exception as excep:
        session.rollback()
        raise excep
