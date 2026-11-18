from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from settings import SECRET_KEY

def codificar_clave(clave_plana: str) -> str:
    """Convierte la contraseña a un código seguro para guardar"""
    return generate_password_hash(clave_plana)

def verificar_clave(clave_guardada: str, clave_ingresada: str) -> bool:
    """Compara la contraseña ingresada con la guardada"""
    return check_password_hash(clave_guardada, clave_ingresada)

# 👇 Agregá estas dos funciones nuevas acá abajo

def generar_token_jwt(usuario_id: int) -> str:
    """Crea un token JWT que dura 24 horas"""
    payload = {
        "usuario_id": usuario_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verificar_token_jwt(token: str) -> dict | None:
    """Verifica que el token sea válido y no expiró"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None