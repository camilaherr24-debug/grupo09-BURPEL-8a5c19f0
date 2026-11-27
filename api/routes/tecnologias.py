from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db import get_db
from api.schemas.tecnologia import Tecnologia, TecnologiaCreate
from api.services import tecnologia_service

router = APIRouter(prefix="/tecnologias", tags=["Tecnologías"])

@router.get("/", response_model=list[Tecnologia])
def listar_tecnologias(db: Session = Depends(get_db)):
    return tecnologia_service.obtener_tecnologias(db)

@router.get("/{tecnologia_id}", response_model=Tecnologia)
def obtener_tecnologia(tecnologia_id: int, db: Session = Depends(get_db)):
    dato = tecnologia_service.obtener_tecnologia_por_id(db, tecnologia_id)
    if not dato:
        raise HTTPException(status_code=404, detail="Tecnología no encontrada")
    return dato

@router.post("/", response_model=Tecnologia, status_code=201)
def crear_tecnologia(tecnologia: TecnologiaCreate, db: Session = Depends(get_db)):
    nuevo = tecnologia_service.crear_tecnologia(db, tecnologia)
    if not nuevo:
        raise HTTPException(status_code=400, detail="La tecnología ya existe")
    return nuevo

@router.delete("/{tecnologia_id}")
def eliminar_tecnologia(tecnologia_id: int, db: Session = Depends(get_db)):
    ok = tecnologia_service.eliminar_tecnologia(db, tecnologia_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tecnología no encontrada")
    return {"mensaje": "Tecnología eliminada correctamente"}