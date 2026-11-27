from api.utils.esquemas import cargar_esquema_json
from api.utils.validacion import validar_contra_schema

SCHEMA_USUARIO = cargar_esquema_json("usuario.schema.json")


def obtener_perfil_usuario(usuario_id):
    # TODO: buscar usuario por ID usando Usuario y devolver datos públicos (sin password)
    return {
        "mensaje": "Consulta de perfil lista para conectar a la base de datos",
        "id": usuario_id,
    }


def actualizar_perfil_usuario(usuario_id, datos):
    datos_validados = validar_contra_schema(datos, SCHEMA_USUARIO)
    # TODO: actualizar registro en tabla de usuarios usando Usuario y el mapeo
    return {
        "mensaje": "Datos de usuario validados correctamente",
        "id": usuario_id,
        "usuario": {
            "nombre": datos_validados["nombre"],
            "email": datos_validados["email"],
        },
    }