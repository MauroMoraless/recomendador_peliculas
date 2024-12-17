import pandas as pd
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
