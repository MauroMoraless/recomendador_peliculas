import pandas as pd
from scipy.spatial.distance import hamming
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

def recomendar_pelicula(titulo_usuario, df):
    """
    Recomienda una película basada en el mismo cluster que la película ingresada.

    Args:
        titulo_usuario (str): Título de la película ingresada por el usuario.
        df (DataFrame): Dataset con información de películas y sus clusters.

    Returns:
        list: Lista con una película recomendada o un mensaje de error.
    """
    # Buscar la película ingresada por el usuario
    pelicula = df[df['title'].str.lower() == titulo_usuario.lower()]
    
    if pelicula.empty:
        return "La película ingresada no se encuentra en el dataset."
    
    # Obtener el cluster de la película
    cluster_usuario = pelicula['cluster'].iloc[0]
    
    # Filtrar películas del mismo cluster
    recomendaciones = df[df['cluster'] == cluster_usuario]['title'].tolist()
    
    # Eliminar la película ingresada de la lista de recomendaciones
    recomendaciones = [rec for rec in recomendaciones if rec.lower() != titulo_usuario.lower()]
    
    if not recomendaciones:
        return "No se encontraron otras películas en el mismo cluster."
    
    # Seleccionar aleatoriamente una película del cluster
    pelicula_recomendada = random.choice(recomendaciones)
    
    return [pelicula_recomendada]

def comparar_peliculas(df, pelicula_usuario, pelicula_recomendada):
    """
    Compara características, géneros y descripción entre dos películas.
    Devuelve similitud de géneros, descripción y diferencias en características.
    """
    # Filtrar ambas películas
    pelicula1 = df[df['title'].str.lower() == pelicula_usuario.lower()]
    pelicula2 = df[df['title'] == pelicula_recomendada]
    
    if pelicula1.empty or pelicula2.empty:
        return {"error": "Una de las películas no se encuentra en el dataset."}
    
    # Características a comparar
    features = ['vote_average', 'vote_count', 'popularity', 'runtime', 'revenue']
    diferencias = {}
    for feature in features:
        diferencias[feature] = abs(pelicula1[feature].iloc[0] - pelicula2[feature].iloc[0])
    
    # Similitud de géneros
    generos_cols = df.columns[df.columns.str.contains('Genre|Science Fiction|Thriller')]
    generos1 = pelicula1[generos_cols].values[0]
    generos2 = pelicula2[generos_cols].values[0]
    distancia_generos = hamming(generos1, generos2)
    similitud_generos = round(1 - distancia_generos, 2)  # Similitud de géneros
    
    # Similitud de descripción
    overview1 = pelicula1['overview'].iloc[0]
    overview2 = pelicula2['overview'].iloc[0]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([overview1, overview2])
    similitud_descripcion = round(cosine_similarity(tfidf[0], tfidf[1])[0][0], 2)
    
    # Retornar resultados
    resultados = {
        "similitud_generos": similitud_generos,
        "similitud_descripcion": similitud_descripcion,
        "diferencias_caracteristicas": diferencias
    }
    return resultados

def comparar_generos(df, pelicula_usuario, pelicula_recomendada):
    """
    Calcula la similitud de géneros entre dos películas.
    """
    # Filtrar ambas películas
    pelicula1 = df[df['title'].str.lower() == pelicula_usuario.lower()]
    pelicula2 = df[df['title'] == pelicula_recomendada]

    if pelicula1.empty or pelicula2.empty:
        return "Una de las películas no se encuentra en el dataset."

    # Extraer columnas de géneros (usando las columnas generadas con One-Hot Encoding)
    generos_cols = df.columns[df.columns.isin(df['genres'].str.get_dummies(sep=', ').columns)]
    generos1 = pelicula1[generos_cols].values[0]
    generos2 = pelicula2[generos_cols].values[0]

    # Calcular distancia de Hamming entre géneros
    distancia = hamming(generos1, generos2)
    similitud = round((1 - distancia) * 100, 2)  # Convertir la distancia en similitud (en %)

    return f"Similitud de géneros: {similitud}%"

def comparar_descripcion(df, pelicula_usuario, pelicula_recomendada):
    """
    Calcula la similitud de texto entre las descripciones (overview) de dos películas.
    """
    # Filtrar ambas películas
    pelicula1 = df[df['title'].str.lower() == pelicula_usuario.lower()]
    pelicula2 = df[df['title'] == pelicula_recomendada]

    if pelicula1.empty or pelicula2.empty:
        return "Una de las películas no se encuentra en el dataset."

    # Extraer descripciones (overview)
    overview1 = pelicula1['overview'].iloc[0]
    overview2 = pelicula2['overview'].iloc[0]

    # Manejar casos en los que las descripciones estén vacías o nulas
    if pd.isna(overview1) or pd.isna(overview2):
        return "No se pueden comparar las descripciones porque faltan datos."

    # Vectorizar las descripciones y calcular similitud coseno
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([overview1, overview2])
    similitud = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    return round(similitud, 2)
