# _*_ coding: utf-8 _*_

"""
base model
"""

from datetime import date, datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from .. import PhoneStr

__all__ = [
    "date", "datetime", "Any", "Dict", "Optional",
    "BaseModel", "Field", "EmailStr", "HttpUrl", "PhoneStr",
]