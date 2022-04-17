from pydantic import BaseModel
from datetime import date
from typing import Optional

class NoticiaResponse(BaseModel):
    cantidad_noticias: Optional[str]
    fecha: Optional[date]
    pagina: Optional[str]
    mensaje: str