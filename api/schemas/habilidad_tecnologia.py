from pydantic import BaseModel

class HabilidadTecnologiaCreate(BaseModel):
    usuario_id: int
    tecnologia_id: int

class HabilidadTecnologia(HabilidadTecnologiaCreate):
    class Config:
        orm_mode = True