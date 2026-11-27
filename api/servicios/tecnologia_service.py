from sqlalchemy.orm import Session
from api.models.tecnologia import Tecnologia
from api.schemas.tecnologia import TecnologiaCreate

def obtener_tecnologias(db: Session):
    return db.query(Tecnologia).all()

def obtener_tecnologia_por_id(db: Session, tecnologia_id: int):
    return db.query(Tecnologia).filter(Tecnologia.id == tecnologia_id).first()

def crear_tecnologia(db: Session, tecnologia: TecnologiaCreate):
    existe = db.query(Tecnologia).filter(Tecnologia.nombre == tecnologia.nombre).first()
    if existe:
        return None
    nueva = Tecnologia(nombre=tecnologia.nombre, descripcion=tecnologia.descripcion)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def eliminar_tecnologia(db: Session, tecnologia_id: int):
    elemento = db.query(Tecnologia).filter(Tecnologia.id == tecnologia_id).first()
    if elemento:
        db.delete(elemento)
        db.commit()
        return True
    return False