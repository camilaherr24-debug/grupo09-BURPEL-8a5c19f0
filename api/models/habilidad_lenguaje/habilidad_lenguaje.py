from api.models.base import ModeloBase
from api.models.habilidad_lenguaje.habilidad_lenguaje_mapping import MAPEO_HABILIDAD_LENGUAJE
from api.utils.esquemas import cargar_esquema_json

class HabilidadLenguaje(ModeloBase):
    schema = cargar_esquema_json("habilidad_lenguaje.schema.json")
    _columna_de = MAPEO_HABILIDAD_LENGUAJE
    tabla = "habilidades_lenguajes"