from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Cargar el dataset
df = pd.read_csv("../data/tmdb_2023_movies_reducido.csv")

# Transformar la columna 'genres' usando One-Hot Encoding
# Dividir géneros separados por comas en columnas individuales
genres_onehot = df['genres'].str.get_dummies(sep=', ')
df = pd.concat([df, genres_onehot], axis=1)

# Selección de características
features = ['vote_average', 'vote_count', 'popularity', 'revenue', 'runtime'] + list(genres_onehot.columns)

# Aplicar transformación logarítmica para corregir valores sesgados
df['revenue'] = np.log1p(df['revenue'])
df['vote_count'] = np.log1p(df['vote_count'])

# Eliminar valores nulos
df = df.dropna(subset=features)

# Escalar características
scaler = StandardScaler()
X = scaler.fit_transform(df[features])

# Entrenar Agglomerative Clustering
agg_clustering = AgglomerativeClustering(n_clusters=15, linkage='ward')
df['cluster'] = agg_clustering.fit_predict(X)

# Verificar los clusters
print("Resumen de Clusters Generados:")
print(df['cluster'].value_counts())
print("Primeras filas del dataset con clusters:")
print(df[['title', 'cluster']].head(20))

# Guardar el dataset con clusters
df.to_csv("../data/tmdb_2023_movies_clustered.csv", index=False)
print("Dataset con clusters guardado correctamente.")

# Visualización del Dendrograma
Z = linkage(X, method='ward')
plt.figure(figsize=(12, 6))
dendrogram(Z, truncate_mode="level", p=10)
plt.title("Dendrograma de Agglomerative Clustering")
plt.xlabel("Índice de las Películas")
plt.ylabel("Distancia")
plt.show()
