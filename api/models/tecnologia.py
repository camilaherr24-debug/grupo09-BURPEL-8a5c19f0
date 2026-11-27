from sqlalchemy import Column, Integer, String
from api.db import Base

class Tecnologia(Base):
    __tablename__ = "tecnologias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)