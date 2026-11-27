from api.models.base import ModeloBase
from api.models.tecnologia.tecnologia_mapping import MAPEO_TECNOLOGIA
from api.utils.esquemas import cargar_esquema_json

class Tecnologia(ModeloBase):
    schema = cargar_esquema_json("tecnologia.schema.json")
    _columna_de = MAPEO_TECNOLOGIA
    tabla = "tecnologias"