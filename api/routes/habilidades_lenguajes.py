from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db import get_db
from api.schemas.habilidad_lenguaje import HabilidadLenguaje, HabilidadLenguajeCreate
from api.services import habilidad_lenguaje_service

router = APIRouter(prefix="/habilidades-lenguajes", tags=["Habilidades - Lenguajes"])

@router.get("/")
def listar_habilidades(usuario_id: int = None, db: Session = Depends(get_db)):
    return habilidad_lenguaje_service.obtener_habilidades_lenguajes(db, usuario_id)

@router.post("/", status_code=201)
def agregar_habilidad(dato: HabilidadLenguajeCreate, db: Session = Depends(get_db)):
    nuevo = habilidad_lenguaje_service.agregar_habilidad_lenguaje(db, dato)
    if not nuevo:
        raise HTTPException(status_code=400, detail="La habilidad ya existe")
    return nuevo

@router.delete("/")
def quitar_habilidad(usuario_id: int, lenguaje_id: int, db: Session = Depends(get_db)):
    ok = habilidad_lenguaje_service.quitar_habilidad_lenguaje(db, usuario_id, lenguaje_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")
    return {"mensaje": "Habilidad eliminada correctamente"}