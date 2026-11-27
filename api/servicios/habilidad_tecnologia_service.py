from sqlalchemy.orm import Session
from api.models.habilidad_tecnologia import HabilidadTecnologia
from api.schemas.habilidad_tecnologia import HabilidadTecnologiaCreate

def obtener_habilidades_tecnologias(db: Session, usuario_id: int = None):
    consulta = db.query(HabilidadTecnologia)
    if usuario_id:
        consulta = consulta.filter(HabilidadTecnologia.usuario_id == usuario_id)
    return consulta.all()

def agregar_habilidad_tecnologia(db: Session, dato: HabilidadTecnologiaCreate):
    existe = db.query(HabilidadTecnologia).filter(
        HabilidadTecnologia.usuario_id == dato.usuario_id,
        HabilidadTecnologia.tecnologia_id == dato.tecnologia_id
    ).first()
    if existe:
        return None
    nuevo = HabilidadTecnologia(usuario_id=dato.usuario_id, tecnologia_id=dato.tecnologia_id)
    db.add(nuevo)
    db.commit()
    return nuevo

def quitar_habilidad_tecnologia(db: Session, usuario_id: int, tecnologia_id: int):
    elemento = db.query(HabilidadTecnologia).filter(
        HabilidadTecnologia.usuario_id == usuario_id,
        HabilidadTecnologia.tecnologia_id == tecnologia_id
    ).first()
    if elemento:
        db.delete(elemento)
        db.commit()
        return True
    return False