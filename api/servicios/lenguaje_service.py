from sqlalchemy.orm import Session
from api.models.lenguaje import Lenguaje
from api.schemas.lenguaje import LenguajeCreate

def obtener_lenguajes(db: Session):
    return db.query(Lenguaje).all()

def obtener_lenguaje_por_id(db: Session, lenguaje_id: int):
    return db.query(Lenguaje).filter(Lenguaje.id == lenguaje_id).first()

def crear_lenguaje(db: Session, lenguaje: LenguajeCreate):
    existe = db.query(Lenguaje).filter(Lenguaje.nombre == lenguaje.nombre).first()
    if existe:
        return None
    nuevo = Lenguaje(nombre=lenguaje.nombre, descripcion=lenguaje.descripcion)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def eliminar_lenguaje(db: Session, lenguaje_id: int):
    elemento = db.query(Lenguaje).filter(Lenguaje.id == lenguaje_id).first()
    if elemento:
        db.delete(elemento)
        db.commit()
        return True
    return False