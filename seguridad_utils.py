import bcrypt
import getpass

def generar_hash(clave):
    clave_bytes = clave.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(clave_bytes, salt).decode("utf-8")

def verificar_clave(clave_plana, clave_hash):
    if not clave_hash:
        return False
    return bcrypt.checkpw(clave_plana.encode("utf-8"), clave_hash.encode("utf-8"))

def leer_clave(texto="Contraseña: "):
    return getpass.getpass(texto)

def validar_username(username):
    username = username.strip()
    return len(username) >= 3

def validar_email(email):
    email = email.strip()
    return "@" in email and "." in email and len(email) >= 5

def validar_clave_texto(clave):
    return len(clave) >= 4
