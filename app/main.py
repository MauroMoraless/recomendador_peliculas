import sys
import os
import pandas as pd
import streamlit as st

# Agregar los directorios de scripts y database al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

# Importar módulos necesarios
from scripts.feedback_handler import guardar_feedback
from recommend import recomendar_pelicula

# Cargar el dataset con clusters (no reentrenar)
dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "tmdb_2023_movies_clustered.csv"))
df = pd.read_csv(dataset_path)

# Función para obtener la URL completa del póster
def obtener_poster_local(poster_path):
    base_url = "https://image.tmdb.org/t/p/w500"  # URL base de TMDb para imágenes
    if pd.notna(poster_path) and poster_path.startswith("/"):
        return f"{base_url}{poster_path}"
    return None

# Título de la aplicación
st.title("Recomendador de Películas TMDb")

# Inicializar el estado de la recomendación
if 'recomendacion' not in st.session_state:
    st.session_state['recomendacion'] = None

# Entrada del título de la película
titulo_usuario = st.selectbox("Ingrese el título de una película:", df.title.unique())

if st.button("Recomendar"):
    recomendacion = recomendar_pelicula(titulo_usuario, df)
    
    if isinstance(recomendacion, str):  # Si no se encuentra la película
        st.error(recomendacion)
    else:
        pelicula_recomendada = recomendacion[0]
        st.write(f"**Película recomendada:** {pelicula_recomendada}")
        
        # Obtener y mostrar la imagen del póster
        poster_path = df[df['title'] == pelicula_recomendada]['poster_path'].iloc[0]
        poster_url = obtener_poster_local(poster_path)
        
        if poster_url:
            st.markdown(
                f'<img src="{poster_url}" alt="{pelicula_recomendada}" style="width:300px;"/>',
                unsafe_allow_html=True
            )
        else:
            st.write("No se encontró el póster de la película.")

        # Feedback del usuario
        feedback = st.radio("¿Te gustó la recomendación?", ("buena", "mala"))
        if st.button("Guardar Feedback"):
            guardar_feedback("anonimo", titulo_usuario, pelicula_recomendada, feedback)
            st.success("¡Feedback guardado! Gracias por tu colaboración.")
