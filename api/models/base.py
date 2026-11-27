from api.utils.validacion import validar_contra_schema


class ModeloBase:
    schema = None
    _columna_de = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.schema is None or cls._columna_de is None:
            raise NotImplementedError(
                f"{cls.__name__} debe definir 'schema' y '_columna_de'"
            )

        props = cls.schema["properties"]
        cls._campos = list(props)
        cls._campos_salida = [
            c for c in cls._campos if not props[c].get("writeOnly", False)
        ]
        cls._columnas_select = ", ".join(
            ["id"] + [cls._columna_de[c] for c in cls._campos_salida]
        )

        if set(cls._campos) != set(cls._columna_de):
            raise ValueError(
                f"{cls.__name__}: los campos del schema {sorted(cls._campos)} "
                f"no coinciden con los del mapeo {sorted(cls._columna_de)}"
            )

    @classmethod
    def validar(cls, datos):
        return validar_contra_schema(datos, cls.schema)

    def __init__(self, fila_dict):
        self._id = fila_dict["id"]
        self._datos = {
            campo: fila_dict[self._columna_de[campo]]
            for campo in cls_campos_salida(self)
        }

    def to_json(self):
        return {"id": self._id, **self._datos}


def cls_campos_salida(instancia):
    return instancia.__class__._campos_salida