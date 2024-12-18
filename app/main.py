import sys
import os
import pandas as pd
import streamlit as st
from scripts.feedback_handler import guardar_feedback
from recommend import recomendar_pelicula, comparar_peliculas, comparar_generos, comparar_descripcion


# Agregar los directorios de scripts y database al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

# Cargar el dataset con clusters 
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
    pelicula_recomendada = recomendacion[0]
    
    if isinstance(recomendacion, str):  # Si no se encuentra la película
        st.error(recomendacion)
    else:
        st.write(f"### **Película recomendada:** {pelicula_recomendada}")
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
        
        # Comparar películas
        comparacion = comparar_peliculas(df, titulo_usuario, pelicula_recomendada)
        similitud_generos = comparar_generos(df, titulo_usuario, pelicula_recomendada)
        similitud_descripcion = comparar_descripcion(df, titulo_usuario, pelicula_recomendada)

        # Mostrar análisis descriptivo
        st.write("### Comparación entre las Películas:")
        st.write(f"- **Similitud de Géneros:** {similitud_generos} (100% significa géneros idénticos)")
        st.write(f"- **Similitud de Descripción:** {similitud_descripcion * 100:.0f}%")
        st.write("#### Comparación de Características:")
        for feature, diferencia in comparacion['diferencias_caracteristicas'].items():
            if feature == "vote_average":
                st.write(f"- **Calificación promedio**: La película recomendada tiene un puntaje {'más alto' if diferencia > 0 else 'más bajo'} en promedio.")
            elif feature == "vote_count":
                st.write(f"- **Cantidad de votos**: La recomendada tiene {'más votos' if diferencia > 0 else 'menos votos'}.")
            elif feature == "popularity":
                st.write(f"- **Popularidad**: Es {'más popular' if diferencia > 0 else 'menos popular'}.")
            elif feature == "runtime":
                st.write(f"- **Duración**: Tiene una duración {'más larga' if diferencia > 0 else 'más corta'} por {abs(diferencia)} minutos.")


        # Feedback del usuario
        feedback = st.radio("¿Te gustó la recomendación?", ("buena", "mala"))
        if st.button("Guardar Feedback"):
            guardar_feedback("anonimo", titulo_usuario, pelicula_recomendada, feedback)
            st.success("¡Feedback guardado! Gracias por tu colaboración.")
