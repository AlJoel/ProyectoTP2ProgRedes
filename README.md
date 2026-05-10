# PFO 2 - Sistema de Gestión de Tareas con API y Base de Datos

Este proyecto implementa una API REST básica usando Flask y SQLite. Permite registrar usuarios, iniciar sesión y acceder a una página de tareas solo si existe una sesión iniciada para la IP del cliente.
Para el almacenado de contraseñas seguras implementamos hasheo con la librería Werkzeug

## Archivos del proyecto

- "servidor.py": contiene la API Flask, la conexión con SQLite, el registro, el login, el logout y el listado de las tareas.
- "cliente.py": cliente de consola para interactuar con el servidor.
- "requirements.txt": librerías necesarias para ejecutar el proyecto.

## Instalación

Primero instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

En una terminal ejecutar el servidor:

```bash
python servidor.py
```

En otra terminal ejecutar el cliente:

```bash
python cliente.py
```

## Endpoints

### POST /registro

Registra un usuario nuevo.

Ejemplo de JSON:

```json
{
  "usuario": "usuario",
  "contrasena": "1234"
}
```

La contraseña no se guarda en texto plano. Se guarda hasheada usando `generate_password_hash`.

### POST /login

Verifica usuario y contraseña. Si los datos son correctos, se crea una sesión simple en memoria asociada a la IP del cliente.

Ejemplo de JSON:

```json
{
  "usuario": "usuario",
  "contrasena": "1234"
}
```

### GET /tareas

Muestra una página HTML de bienvenida. Esta ruta solo permite el acceso si la IP del cliente tiene una sesión iniciada.

Si no hay sesión iniciada, devuelve un mensaje de acceso denegado.

### POST /logout

Cierra la sesión de la IP actual. En el cliente de consola se ejecuta automáticamente cuando se elige la opción "4. Salir".

## "Sesiones"

El servidor usa una variable llamada "sesiones_iniciadas", que es un diccionario en memoria.

Ejemplo:

```python
sesiones_iniciadas = {
    "127.0.0.1": "usuario"
}
```

Esto permite saber si una IP tiene una sesión iniciada y a qué usuario corresponde.

Cuando el servidor se reinicia, esta variable queda vacía, por lo que no se conservan sesiones anteriores.

