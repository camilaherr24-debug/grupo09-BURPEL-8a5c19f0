from flask import jsonify, request
import pymysql
from pymysql.cursors import DictCursor
from settings import BASE_DATOS, API_BASE_URL, CABECERAS_API
from functools import wraps
from api.servicios.servicio_token import codificar_clave, verificar_clave, generar_token_jwt, verificar_token_jwt
from api.utils.esquemas import ESQUEMA_REGISTRO, ESQUEMA_LOGIN

# ============== DECORADOR: PROTEGER RUTAS ==============
def requiere_token(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token faltante"}), 401
        try:
            tipo, token = auth_header.split(" ")
            if tipo.lower() != "bearer":
                raise ValueError()
            datos_token = verificar_token_jwt(token)
            if not datos_token:
                return jsonify({"error": "Token inválido o expirado"}), 401
            request.usuario_id = datos_token["usuario_id"]
        except:
            return jsonify({"error": "Formato de token incorrecto"}), 401
        return f(*args, **kwargs)
    return decorada

# ============== CONEXIÓN A LA BASE ==============
def conectar_base():
    return pymysql.connect(
        host=BASE_DATOS["host"],
        port=BASE_DATOS["puerto"],
        user=BASE_DATOS["usuario"],
        password=BASE_DATOS["clave"],
        database=BASE_DATOS["nombre_base"],
        cursorclass=DictCursor,
        auth_plugin="mysql_native_password"
    )

# ============== VALIDACIÓN CON ESQUEMA ==============
def validar_esquema(datos, esquema):
    errores = []
    for campo in esquema.get("required", []):
        if campo not in datos:
            errores.append(f"Falta el campo obligatorio: {campo}")
            continue
        regla = esquema["properties"].get(campo, {})
        valor = datos[campo]
        if regla.get("type") == "string" and not isinstance(valor, str):
            errores.append(f"'{campo}' debe ser texto")
        if "minLength" in regla and len(valor) < regla["minLength"]:
            errores.append(f"'{campo}' mínimo {regla['minLength']} caracteres")
        if regla.get("format") == "email" and "@" not in valor:
            errores.append(f"'{campo}' no es un correo válido")
    return errores

# ============== REGISTRAR TODAS LAS RUTAS ==============
def registrar_manejadores(app):

    # --- Registro ---
    @app.route("/api/registro", methods=["POST"])
    def registro():
        datos = request.json
        errores = validar_esquema(datos, ESQUEMA_REGISTRO)
        if errores:
            return jsonify({"errores": errores}), 400

        clave_cod = codificar_clave(datos["password"])

        try:
            db = conectar_base()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)",
                (datos["nombre"], datos["email"], clave_cod)
            )
            db.commit()
            nuevo_id = cursor.lastrowid
            cursor.close()
            db.close()

            token = generar_token_jwt(nuevo_id)
            return jsonify({
                "mensaje": "Usuario registrado correctamente ✅",
                "token": token
            }), 201

        except pymysql.IntegrityError:
            return jsonify({"error": "Ese correo ya está registrado"}), 409

    # --- Login ---
    @app.route("/api/login", methods=["POST"])
    def login():
        datos = request.json
        errores = validar_esquema(datos, ESQUEMA_LOGIN)
        if errores:
            return jsonify({"errores": errores}), 400

        db = conectar_base()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)",
            (datos["nombre"], datos["email"], clave_cod)
        )

        fila = cursor.fetchone()
        cursor.close()
        db.close()

        if not fila:
            return jsonify({"error": "Usuario no encontrado"}), 404
        if not verificar_clave(fila["password_hash"], datos["password"]):
            return jsonify({"error": "Contraseña incorrecta"}), 401

        token = generar_token_jwt(fila["id"])
        return jsonify({
            "mensaje": f"Bienvenido/a {fila['nombre']}",
            "token": token
        }), 200

    # --- Cerrar sesión ---
    @app.route("/api/logout", methods=["GET"])
    def logout():
        return jsonify({"mensaje": "Sesión cerrada correctamente. Olvidá el token del cliente"}), 200

    # --- Tecnologías ---
    @app.route("/api/tecnologias", methods=["GET"])
    def listar_tecnologias():
        import requests
        try:
            resp = requests.get(f"{API_BASE_URL}/tecnologias", headers=CABECERAS_API)
            return jsonify(resp.json()), resp.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 503

    # --- Lenguajes ---
    @app.route("/api/lenguajes", methods=["GET"])
    def listar_lenguajes():
        import requests
        try:
            resp = requests.get(f"{API_BASE_URL}/lenguajes", headers=CABECERAS_API)
            return jsonify(resp.json()), resp.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 503

    # --- Bloquear escritura en catálogos ---
    @app.route("/api/tecnologias", methods=["POST", "PUT", "DELETE"])
    @app.route("/api/tecnologias/<int:id>", methods=["POST", "PUT", "DELETE"])
    def solo_lectura_tec(id=None):
        return jsonify({"error": "Operación no permitida. El catálogo es de solo lectura"}), 405

    @app.route("/api/lenguajes", methods=["POST", "PUT", "DELETE"])
    @app.route("/api/lenguajes/<int:id>", methods=["POST", "PUT", "DELETE"])
    def solo_lectura_len(id=None):
        return jsonify({"error": "Operación no permitida. El catálogo es de solo lectura"}), 405

    # ============== PERFIL PÚBLICO ==============
    @app.route("/api/perfil/<int:usuario_id>", methods=["GET"])
    def ver_perfil_publico(usuario_id):
        db = conectar_base()
        cursor = db.cursor()
        
        cursor.execute("SELECT id, nombre, DATE_FORMAT(fecha_registro, '%d/%m/%Y') as fecha_registro FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            cursor.close()
            db.close()
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        cursor.execute("SELECT * FROM habilidades WHERE usuario_id = %s", (usuario_id,))
        habilidades = cursor.fetchall()
        
        cursor.execute("SELECT id, nombre, descripcion, etapa, fecha_creacion, ultima_actualizacion, fecha_fin, deadline FROM proyectos WHERE usuario_id = %s ORDER BY fecha_creacion DESC", (usuario_id,))
        proyectos = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return jsonify({
            "usuario": usuario,
            "habilidades": habilidades,
            "proyectos": proyectos
        }), 200

    # ============== MIS HABILIDADES ==============
    @app.route("/api/mis-habilidades", methods=["GET"])
    @requiere_token
    def listar_mis_habilidades():
        db = conectar_base()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM habilidades WHERE usuario_id = %s", (request.usuario_id,))
        habilidades = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(habilidades), 200

    @app.route("/api/mis-habilidades", methods=["POST"])
    @requiere_token
    def agregar_habilidad():
        datos = request.json
        if not datos.get("referencia_id") or not datos.get("tipo") or not datos.get("nivel"):
            return jsonify({"error": "Faltan datos: referencia_id, tipo y nivel son obligatorios"}), 400
        if datos["tipo"] not in ["tecnologia", "lenguaje"]:
            return jsonify({"error": "tipo debe ser 'tecnologia' o 'lenguaje'"}), 400
        if datos["nivel"] not in ["básico", "intermedio", "avanzado"]:
            return jsonify({"error": "nivel debe ser: básico, intermedio o avanzado"}), 400
        
        try:
            db = conectar_base()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO habilidades (usuario_id, referencia_id, tipo, nivel)
                VALUES (%s, %s, %s, %s)
            """, (request.usuario_id, datos["referencia_id"], datos["tipo"], datos["nivel"]))
            db.commit()
            nuevo_id = cursor.lastrowid
            cursor.close()
            db.close()
            return jsonify({"mensaje": "Habilidad agregada ✅", "id": nuevo_id}), 201
        except pymysql.IntegrityError:
            return jsonify({"error": "Esa habilidad ya la tenés registrada"}), 409

    @app.route("/api/mis-habilidades/<int:habilidad_id>", methods=["PUT"])
    @requiere_token
    def editar_habilidad(habilidad_id):
        datos = request.json
        if not datos.get("nivel") or datos["nivel"] not in ["básico", "intermedio", "avanzado"]:
            return jsonify({"error": "Nivel inválido"}), 400
        
        db = conectar_base()
        cursor = db.cursor()
        cursor.execute("SELECT id, usuario_id FROM habilidades WHERE id = %s", (habilidad_id,))
        habilidad = cursor.fetchone()
        if not habilidad:
            cursor.close()
            db.close()
            return jsonify({"error": "Habilidad no encontrada"}), 404
        if habilidad["usuario_id"] != request.usuario_id:
            cursor.close()
            db.close()
            return jsonify({"error": "No podés modificar esta habilidad"}), 403
        
        cursor.execute("UPDATE habilidades SET nivel = %s WHERE id = %s", (datos["nivel"], habilidad_id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"mensaje": "Habilidad actualizada ✅"}), 200

    @app.route("/api/mis-habilidades/<int:habilidad_id>", methods=["DELETE"])
    @requiere_token
    def eliminar_habilidad(habilidad_id):
        db = conectar_base()
        cursor = db.cursor()
        cursor.execute("SELECT id, usuario_id FROM habilidades WHERE id = %s", (habilidad_id,))
        habilidad = cursor.fetchone()
        if not habilidad:
            cursor.close()
            db.close()
            return jsonify({"error": "Habilidad no encontrada"}), 404
        if habilidad["usuario_id"] != request.usuario_id:
            cursor.close()
            db.close()
            return jsonify({"error": "No podés eliminar esta habilidad"}), 403
        
        cursor.execute("DELETE FROM habilidades WHERE id = %s", (habilidad_id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"mensaje": "Habilidad eliminada ✅"}), 200

    @app.route("/api/mis-proyectos", methods=["GET"])
    @requiere_token
    def listar_mis_proyectos():
        db = conectar_base()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM proyectos WHERE usuario_id = %s ORDER BY fecha_creacion DESC", (request.usuario_id,))
        proyectos = cursor.fetchall()
        
        for p in proyectos:
            cursor.execute("SELECT lenguaje_id FROM proyecto_lenguajes WHERE proyecto_id = %s", (p["id"],))
            p["lenguajes"] = [row["lenguaje_id"] for row in cursor.fetchall()]
            cursor.execute("SELECT tecnologia_id FROM proyecto_tecnologias WHERE proyecto_id = %s", (p["id"],))
            p["tecnologias"] = [row["tecnologia_id"] for row in cursor.fetchall()]
            cursor.execute("SELECT id, tipo, url FROM links WHERE proyecto_id = %s", (p["id"],))
            p["links"] = cursor.fetchall()
        
        cursor.close()
        db.close()
        return jsonify(proyectos), 200

    @app.route("/api/mis-proyectos", methods=["POST"])
    @requiere_token
    def crear_proyecto():
        datos = request.json
        if not datos.get("nombre") or not datos.get("etapa") or not datos.get("fecha_creacion"):
            return jsonify({"error": "Faltan datos obligatorios: nombre, etapa y fecha_creacion"}), 400
        
        db = conectar_base()
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO proyectos (usuario_id, nombre, descripcion, etapa, fecha_creacion, fecha_fin, deadline)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                request.usuario_id,
                datos["nombre"],
                datos.get("descripcion", ""),
                datos["etapa"],
                datos["fecha_creacion"],
                datos.get("fecha_fin"),
                datos.get("deadline")
            ))
            proyecto_id = cursor.lastrowid
            
            for lang_id in datos.get("lenguajes", []):
                cursor.execute("INSERT INTO proyecto_lenguajes VALUES (%s, %s)", (proyecto_id, lang_id))
            
            for tech_id in datos.get("tecnologias", []):
                cursor.execute("INSERT INTO proyecto_tecnologias VALUES (%s, %s)", (proyecto_id, tech_id))
            
            for link in datos.get("links", []):
                cursor.execute("INSERT INTO links (proyecto_id, tipo, url) VALUES (%s, %s, %s)", 
                             (proyecto_id, link["tipo"], link["url"]))
            
            db.commit()
            return jsonify({"mensaje": "Proyecto creado ✅", "id": proyecto_id}), 201
        except Exception as e:
            db.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            db.close()

    @app.route("/api/mis-proyectos/<int:proyecto_id>", methods=["GET"])
    @requiere_token
    def ver_proyecto(proyecto_id):
        db = conectar_base()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM proyectos WHERE id = %s AND usuario_id = %s", (proyecto_id, request.usuario_id))
        p = cursor.fetchone()
        if not p:
            cursor.close()
            db.close()
            return jsonify({"error": "Proyecto no encontrado"}), 404
        
        cursor.execute("SELECT lenguaje_id FROM proyecto_lenguajes WHERE proyecto_id = %s", (proyecto_id,))
        p["lenguajes"] = [row["lenguaje_id"] for row in cursor.fetchall()]
        cursor.execute("SELECT tecnologia_id FROM proyecto_tecnologias WHERE proyecto_id = %s", (proyecto_id,))
        p["tecnologias"] = [row["tecnologia_id"] for row in cursor.fetchall()]
        cursor.execute("SELECT id, tipo, url FROM links WHERE proyecto_id = %s", (proyecto_id,))
        p["links"] = cursor.fetchall()
        
        cursor.close()
        db.close()
        return jsonify(p), 200

    @app.route("/api/mis-proyectos/<int:proyecto_id>", methods=["PUT"])
    @requiere_token
    def editar_proyecto(proyecto_id):
        datos = request.json
        if not datos.get("nombre") or not datos.get("etapa"):
            return jsonify({"error": "Nombre y etapa son obligatorios"}), 400
        
        db = conectar_base()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM proyectos WHERE id = %s AND usuario_id = %s", (proyecto_id, request.usuario_id))
        if not cursor.fetchone():
            cursor.close()
            db.close()
            return jsonify({"error": "Proyecto no encontrado"}), 404
        
        try:
            cursor.execute("""
                UPDATE proyectos 
                SET nombre = %s, descripcion = %s, etapa = %s, fecha_fin = %s, deadline = %s, ultima_actualizacion = CURDATE()
                WHERE id = %s AND usuario_id = %s
            """, (
                datos["nombre"],
                datos.get("descripcion", ""),
                datos["etapa"],
                datos.get("fecha_fin"),
                datos.get("deadline"),
                proyecto_id,
                request.usuario_id
            ))
            db.commit()
            return jsonify({"mensaje": "Proyecto actualizado ✅"}), 200
        except Exception as e:
            db.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            db.close()

    @app.route("/api/mis-proyectos/<int:proyecto_id>", methods=["DELETE"])
    @requiere_token
    def eliminar_proyecto(proyecto_id):
        db = conectar_base()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM proyectos WHERE id = %s AND usuario_id = %s", (proyecto_id, request.usuario_id))
        if not cursor.fetchone():
            cursor.close()
            db.close()
            return jsonify({"error": "Proyecto no encontrado"}), 404
        
        cursor.execute("DELETE FROM proyectos WHERE id = %s AND usuario_id = %s", (proyecto_id, request.usuario_id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"mensaje": "Proyecto eliminado ✅"}), 200