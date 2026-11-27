from pydantic import BaseModel, Field
from typing import Optional

class TecnologiaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None

class TecnologiaCreate(TecnologiaBase):
    pass

class Tecnologia(TecnologiaBase):
    id: int

    class Config:
        orm_mode = True