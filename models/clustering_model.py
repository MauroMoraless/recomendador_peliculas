from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

def entrenar_clustering(df):
    scaler = StandardScaler()
    X = scaler.fit_transform(df[['popularity', 'vote_average', 'vote_count']])
    clustering = AgglomerativeClustering(n_clusters=10)
    df['cluster'] = clustering.fit_predict(X)
    return df