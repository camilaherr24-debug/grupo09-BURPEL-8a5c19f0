# api/esquemas.py — Validación con JSON Schema

ESQUEMA_REGISTRO = {
    "type": "object",
    "properties": {
        "nombre": {
            "type": "string",
            "minLength": 2,
            "description": "Nombre del usuario"
        },
        "email": {
            "type": "string",
            "format": "email",
            "description": "Correo electrónico"
        },
        "password": {
            "type": "string",
            "minLength": 6,
            "description": "Contraseña mínima 6 caracteres"
        }
    },
    "required": ["nombre", "email", "password"],
    "additionalProperties": False
}

ESQUEMA_LOGIN = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 6
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}