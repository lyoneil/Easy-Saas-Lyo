# _*_ coding: utf-8 _*_

"""
project schema
"""

from typing import Optional

from pydantic import BaseModel, Field


# used for response_model
class ProjectSchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    permission: Optional[int] = None


# used for request body
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=4, max_length=100)
    desc: Optional[str] = Field(description="Description")


# used for request body
class ProjectUpdate(BaseModel):
    id: str = Field(..., description="Project ID")
    name: Optional[str] = Field(min_length=4, max_length=100)
    desc: Optional[str] = Field(description="Description")
