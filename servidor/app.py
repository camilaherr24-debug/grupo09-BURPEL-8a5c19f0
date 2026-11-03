from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='../')
CORS(app)

# Datos de la API del profesor
API_BASE = "https://api-profesor.upso.edu.ar/api/v1"
ACCESS_KEY = "grupo09-BURPEL-8a5c19f0"

# Cabecera que se envía en cada solicitud
CABECERAS = {
    "Grupo-Access-Key": ACCESS_KEY
}

# ------------------------------
# Páginas del frontend
# ------------------------------
@app.route('/')
def inicio():
    return send_from_directory('../', 'index.html')

@app.route('/tecnologias')
def tecnologias():
    return send_from_directory('../', 'tecnologias.html')

@app.route('/lenguajes')
def lenguajes():
    return send_from_directory('../', 'lenguajes.html')

# ------------------------------
# Endpoints que conectan con la API
# ------------------------------
@app.route('/api/tecnologias', methods=['GET'])
def listar_tecnologias():
    try:
        respuesta = requests.get(f"{API_BASE}/tecnologias", headers=CABECERAS)
        return jsonify(respuesta.json()), respuesta.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/lenguajes', methods=['GET'])
def listar_lenguajes():
    try:
        respuesta = requests.get(f"{API_BASE}/lenguajes", headers=CABECERAS)
        return jsonify(respuesta.json()), respuesta.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------
# Archivos estáticos (estilo, js, etc.)
# ------------------------------
@app.route('/<nombre_archivo>')
def archivos_estaticos(nombre_archivo):
    return send_from_directory('../', nombre_archivo)

if __name__ == '__main__':
    app.run(debug=True)