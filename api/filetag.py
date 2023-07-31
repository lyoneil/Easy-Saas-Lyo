# _*_ coding: utf-8 _*_

"""
filetag api
"""

import time
from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi import Body, Depends, Path, Query
from pydantic import Field
from sqlalchemy.orm import Session

from core.utils import get_id_string
from data import get_session
from data.models import FILETAG_SYSTEM_SET, FileTag, User
from data.schemas import FileTagCreate, FileTagSchema, FileTagUpdate, Resp
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespFileTag(Resp):
    data_filetag: FileTagSchema = Field(None)


# response model
class RespFileTagList(Resp):
    data_filetag_list: List[FileTagSchema] = Field(None)


@router.get("/", response_model=RespFileTagList)
def _get_filetag_schema_list(skip: int = Query(0, description="skip count"),
                             limit: int = Query(10, description="limit count"),
                             current_user: User = Depends(get_current_user),
                             session: Session = Depends(get_session)):
    """
    get filetag schema list and return
    """
    user_id = current_user.id

    # filetag schema list
    filetag_model_list = session.query(FileTag).filter(
        FileTag.user_id == user_id,
    ).offset(skip).limit(limit).all()
    filetag_schema_list = [FileTagSchema(**fm.dict()) for fm in filetag_model_list]

    # return filetag schema list
    return RespFileTagList(data_filetag_list=filetag_schema_list)


def check_filetag_permission(filetag_id: str, user_id: str, session: Session) -> FileTag:
    """
    check if filetag_id is valid and user_id has permission to access filetag
    """
    filetag_model = session.query(FileTag).get(filetag_id)
    if (not filetag_model) or (filetag_model.user_id != user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no permission to access filetag",
        )
    return filetag_model


@router.post("/", response_model=RespFileTag)
def _create_filetag_model(filetag_schema: FileTagCreate = Body(..., description="create schema"),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    create filetag model based on create schema, return filetag schema
    - **status=-1**: filetag name invalid or existed
    """
    user_id = current_user.id

    # check if filetag name is valid
    if filetag_schema.name in FILETAG_SYSTEM_SET:
        return RespFileTag(status=-1, msg="filetag name invalid")
    filetag_name = filetag_schema.name

    # check if filetag name existed
    for filetag_model in current_user.filetags:
        if filetag_name != filetag_model.name:
            continue
        return RespFileTag(status=-1, msg="filetag name existed")
    filetag_id = get_id_string(f"{user_id}-{filetag_name}-{time.time()}")

    # create filetag model based on create schema, ttype="custom"
    filetag_kwargs = filetag_schema.model_dump(exclude_unset=True)
    filetag_model = FileTag(id=filetag_id, user_id=user_id, **filetag_kwargs)
    session.add(filetag_model)
    session.commit()

    # return filetag schema
    return RespFileTag(data_filetag=FileTagSchema(**filetag_model.dict()))


@router.patch("/{filetag_id}", response_model=RespFileTag)
def _update_filetag_model(filetag_id: str = Path(..., description="id of filetag"),
                          filetag_schema: FileTagUpdate = Body(..., description="update schema"),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    update filetag model based on update schema, return filetag schema
    - **status=-1**: filetag name invalid or existed
    - **status_code=403**: no permission to access filetag
    """
    user_id = current_user.id

    # check if filetag name is valid
    if filetag_schema.name in FILETAG_SYSTEM_SET:
        return RespFileTag(status=-1, msg="filetag name invalid")
    filetag_name = filetag_schema.name

    # check if filetag name existed
    for filetag_model in current_user.filetags:
        if filetag_name != filetag_model.name:
            continue
        return RespFileTag(status=-1, msg="filetag name existed")
    filetag_model = check_filetag_permission(filetag_id, user_id, session)

    # update filetag model based on update schema
    for field in filetag_schema.model_dump(exclude_unset=True):
        setattr(filetag_model, field, getattr(filetag_schema, field))
    session.merge(filetag_model)
    session.commit()

    # return filetag schema
    return RespFileTag(data_filetag=FileTagSchema(**filetag_model.dict()))


@router.delete("/{filetag_id}", response_model=RespFileTag)
def _delete_filetag_model(filetag_id: str = Path(..., description="id of filetag"),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    delete filetag model by id, return filetag schema
    - **status=-2**: filetag not empty with files
    - **status_code=403**: no permission to access filetag
    """
    user_id = current_user.id
    filetag_model = check_filetag_permission(filetag_id, user_id, session)

    # check if filetag not empty
    if filetag_model.filetagfiles:
        return RespFileTag(status=-2, msg="filetag not empty with files")

    # delete filetag model
    session.delete(filetag_model)
    session.commit()

    # return filetag schema
    return RespFileTag(data_filetag=FileTagSchema(**filetag_model.dict()))
