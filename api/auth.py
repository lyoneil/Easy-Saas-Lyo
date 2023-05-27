# _*_ coding: utf-8 _*_

"""
auth api
"""

import logging
import random
from enum import Enum

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, Field
from sqlalchemy.orm import Session

from core.security import check_password_hash, get_password_hash
from core.security import create_token_data, get_token_payload
from core.settings import error_tips, settings
from core.utemail import send_email
from data import get_session
from data.crud import crud_user
from data.schemas import AccessToken, Resp
from data.schemas import UserCreatePri, UserUpdatePri

# define router
router = APIRouter()


@router.post("/access-token", response_model=AccessToken)
def _access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    get access_token by OAuth2PasswordRequestForm, return access_token or raise exception(401)
    - **username**: value of email
    - **password**: value of password
    - **scopes**: value of scopes, split by space
    """
    # get username and password from form_data
    email, pwd_plain = form_data.username, form_data.password

    # check if user existed (must raise exception)
    user_model = crud_user.get_by_email(session, email=email)
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_tips.EMAIL_NOT_EXISTED,
        )
    pwd_hash = user_model.password

    # check password (must raise exception)
    if not check_password_hash(pwd_plain, pwd_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_tips.PWD_INCORRECT,
        )
    user_id = user_model.id

    # create access_token with user_id and scopes: List[str]
    access_token = create_token_data({"sub": str(user_id), "scopes": form_data.scopes})
    logging.warning("create access_token: %s - %s - %s", user_id, form_data.scopes, access_token)

    # return access_token
    return AccessToken(access_token=access_token)


# define enum of type
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


# response model
class RespSend(Resp):
    data: str = Field(None, description="token")


@router.post("/send-code", response_model=RespSend)
def _send_code(email: EmailStr = Body(...),
               _type: TypeName = Body(...),
               session: Session = Depends(get_session)):
    """
    send a code to email, and return token with code
    - **status=0**: send email success, data=token
    - **status=-1**: email existed or not existed
    - **status=-2**: send email failed
    """
    # check user existed or not
    user_model = crud_user.get_by_email(session, email=email)
    if _type == TypeName.signup and user_model:
        return RespSend(status=-1, msg=error_tips.EMAIL_EXISTED)
    if _type == TypeName.reset and (not user_model):
        return RespSend(status=-1, msg=error_tips.EMAIL_NOT_EXISTED)

    # define code, data and token
    code = random.randint(100000, 999999)
    data = dict(sub=email, code=code, type=_type)
    token = create_token_data(data, expires_duration=settings.NORMAL_TOKEN_EXPIRE_DURATION)

    # define email content and render
    mail_subject = "Verify of {{ app_name }}"
    mail_html = "Verify code: <b>{{ code }}</b>"
    render = dict(app_name=settings.APP_NAME, code=code)

    # send email and check status_code
    _from = (settings.APP_NAME, settings.MAIL_USERNAME)
    status_code = send_email(_from, email, subject=mail_subject, html=mail_html, render=render)
    if status_code != 250:
        return RespSend(status=-2, msg=error_tips.EMAIL_SEND_FAILED)
    logging.warning("send code: %s - %s - %s - %s", email, code, _type, token)

    # return token with code
    return RespSend(data=token)


@router.post("/verify-code", response_model=Resp)
def _verify_code(code: int = Body(..., ge=100000, le=999999),
                 token: str = Body(..., min_length=10),
                 password: str = Body(..., min_length=6, max_length=20),
                 session: Session = Depends(get_session)):
    """
    verify code and token, then create user or update password
    - **status=0**: verify success
    - **status=-1**: token invalid
    - **status=-2**: code invalid
    """
    # get payload from token
    payload = get_token_payload(token)
    logging.warning("get payload: %s - %s", code, payload)

    # check token: type(!!!)
    if (not payload.get("type")) or (payload["type"] not in TypeName.__members__):
        return Resp(status=-1, msg=error_tips.TOKEN_INVALID)
    _type = payload["type"]

    # check token: email (sub)
    if not payload.get("sub"):
        return Resp(status=-1, msg=error_tips.TOKEN_INVALID)
    email = payload["sub"]

    # check token: code
    if (not payload.get("code")) or (payload["code"] != code):
        return Resp(status=-2, msg=error_tips.CODE_INVALID)
    pwd_hash = get_password_hash(password)

    # get user from db
    user_model = crud_user.get_by_email(session, email=email)

    # check token type: signup
    if _type == TypeName.signup and (not user_model):
        # create user based on UserCreatePri
        user_schema = UserCreatePri(email=email, password=pwd_hash, email_verified=True)
        user_model = crud_user.create(session, obj_schema=user_schema)

        # logging and return result
        logging.warning("create user: %s", user_model.to_dict())
        return Resp(msg=f"{_type} successfully")

    # check token type: reset
    if _type == TypeName.reset and user_model:
        # update password based on UserUpdatePri
        user_schema = UserUpdatePri(password=pwd_hash)
        user_model = crud_user.update(session, obj_model=user_model, obj_schema=user_schema)

        # logging and return result
        logging.warning("reset password: %s", user_model.to_dict())
        return Resp(msg=f"{_type} successfully")

    # return result
    return Resp(status=-1, msg=error_tips.TOKEN_INVALID)
