from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db import get_db
from api.schemas.habilidad_tecnologia import HabilidadTecnologia, HabilidadTecnologiaCreate
from api.services import habilidad_tecnologia_service

router = APIRouter(prefix="/habilidades-tecnologias", tags=["Habilidades - Tecnologías"])

@router.get("/")
def listar_habilidades(usuario_id: int = None, db: Session = Depends(get_db)):
    return habilidad_tecnologia_service.obtener_habilidades_tecnologias(db, usuario_id)

@router.post("/", status_code=201)
def agregar_habilidad(dato: HabilidadTecnologiaCreate, db: Session = Depends(get_db)):
    nuevo = habilidad_tecnologia_service.agregar_habilidad_tecnologia(db, dato)
    if not nuevo:
        raise HTTPException(status_code=400, detail="La habilidad ya existe")
    return nuevo

@router.delete("/")
def quitar_habilidad(usuario_id: int, tecnologia_id: int, db: Session = Depends(get_db)):
    ok = habilidad_tecnologia_service.quitar_habilidad_tecnologia(db, usuario_id, tecnologia_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")
    return {"mensaje": "Habilidad eliminada correctamente"}