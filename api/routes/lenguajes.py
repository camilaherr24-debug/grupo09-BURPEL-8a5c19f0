from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db import get_db
from api.schemas.lenguaje import Lenguaje, LenguajeCreate
from api.services import lenguaje_service

router = APIRouter(prefix="/lenguajes", tags=["Lenguajes"])

@router.get("/", response_model=list[Lenguaje])
def listar_lenguajes(db: Session = Depends(get_db)):
    return lenguaje_service.obtener_lenguajes(db)

@router.get("/{lenguaje_id}", response_model=Lenguaje)
def obtener_lenguaje(lenguaje_id: int, db: Session = Depends(get_db)):
    dato = lenguaje_service.obtener_lenguaje_por_id(db, lenguaje_id)
    if not dato:
        raise HTTPException(status_code=404, detail="Lenguaje no encontrado")
    return dato

@router.post("/", response_model=Lenguaje, status_code=201)
def crear_lenguaje(lenguaje: LenguajeCreate, db: Session = Depends(get_db)):
    nuevo = lenguaje_service.crear_lenguaje(db, lenguaje)
    if not nuevo:
        raise HTTPException(status_code=400, detail="El lenguaje ya existe")
    return nuevo

@router.delete("/{lenguaje_id}")
def eliminar_lenguaje(lenguaje_id: int, db: Session = Depends(get_db)):
    ok = lenguaje_service.eliminar_lenguaje(db, lenguaje_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Lenguaje no encontrado")
    return {"mensaje": "Lenguaje eliminado correctamente"}