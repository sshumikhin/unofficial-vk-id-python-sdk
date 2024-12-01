import datetime
import enum
from pydantic import BaseModel, field_validator
from typing import Optional, Union, Any


class Gender(enum.StrEnum):
    MAN = "man"
    WOMAN = "woman"
    UNDEFINED = "undefined"


class User(BaseModel):
    user_id: Optional[str] = None
    first_name: str
    last_name: str
    avatar: str
    sex: Union[int, str]
    birthday: str | datetime.date
    phone: Optional[str] = None
    email: Optional[str] = None
    sex: Optional[int] = None
    verified: bool

    @field_validator("sex")
    def check_sex(cls, v):
        if v == 1:
            return Gender.WOMAN.value
        elif v == 2:
            return Gender.MAN.value
        else:
            return Gender.UNDEFINED.value

    @field_validator("birthday")
    def check_birthday(cls, v):
        return datetime.datetime.strptime(v, "%d.%m.%Y").date()

    @field_validator("email")
    def validate_email(cls, v):
        if v == '':
            return None
        return v