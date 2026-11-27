from werkzeug.security import check_password_hash, generate_password_hash
from api.utils.esquemas import cargar_esquema_json
from api.utils.validacion import validar_contra_schema

SCHEMA_REGISTRO = cargar_esquema_json("usuario_registro.schema.json")
SCHEMA_LOGIN = cargar_esquema_json("usuario_login.schema.json")
SCHEMA_CAMBIO_PASSWORD = cargar_esquema_json("cambio_password.schema.json")


def hashear_password(password_plana):
    return generate_password_hash(password_plana)


def verificar_password(password_plana, password_hash):
    return check_password_hash(password_hash, password_plana)


def registrar_usuario(datos):
    datos_validados = validar_contra_schema(datos, SCHEMA_REGISTRO)
    password_hash = hashear_password(datos_validados["password"])
    # verificar si ya existe el email y guardar password_hash con Usuario
    return {
        "mensaje": "Usuario validado y contraseña hasheada correctamente",
        "usuario": {
            "nombre": datos_validados["nombre"],
            "email": datos_validados["email"],
        },
        "password_hash_preview": password_hash[:20] + "...",
    }


def iniciar_sesion(datos):
    datos_validados = validar_contra_schema(datos, SCHEMA_LOGIN)
    # buscar usuario en BD por email y usar verificar_password(datos_validados["password"], usuario.password_hash)
    return {
        "mensaje": "Datos de login validados correctamente",
        "email": datos_validados["email"],
    }


def cambiar_password(datos, password_hash_actual=None):
    datos_validados = validar_contra_schema(datos, SCHEMA_CAMBIO_PASSWORD)

    if password_hash_actual and not verificar_password(
        datos_validados["password_actual"], password_hash_actual
    ):
        raise ValueError("La contraseña actual no es correcta")

    nueva_password_hash = hashear_password(datos_validados["password_nueva"])
    # actualizar password_hash del usuario en la BD
    return {
        "mensaje": "Contraseña actualizada correctamente",
        "password_hash_preview": nueva_password_hash[:20] + "...",
    }