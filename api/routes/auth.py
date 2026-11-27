from flask import Blueprint, jsonify, request
from api.servicios.servicio_auth import iniciar_sesion, registrar_usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/registro", methods=["POST"])
def registro():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "El cuerpo de la petición debe ser un JSON válido"}), 400

    try:
        resultado = registrar_usuario(payload)
        return jsonify(resultado), 201
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "El cuerpo de la petición debe ser un JSON válido"}), 400

    try:
        resultado = iniciar_sesion(payload)
        return jsonify(resultado), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 401