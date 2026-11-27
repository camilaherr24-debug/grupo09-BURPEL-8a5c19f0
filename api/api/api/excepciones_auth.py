# api/excepciones_auth.py — Errores personalizados

class CredencialesInvalidasError(Exception):
    codigo = 401
    mensaje = "Credenciales inválidas"

class TokenInvalidoError(Exception):
    codigo = 401
    mensaje = "Token inválido o expirado"

class AccesoDenegadoError(Exception):
    codigo = 403
    mensaje = "No tenés permiso para acceder a este recurso"

class IdInexistenteError(Exception):
    codigo = 404
    mensaje = "El recurso no existe"

class ColumnaDuplicadaError(Exception):
    codigo = 409
    mensaje = "Registro duplicado"