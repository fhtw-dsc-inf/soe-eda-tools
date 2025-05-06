
import numpy as np
from sklearn import datasets
from sklearn.model_selection import cross_val_score, ParameterGrid
from sklearn.svm import SVC
import psycopg2
import json

# Datenbankverbindung herstellen
conn = psycopg2.connect(
    dbname='solution_engineering_test',
    user='solution_test',
    password='PW',
    host='fhtw-big-data.postgres.database.azure.com',
    port='5432'
)
cur = conn.cursor()

# Datenbanktabelle erstellen, falls noch nicht vorhanden
cur.execute("""
CREATE TABLE IF NOT EXISTS gridsearch_results (
    id SERIAL PRIMARY KEY,
    params JSON,
    mean_score FLOAT
)
""")
conn.commit()

# Datensatz laden
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Parameter-Raum definieren
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto'],
    'kernel': ['rbf', 'linear']
}

# Prüfen, welche Parameter bereits evaluiert wurden
cur.execute("SELECT params FROM gridsearch_results")
evaluated_params = {json.dumps(row[0]) for row in cur.fetchall()}

# ParameterGrid erstellen und durch Iteration Parameter evaluieren
param_list = list(ParameterGrid(param_grid))


for params in param_list:
    params_json = json.dumps(params)
    if params_json not in evaluated_params:
        model = SVC(**params)
        score = np.mean(cross_val_score(model, X, y, cv=3, n_jobs=-1))
        # Ergebnis in die Datenbank schreiben
        cur.execute(
            "INSERT INTO gridsearch_results (params, mean_score) VALUES (%s, %s)",
            (params_json, score)
        )
        conn.commit()
        print(f"Evaluated: {params}, Score: {score}")

# Beste Ergebnisse abrufen
cur.execute("SELECT params, mean_score FROM gridsearch_results ORDER BY mean_score DESC LIMIT 1")
best_result = cur.fetchone()
print(f"Beste Parameter: {best_result[0]}, Beste Score: {best_result[1]}")

# Datenbankverbindung schließen
cur.close()
conn.close()
