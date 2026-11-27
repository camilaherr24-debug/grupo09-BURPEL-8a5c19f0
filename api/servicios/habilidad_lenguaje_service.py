from sqlalchemy.orm import Session
from api.models.habilidad_lenguaje import HabilidadLenguaje
from api.schemas.habilidad_lenguaje import HabilidadLenguajeCreate

def obtener_habilidades_lenguajes(db: Session, usuario_id: int = None):
    consulta = db.query(HabilidadLenguaje)
    if usuario_id:
        consulta = consulta.filter(HabilidadLenguaje.usuario_id == usuario_id)
    return consulta.all()

def agregar_habilidad_lenguaje(db: Session, dato: HabilidadLenguajeCreate):
    existe = db.query(HabilidadLenguaje).filter(
        HabilidadLenguaje.usuario_id == dato.usuario_id,
        HabilidadLenguaje.lenguaje_id == dato.lenguaje_id
    ).first()
    if existe:
        return None
    nuevo = HabilidadLenguaje(usuario_id=dato.usuario_id, lenguaje_id=dato.lenguaje_id)
    db.add(nuevo)
    db.commit()
    return nuevo

def quitar_habilidad_lenguaje(db: Session, usuario_id: int, lenguaje_id: int):
    elemento = db.query(HabilidadLenguaje).filter(
        HabilidadLenguaje.usuario_id == usuario_id,
        HabilidadLenguaje.lenguaje_id == lenguaje_id
    ).first()
    if elemento:
        db.delete(elemento)
        db.commit()
        return True
    return False