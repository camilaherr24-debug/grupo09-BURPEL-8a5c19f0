from flask import Flask, render_template
from flask_cors import CORS
from settings import SECRET_KEY
from api.manejadores import registrar_manejadores

app = Flask(__name__)
CORS(app)
app.secret_key = SECRET_KEY

# Páginas HTML
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/registro")
def pagina_registro():
    return render_template("registro.html")

@app.route("/login")
def pagina_login():
    return render_template("login.html")

@app.route("/tecnologias")
def pagina_tecnologias():
    return render_template("tecnologias.html")

@app.route("/lenguajes")
def pagina_lenguajes():
    return render_template("lenguajes.html")

# Registrar todas las rutas
registrar_manejadores(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)