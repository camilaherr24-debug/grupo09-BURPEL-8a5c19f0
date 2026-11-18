# settings.py — Configuración del Proyecto

# Clave secreta para las sesiones de Flask
SECRET_KEY = "clave_secreta_proyecto_2026"

# Configuración de la API del profesor
API_BASE_URL = "https://api-profesor.upso.edu.ar/api/v1"
CLAVE_GRUPO = "grupo09-BURPEL-8a5c19f0"
CABECERAS_API = {
    "Grupo-Access-Key": CLAVE_GRUPO
}

# Configuración de la Base de Datos MySQL
BASE_DATOS = {
    "host": "127.0.0.1",
    "puerto": 3306,
    "usuario": "root",
    "clave": "",
    "nombre_base": "proyecto_informatico"
}