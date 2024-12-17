from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def entrenar_clustering(df, n_clusters=10):
    # Verificar si la columna 'cluster' ya existe
    if 'cluster' not in df.columns:
        print("Entrenando modelo de clustering...")
        
        # Seleccionar características numéricas
        features = ['popularity', 'vote_average', 'vote_count']
        
        # Eliminar filas con valores nulos en las columnas necesarias
        df = df.dropna(subset=features)
        
        # Escalar las características
        scaler = StandardScaler()
        X = scaler.fit_transform(df[features])

        # Aplicar KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['cluster'] = kmeans.fit_predict(X)
        print("Clustering completado. Columna 'cluster' añadida.")
    
    return df


def recomendar_pelicula(titulo_usuario, df):
    # Buscar la película ingresada por el usuario
    pelicula = df[df['title'].str.lower() == titulo_usuario.lower()]
    
    if pelicula.empty:
        return "Película no encontrada."
    
    # Obtener el cluster de la película encontrada
    cluster = pelicula['cluster'].iloc[0]
    
    # Filtrar películas del mismo cluster
    recomendaciones = df[df['cluster'] == cluster]['title'].tolist()
    
    # Eliminar la película ingresada de las recomendaciones
    recomendaciones = [r for r in recomendaciones if r.lower() != titulo_usuario.lower()]
    
    if not recomendaciones:
        return "No se encontraron recomendaciones en el mismo cluster."
    
    # Devolver la primera película recomendada
    return recomendaciones[:1]
