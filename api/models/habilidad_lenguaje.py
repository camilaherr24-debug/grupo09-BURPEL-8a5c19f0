from sqlalchemy import Column, Integer, ForeignKey
from api.db import Base

class HabilidadLenguaje(Base):
    __tablename__ = "habilidades_lenguajes"

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    lenguaje_id = Column(Integer, ForeignKey("lenguajes.id"), primary_key=True)