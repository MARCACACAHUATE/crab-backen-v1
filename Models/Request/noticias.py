from pydantic import BaseModel
from datetime import date


class Noticia(BaseModel):
    contenido: str
    fecha: date
    categoria_id: int
    pagina_id: int


class NoticiaRequest(BaseModel):
    fecha: date
    pagina: str
    data: list[Noticia]