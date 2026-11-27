from flask import Blueprint, jsonify, request
# Acá tu compañera te dice cómo importar el servicio

tecnologias_bp = Blueprint("tecnologias", __name__, url_prefix="/api/tecnologias")

@tecnologias_bp.route("/", methods=["GET"])
def listar():
    return jsonify({"mensaje": "Lista de tecnologías"}), 200

@tecnologias_bp.route("/", methods=["POST"])
def crear():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "JSON inválido"}), 400
    return jsonify({"mensaje": "Tecnología recibida", "datos": payload}), 201