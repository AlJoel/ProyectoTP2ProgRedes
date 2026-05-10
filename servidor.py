from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

DB_FILE = "tareas.db"

app = Flask(__name__)

# Se me ocurrió utilizar un objeto para almacenar las sesiones activas con el fin de dar un poco de seguridad a la API
# Se almacena IP y Usuario, para verificar si existe al menos una sesión iniciada en la pc que está haciendo la llamada.
# Formato: { "ip_cliente": "usuario" }
sesiones_iniciadas = {}

def conectar_db():
    return sqlite3.connect(DB_FILE)

def inicializar_db():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    ''')

    conexion.commit()
    conexion.close()


def obtener_ip_cliente():
    return request.remote_addr

@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()

    if not datos:
        return jsonify({"mensaje": "No se recibieron datos"}), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"mensaje": "Faltan datos"}), 400

    contrasena_hasheada = generate_password_hash(contrasena)

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
            (usuario, contrasena_hasheada)
        )
        conexion.commit()
        conexion.close()

        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"mensaje": "El usuario ya existe"}), 400


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()

    if not datos:
        return jsonify({"mensaje": "No se recibieron datos"}), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"mensaje": "Faltan datos"}), 400

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conexion.close()

    if resultado and check_password_hash(resultado[0], contrasena):
        ip_cliente = obtener_ip_cliente()
        sesiones_iniciadas[ip_cliente] = usuario

        return jsonify({
            "mensaje": "Inicio de sesión correcto",
            "usuario": usuario,
            "ip": ip_cliente
        }), 200
    else:
        return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401


@app.route("/logout", methods=["POST"])
def logout():
    ip_cliente = obtener_ip_cliente()

    if ip_cliente in sesiones_iniciadas:
        usuario = sesiones_iniciadas[ip_cliente]
        del sesiones_iniciadas[ip_cliente]
        return jsonify({"mensaje": f"Sesión cerrada para el usuario {usuario}"}), 200

    return jsonify({"mensaje": "No había una sesión iniciada para esta IP"}), 400


@app.route("/tareas", methods=["GET"])
def tareas():
    ip_cliente = obtener_ip_cliente()

    if ip_cliente not in sesiones_iniciadas:
        return jsonify({"mensaje": "Acceso denegado. Primero debe iniciar sesión."}), 401

    usuario = sesiones_iniciadas[ip_cliente]

    return f"""
    <html>
        <head>
            <title>Sistema de Tareas</title>
        </head>
        <body>
            <h1>Bienvenido al sistema de gestión de tareas</h1>
            <p>Usuario con sesión iniciada: {usuario}</p>
            <p>IP registrada: {ip_cliente}</p>
            <h2>Tareas disponibles</h2>
            <ul>
                <li>1 - Estudiar sockets</li>
                <li>2 - Terminar TP de redes</li>
                <li>3 - Probar API REST</li>
            </ul>
        </body>
    </html>
    """


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({"mensaje": "Servidor funcionando"})


if __name__ == "__main__":
    # Al levantar el servidor, la variable de sesiones arranca vacía para que que no quede ninguna sesión anterior guardada.
    sesiones_iniciadas.clear()
    inicializar_db()
    app.run(debug=True, port=5000)
