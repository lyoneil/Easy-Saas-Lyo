# _*_ coding: utf-8 _*_

"""
api module
"""

from fastapi import APIRouter

from . import auth, project, user

# define api_router
api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(project.router, prefix="/project", tags=["project"])
