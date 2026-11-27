from api.models.base import ModeloBase
from api.models.lenguaje.lenguaje_mapping import MAPEO_LENGUAJE
from api.utils.esquemas import cargar_esquema_json

class Lenguaje(ModeloBase):
    schema = cargar_esquema_json("lenguaje.schema.json")
    _columna_de = MAPEO_LENGUAJE
    tabla = "lenguajes"