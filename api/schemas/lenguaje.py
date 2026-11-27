from pydantic import BaseModel, Field
from typing import Optional

class LenguajeBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None

class LenguajeCreate(LenguajeBase):
    pass

class Lenguaje(LenguajeBase):
    id: int

    class Config:
        orm_mode = True