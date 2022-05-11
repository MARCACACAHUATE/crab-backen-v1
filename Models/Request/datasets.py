# Pydantic
from pydantic import BaseModel

# Typing
from datetime import date
from typing import Optional


class Dataset(BaseModel):
    fecha_inicio: date 
    fecha_fin: date