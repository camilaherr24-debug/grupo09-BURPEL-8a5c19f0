from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base

class HabilidadTecnologia(Base):
    __tablename__ = "habilidades_tecnologias"

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    tecnologia_id = Column(Integer, ForeignKey("tecnologias.id"), primary_key=True)