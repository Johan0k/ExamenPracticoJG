import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient

load_dotenv()

def obtener_conexion_mysql():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print("Error de conexión MySQL:", e)
    return None

def obtener_bd_mongo():
    uri = os.getenv("MONGO_URI")
    if not uri:
        return None
    try:
        cliente = MongoClient(uri, tls=True)
        bd = cliente["examen_autenticacion"]
        return bd
    except Exception as e:
        print("Error de conexión MongoDB:", e)
        return None
