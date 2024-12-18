from database.db_connection import conectar_bd
import hashlib
import mysql.connector

def hash_password(password):
    """
    Genera un hash SHA-256 de la contraseña.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """
    Registra un nuevo usuario en la base de datos.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conexion.commit()
        return "Usuario registrado correctamente."
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conexion.close()

def login_user(username, password):
    """
    Verifica las credenciales de un usuario.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    hashed_pw = hash_password(password)
    try:
        cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username, hashed_pw))
        user = cursor.fetchone()
        return user if user else None
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conexion.close()
