from flask import Blueprint, jsonify, request
from api.servicios.servicio_usuario import actualizar_perfil_usuario, obtener_perfil_usuario

usuario_bp = Blueprint("usuario", __name__, url_prefix="/api/usuarios")


@usuario_bp.route("/<int:usuario_id>", methods=["GET"])
def ver_usuario(usuario_id):
    resultado = obtener_perfil_usuario(usuario_id)
    return jsonify(resultado), 200


@usuario_bp.route("/<int:usuario_id>", methods=["PUT"])
def editar_usuario(usuario_id):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "El cuerpo de la petición debe ser un JSON válido"}), 400

    try:
        resultado = actualizar_perfil_usuario(usuario_id, payload)
        return jsonify(resultado), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400