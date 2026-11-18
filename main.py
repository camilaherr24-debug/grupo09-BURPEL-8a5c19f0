from flask import Flask, send_from_directory
from flask_cors import CORS
from settings import SECRET_KEY
from api.manejadores import registrar_manejadores

app = Flask(__name__, static_folder=".")
CORS(app)
app.secret_key = SECRET_KEY

# Páginas HTML
@app.route("/")
def inicio():
    return send_from_directory(".", "index.html")

@app.route("/registro")
def pagina_registro():
    return send_from_directory(".", "registro.html")

@app.route("/login")
def pagina_login():
    return send_from_directory(".", "login.html")

@app.route("/tecnologias")
def pagina_tecnologias():
    return send_from_directory(".", "tecnologias.html")

@app.route("/lenguajes")
def pagina_lenguajes():
    return send_from_directory(".", "lenguajes.html")

# Registrar todas las rutas
registrar_manejadores(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)