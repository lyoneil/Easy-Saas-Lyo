# _*_ coding: utf-8 _*_

"""
schemas module
"""

from pydantic import BaseModel

from .file import FileTagCreate, FileTagSchema, FileTagUpdate
from .project import ProjectCreate, ProjectSchema, ProjectUpdate
from .user import UserCreate, UserSchema, UserUpdate


class AccessToken(BaseModel):
    access_token: str  # required
    token_type: str = "bearer"


class Resp(BaseModel):
    status: int = 0
    msg: str = "success"
