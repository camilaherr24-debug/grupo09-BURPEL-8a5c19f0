from jsonschema import ValidationError, validate


def validar_contra_schema(datos, schema):
    try:
        validate(instance=datos, schema=schema)
    except ValidationError as err:
        raise ValueError(f"Error de validación: {err.message}")
    return datos