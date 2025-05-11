from pydantic import BaseModel
from typing import Optional

class SecretCreate(BaseModel):
    message: str
    password: Optional[str]
    ttl_choice: Optional[str]

class SecretView(BaseModel):
    token: str
    password: Optional[str]