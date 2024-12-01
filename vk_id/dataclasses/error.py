from typing import Optional
from pydantic import BaseModel


class Error(BaseModel):
    error: str
    error_description: str
    state: Optional[str] = None