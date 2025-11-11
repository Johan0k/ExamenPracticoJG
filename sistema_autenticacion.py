from gestion_usuarios import (
    crear_tabla_si_no_existe,
    registrar_usuario,
    iniciar_sesion,
    mostrar_datos_usuario,
    actualizar_perfil,
    recuperar_contrasena,
    mostrar_logs_usuario,
    listar_todos_usuarios
)

def menu_principal():
    crear_tabla_si_no_existe()
    usuario_actual = None
    while True:
        if usuario_actual is None:
            print("\nSISTEMA DE AUTENTICACIÓN")
            print("1. Registrarse")
            print("2. Iniciar sesión")
            print("3. Recuperar contraseña")
            print("4. Salir")
            opcion = input("Opción: ")
            if opcion == "1":
                registrar_usuario()
            elif opcion == "2":
                usuario_actual = iniciar_sesion()
            elif opcion == "3":
                recuperar_contrasena()
            elif opcion == "4":
                print("Fin del programa.")
                break
            else:
                print("Opción inválida.")
        else:
            print("\nMENÚ PRINCIPAL")
            print("1. Ver perfil")
            print("2. Editar perfil")
            print("3. Ver actividad de login")
            if usuario_actual.get("rol") == "admin":
                print("4. Ver todos los usuarios (admin)")
                print("5. Cerrar sesión")
            else:
                print("4. Cerrar sesión")
            opcion = input("Opción: ")
            if opcion == "1":
                mostrar_datos_usuario(usuario_actual)
            elif opcion == "2":
                usuario_actual = actualizar_perfil(usuario_actual)
            elif opcion == "3":
                mostrar_logs_usuario(usuario_actual["id"])
            else:
                if usuario_actual.get("rol") == "admin" and opcion == "4":
                    listar_todos_usuarios()
                elif usuario_actual.get("rol") == "admin" and opcion == "5":
                    usuario_actual = None
                    print("Sesión cerrada.")
                elif usuario_actual.get("rol") != "admin" and opcion == "4":
                    usuario_actual = None
                    print("Sesión cerrada.")
                else:
                    print("Opción inválida.")

if __name__ == "__main__":
    menu_principal()
