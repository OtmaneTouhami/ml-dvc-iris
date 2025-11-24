import json
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.metrics import accuracy_score, classification_report


def load_params(params_path: Path):
    with open(params_path, "r") as f:
        params = yaml.safe_load(f)
    return params


def main():
    params = load_params(Path("params.yaml"))
    train_params = params["train"]
    paths = params["paths"]

    data_path = Path(paths["data"])
    model_path = Path(paths["model"])
    metrics_eval_path = Path(paths["metrics_eval"])

    metrics_eval_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Chargement des données complètes
    df = pd.read_csv(data_path)
    target_col = train_params["target_col"]

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 2. Chargement du modèle
    clf = joblib.load(model_path)

    # 3. Prédictions & métriques
    y_pred = clf.predict(X)
    acc_full = accuracy_score(y, y_pred)
    report_str = classification_report(y, y_pred)

    metrics_eval = {
        "accuracy_full_data": float(acc_full),
        "classification_report": report_str,
    }

    with open(metrics_eval_path, "w") as f:
        json.dump(metrics_eval, f, indent=4)

    print(f"Métriques d'évaluation sauvegardées dans: {metrics_eval_path}")
    print(f"Accuracy (données complètes): {acc_full:.4f}")


if __name__ == "__main__":
    main()
