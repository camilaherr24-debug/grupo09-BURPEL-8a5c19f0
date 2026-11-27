from api.models.base import ModeloBase
from api.models.habilidad_tecnologia.habilidad_tecnologia_mapping import MAPEO_HABILIDAD_TECNOLOGIA
from api.utils.esquemas import cargar_esquema_json

class HabilidadTecnologia(ModeloBase):
    schema = cargar_esquema_json("habilidad_tecnologia.schema.json")
    _columna_de = MAPEO_HABILIDAD_TECNOLOGIA
    tabla = "habilidades_tecnologias"