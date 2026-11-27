from api.models.base import ModeloBase
from api.models.usuario.usuario_mapping import MAPEO_USUARIO
from api.utils.esquemas import cargar_esquema_json


class Usuario(ModeloBase):
    schema = cargar_esquema_json("usuario.schema.json")
    _columna_de = MAPEO_USUARIO
    tabla = "usuarios"