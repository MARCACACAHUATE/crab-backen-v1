# Pydantic
from pydantic import BaseModel, Field

# Typing
from typing import List, Optional



class User(BaseModel):
    username: str = Field(title = "Username unico del usuario para identificarlo en la aplicacion", max_length = 20)
    email: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_admin: bool = False
    is_active: bool = True

    # Esta madre es para los permisos
    principals: List[str] = []


class UserStatus(BaseModel):
    is_active: bool