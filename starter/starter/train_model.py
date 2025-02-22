# Script to train machine learning model.
import sys
import os
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.data_clean import import_data
from starter.ml.data import process_data
from starter.ml.model import train_model, compute_model_metrics, inference
from starter.ml.evaluate import evaluate_on_slices

script_dir = Path(__file__).resolve().parent.parent
model_path = script_dir / "data" / "census.csv"
print(script_dir)
print(model_path)

data = import_data(model_path)
data.columns = data.columns.str.replace(' ', '')
data.columns = data.columns.str.replace('-', '_')
print(data.columns)

# Optional enhancement, use K-fold cross validation instead of a train-test split.
train, test = train_test_split(data, test_size=0.20)

cat_features = [
    "workclass",
    "education",
    "marital_status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native_country",
]
target = "salary"

try:
    X_train, y_train, encoder, lb = process_data(
        train, categorical_features=cat_features, label=target, training=True
    )
    print("Processamento de dados de treino concluído.")
except Exception as e:
    print(f"Ocorreu um erro durante o processamento de dados de treino: {e}")

# Proces the test data with the process_data function.
try:
    X_test, y_test, _, _ = process_data(
        test, categorical_features=cat_features, label=target, training=False, encoder=encoder, lb=lb
    )
    print("Processamento de dados de teste concluído.")
except Exception as e:
    print(f"Ocorreu um erro durante o processamento de dados de teste: {e}")

print(X_train.shape)

model = train_model(X_train, y_train)
preds = inference(model, X_test)

results = evaluate_on_slices(model, test, cat_features, target, encoder, lb)

precision, recall, fbeta = compute_model_metrics(y_test, preds)
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F-beta: {fbeta:.4f}")

base_path = Path(__file__).resolve().parent.parent
joblib.dump(model,os.path.join(base_path,"model", "random_forest_model.pkl"))
joblib.dump(encoder,os.path.join(base_path,"model","encoder.pkl"))
joblib.dump(lb,os.path.join(base_path, "model", "lb.pkl"))