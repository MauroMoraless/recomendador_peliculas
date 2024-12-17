from database.db_connection import conectar_bd

def guardar_feedback(username, pelicula_ingresada, pelicula_recomendada, feedback):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feedback_recomendaciones 
            (username, pelicula_ingresada, pelicula_recomendada, feedback) 
            VALUES (%s, %s, %s, %s)
        """, (username, pelicula_ingresada, pelicula_recomendada, feedback))
        conn.commit()
        conn.close()
        print("Feedback guardado correctamente.")
    except Exception as e:
        print(f"Error al guardar el feedback: {e}")