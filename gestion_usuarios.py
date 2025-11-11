from datetime import datetime
from mysql.connector import Error
from config_conexiones import obtener_conexion_mysql, obtener_bd_mongo
from seguridad_utils import generar_hash, verificar_clave, leer_clave, validar_username, validar_email, validar_clave_texto

def registrar_log(usuario_id, accion, detalle=""):
    bd = obtener_bd_mongo()
    if bd is None:
        return
    coleccion = bd["logs_login"]
    doc = {
        "usuario_id": usuario_id,
        "accion": accion,
        "detalle": detalle,
        "fecha": datetime.utcnow()
    }
    try:
        coleccion.insert_one(doc)
    except Exception:
        pass

def crear_tabla_si_no_existe():
    conexion = obtener_conexion_mysql()
    if conexion is None:
        return
    sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        email VARCHAR(100) UNIQUE,
        password_hash VARCHAR(255),
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        activo BOOLEAN DEFAULT TRUE,
        rol VARCHAR(20) DEFAULT 'usuario'
    )
    """
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()
    cursor.close()
    conexion.close()

def registrar_usuario():
    conexion = obtener_conexion_mysql()
    if conexion is None:
        print("No se pudo conectar a MySQL.")
        return
    username = input("Nombre de usuario: ").strip()
    email = input("Email: ").strip()
    clave = leer_clave("Contraseña: ")
    clave_conf = leer_clave("Confirmar contraseña: ")
    if not validar_username(username):
        print("Usuario inválido.")
        conexion.close()
        return
    if not validar_email(email):
        print("Email inválido.")
        conexion.close()
        return
    if clave != clave_conf or not validar_clave_texto(clave):
        print("Contraseña inválida.")
        conexion.close()
        return
    clave_hash = generar_hash(clave)
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, clave_hash)
        )
        conexion.commit()
        usuario_id = cursor.lastrowid
        bd = obtener_bd_mongo()
        if bd is not None:
            bd["usuarios"].insert_one(
                {
                    "mysql_id": usuario_id,
                    "username": username,
                    "email": email,
                    "password_hash": clave_hash,
                    "fecha_registro": datetime.utcnow(),
                    "activo": True,
                    "rol": "usuario"
                }
            )
        registrar_log(usuario_id, "registro", "usuario creado")
        print("Usuario registrado correctamente.")
    except Error as e:
        print("Error al registrar:", e)
    finally:
        cursor.close()
        conexion.close()

def buscar_usuario_por_username(username):
    conexion = obtener_conexion_mysql()
    if conexion is None:
        return None
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()
    return fila

def iniciar_sesion():
    username = input("Usuario: ").strip()
    clave = leer_clave("Contraseña: ")
    datos = buscar_usuario_por_username(username)
    if datos is None:
        print("Usuario no encontrado.")
        registrar_log(None, "login_fallido", "usuario inexistente")
        return None
    if not datos.get("activo", True):
        print("Usuario inactivo.")
        registrar_log(datos["id"], "login_fallido", "usuario inactivo")
        return None
    if not verificar_clave(clave, datos.get("password_hash")):
        print("Contraseña incorrecta.")
        registrar_log(datos["id"], "login_fallido", "clave incorrecta")
        return None
    registrar_log(datos["id"], "login_exitoso", "")
    print("Inicio de sesión exitoso.")
    return datos

def mostrar_datos_usuario(usuario):
    print("\nDatos del usuario")
    print("ID:", usuario["id"])
    print("Usuario:", usuario["username"])
    print("Email:", usuario["email"])
    print("Fecha registro:", usuario["fecha_registro"])
    estado = "Activo" if usuario.get("activo", True) else "Inactivo"
    print("Estado:", estado)
    print("Rol:", usuario.get("rol", "usuario"))

def actualizar_perfil(usuario_actual):
    conexion = obtener_conexion_mysql()
    if conexion is None:
        print("No se pudo conectar a MySQL.")
        return usuario_actual
    print("\n1. Cambiar email")
    print("2. Cambiar contraseña")
    opcion = input("Opción: ")
    cursor = conexion.cursor(dictionary=True)
    if opcion == "1":
        nuevo_email = input("Nuevo email: ").strip()
        if not validar_email(nuevo_email):
            print("Email inválido.")
        else:
            try:
                cursor.execute("UPDATE usuarios SET email=%s WHERE id=%s", (nuevo_email, usuario_actual["id"]))
                conexion.commit()
                usuario_actual["email"] = nuevo_email
                registrar_log(usuario_actual["id"], "editar_perfil", "cambio de email")
                print("Email actualizado.")
            except Error as e:
                print("Error al actualizar:", e)
    elif opcion == "2":
        clave_actual = leer_clave("Contraseña actual: ")
        if not verificar_clave(clave_actual, usuario_actual.get("password_hash")):
            print("Contraseña actual incorrecta.")
        else:
            nueva = leer_clave("Nueva contraseña: ")
            conf = leer_clave("Confirmar nueva contraseña: ")
            if nueva != conf or not validar_clave_texto(nueva):
                print("Contraseña inválida.")
            else:
                nuevo_hash = generar_hash(nueva)
                try:
                    cursor.execute("UPDATE usuarios SET password_hash=%s WHERE id=%s", (nuevo_hash, usuario_actual["id"]))
                    conexion.commit()
                    usuario_actual["password_hash"] = nuevo_hash
                    registrar_log(usuario_actual["id"], "editar_perfil", "cambio de contraseña")
                    print("Contraseña actualizada.")
                except Error as e:
                    print("Error al actualizar:", e)
    cursor.close()
    conexion.close()
    return usuario_actual

def recuperar_contrasena():
    conexion = obtener_conexion_mysql()
    if conexion is None:
        print("No se pudo conectar a MySQL.")
        return
    username = input("Usuario: ").strip()
    email = input("Email registrado: ").strip()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username=%s AND email=%s", (username, email))
    fila = cursor.fetchone()
    if fila is None:
        print("Datos no coinciden.")
        registrar_log(None, "recuperacion_fallida", "usuario o email inválido")
    else:
        nueva = "1234"
        nuevo_hash = generar_hash(nueva)
        cursor.execute("UPDATE usuarios SET password_hash=%s WHERE id=%s", (nuevo_hash, fila["id"]))
        conexion.commit()
        registrar_log(fila["id"], "recuperar_contrasena", "se asignó clave temporal")
        print("Se asignó una nueva contraseña temporal: 1234")
    cursor.close()
    conexion.close()

def mostrar_logs_usuario(usuario_id):
    bd = obtener_bd_mongo()
    if bd is None:
        print("MongoDB no disponible.")
        return
    coleccion = bd["logs_login"]
    registros = list(coleccion.find({"usuario_id": usuario_id}).sort("fecha", -1))
    if not registros:
        print("Sin registros.")
        return
    for r in registros:
        fecha = r.get("fecha")
        accion = r.get("accion")
        detalle = r.get("detalle", "")
        print(fecha, "-", accion, "-", detalle)

def listar_todos_usuarios():
    conexion = obtener_conexion_mysql()
    if conexion is None:
        print("No se pudo conectar a MySQL.")
        return
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, rol, activo FROM usuarios")
    filas = cursor.fetchall()
    print("\nUsuarios registrados:")
    if not filas:
        print("No hay usuarios.")
    for f in filas:
        estado = "Activo" if f["activo"] else "Inactivo"
        print(f"{f['id']} - {f['username']} - {f['email']} - {f['rol']} - {estado}")
    cursor.close()
    conexion.close()
