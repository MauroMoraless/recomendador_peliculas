import pandas as pd

# Ruta al dataset original
dataset_path = "data/tmdb_2023_movies.csv"  # Ajusta esta ruta si es necesario

# Cargar el dataset original
df = pd.read_csv(dataset_path)

# Verificar las columnas disponibles
print("Columnas disponibles:", df.columns)

# Filtrar filas con más de 50 votos y limitar a 5000 filas
df_reducido = df[df['vote_count'] > 50].head(5000)

# Guardar el dataset reducido
output_path = "data/tmdb_2023_movies_reducido.csv"
df_reducido.to_csv(output_path, index=False)

print(f"Dataset reducido guardado en: {output_path}")