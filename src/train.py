import json
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


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
    metrics_path = Path(paths["metrics_train"])

    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Chargement des données prétraitées
    df = pd.read_csv(data_path)
    target_col = train_params["target_col"]

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 2. Split train / test
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=train_params["test_size"],
        random_state=train_params["random_state"],
        stratify=y,
    )

    # 3. Modèle RandomForest
    clf = RandomForestClassifier(
        n_estimators=train_params["n_estimators"],
        max_depth=train_params["max_depth"],
        random_state=train_params["random_state"],
    )
    clf.fit(X_train, y_train)

    # 4. Evaluation sur le test
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # 5. Sauvegarde du modèle
    joblib.dump(clf, model_path)

    # 6. Sauvegarde des métriques
    metrics = {
        "accuracy_test": float(acc),
        "n_estimators": train_params["n_estimators"],
        "max_depth": train_params["max_depth"],
        "test_size": train_params["test_size"],
        "random_state": train_params["random_state"],
    }
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"Modèle entraîné sauvegardé dans: {model_path}")
    print(f"Métriques d'entraînement sauvegardées dans: {metrics_path}")
    print(f"Accuracy (test): {acc:.4f}")


if __name__ == "__main__":
    main()
