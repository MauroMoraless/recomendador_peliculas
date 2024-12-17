from sklearn.ensemble import RandomForestClassifier

def entrenar_random_forest(X, y):
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    return rf