import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Enable autologging
mlflow.sklearn.autolog()

# Load and preprocess dataset
df = pd.read_csv("bankdata.csv")

# Encode categorical variables
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = LabelEncoder().fit_transform(df[col])

X = df.drop("y", axis=1)
y = df["y"]

# Scale features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model inside MLflow run
C = 0.1
with mlflow.start_run():
    model = LogisticRegression(C=C, max_iter=1000)
    model.fit(X_train, y_train)


    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Accuracy: {acc:.4f}")
