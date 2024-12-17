def procesar_dataset(df):
    return df[['title', 'genres', 'popularity', 'vote_average', 'vote_count']].dropna()
