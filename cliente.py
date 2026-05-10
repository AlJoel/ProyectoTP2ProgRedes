import requests

URL_BASE = "http://localhost:5000"


def registrar_usuario():
    usuario = input("Ingrese usuario: ")
    contrasena = input("Ingrese contraseña: ")

    datos = {
        "usuario": usuario,
        "contrasena": contrasena
    }

    respuesta = requests.post(f"{URL_BASE}/registro", json=datos)
    print(respuesta.json())


def iniciar_sesion():
    usuario = input("Ingrese usuario: ")
    contrasena = input("Ingrese contraseña: ")

    datos = {
        "usuario": usuario,
        "contrasena": contrasena
    }

    respuesta = requests.post(f"{URL_BASE}/login", json=datos)
    print(respuesta.json())


def ver_tareas():
    respuesta = requests.get(f"{URL_BASE}/tareas")

    if respuesta.status_code == 200:
        print(respuesta.text)
    else:
        print(respuesta.json())


def cerrar_sesion():
    respuesta = requests.post(f"{URL_BASE}/logout")
    print(respuesta.json())


def menu():
    while True:
        print("\n--- Cliente del Sistema de Tareas ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver página de tareas")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            cerrar_sesion()
            print("Saliendo...")
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()
