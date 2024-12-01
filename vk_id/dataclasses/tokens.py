from typing import Optional
from pydantic import BaseModel


class Tokens(BaseModel):
    """
    Общий ответ для двух запросов
    """

    refresh_token: str
    access_token: str
    token_type: str
    expires_in: int
    user_id: int
    state: str
    scope: str
    id_token: Optional[str] = None

    class Config:
        from_attributes = True
