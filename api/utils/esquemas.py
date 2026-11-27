# api/esquemas.py — Validación con JSON Schema
import json
from pathlib import Path

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

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"


def cargar_esquema_json(nombre_archivo):
    ruta = SCHEMAS_DIR / nombre_archivo
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el esquema JSON: {ruta}")
    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)