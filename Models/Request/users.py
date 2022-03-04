# Pydantic
from pydantic import BaseModel, Field

# Typing
from typing import Optional



class User(BaseModel):
    username: str = Field(title = "Username unico del usuario para identificarlo en la aplicacion", max_length = 20)
    email: str
    password: str