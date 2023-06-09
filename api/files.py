# _*_ coding: utf-8 _*_

"""
files api
"""

import os
import time
from typing import Annotated

from fastapi import APIRouter, HTTPException, Security, status
from fastapi import File, Form, Path, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import Field

from core.settings import error_tips, settings
from data.models import User
from data.schemas import Resp
from .utils import ScopeName, get_current_user

# define router
router = APIRouter()

# define security scopes
security_scopes = Security(get_current_user, scopes=[ScopeName.files_ud, ])


# response model
class RespFile(Resp):
    file_id: str = Field(None)


@router.post("/upload", response_model=RespFile)
def _upload(current_user: Annotated[User, security_scopes],
            file: UploadFile = File(..., description="max file size")):
    """
    upload file, return file_id
    - **status=0**: upload success
    - **status_code=500**: file size too large
    """
    # check file size: raise exception
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_tips.FILE_SIZE_EXCEEDED,
        )
    file_id = f"{current_user.id}-{int(time.time())}-{file.filename}"

    # define file path and save file
    file_path = f"{settings.FOLDER_UPLOAD}/{file_id}"
    with open(file_path, "wb") as file_in:
        file_in.write(file.file.read())

    # return file_id
    return RespFile(file_id=file_id)


@router.post("/upload-flow", response_model=RespFile)
def _upload_flow(current_user: Annotated[User, security_scopes],
                 file: UploadFile = File(..., description="max file size"),
                 flow_chunk_number: int = Form(..., alias="flowChunkNumber"),
                 flow_chunk_total: int = Form(..., alias="flowChunkTotal"),
                 flow_total_size: int = Form(..., alias="flowTotalSize"),
                 flow_identifier: str = Form(..., alias="flowIdentifier")):
    """
    upload file by flow.js
    - **status=0**: uploading or upload success
    - **status_code=500**: file size too large
    """
    # check file size: raise exception
    if flow_total_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_tips.FILE_SIZE_EXCEEDED,
        )

    # define file path temp
    file_name_temp = f"{flow_identifier}-{file.filename}"
    file_path_temp = f"{settings.FOLDER_UPLOAD}/{file_name_temp}"

    # save flow_chunk_number part
    file_mode = "ab" if flow_chunk_number > 1 else "wb"
    with open(file_path_temp, file_mode) as file_in:
        file_in.write(file.file.read())

    # check if all parts are uploaded
    if flow_chunk_number != flow_chunk_total:
        return RespFile(msg="uploading")
    file_id = f"{current_user.id}-{int(time.time())}-{file.filename}"

    # define file path and save file
    file_path = f"{settings.FOLDER_UPLOAD}/{file_id}"
    with open(file_path, "wb") as file_in:
        with open(file_path_temp, "rb") as file_temp:
            file_in.write(file_temp.read())

    # return file_id
    return RespFile(file_id=file_id)


@router.get("/download/{file_id}", response_class=FileResponse)
def _download(current_user: Annotated[User, security_scopes],
              file_id: str = Path(..., description="file id")):
    """
    download file by file_id
    - **status_code=500**: file not existed
    """
    # define file path: raise exception
    file_path = f"{settings.FOLDER_UPLOAD}/{file_id}"
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_tips.FILE_NOT_EXISTED,
        )

    # define file name and return file
    file_name = "-".join(file_id.split("-")[2:])
    return FileResponse(file_path, filename=file_name)


@router.get("/download-stream/{file_id}", response_class=StreamingResponse)
def _download_stream(current_user: Annotated[User, security_scopes],
                     file_id: str = Path(..., description="file id")):
    """
    download file by file_id
    - **status_code=500**: file not existed
    """
    # define file path: raise exception
    file_path = f"{settings.FOLDER_UPLOAD}/{file_id}"
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_tips.FILE_NOT_EXISTED,
        )

    # define iter function
    def iter_file() -> iter:
        with open(file_path, "rb") as file_in:
            yield from file_in

    # define file name and return file
    file_name = "-".join(file_id.split("-")[2:])
    headers = {"Content-Disposition": f"attachment; filename={file_name}"}
    return StreamingResponse(iter_file(), media_type="audio/mpeg", headers=headers)
