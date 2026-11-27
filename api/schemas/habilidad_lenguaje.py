from pydantic import BaseModel

class HabilidadLenguajeCreate(BaseModel):
    usuario_id: int
    lenguaje_id: int

class HabilidadLenguaje(HabilidadLenguajeCreate):
    class Config:
        orm_mode = True