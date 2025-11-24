from pathlib import Path

import pandas as pd
from sklearn.preprocessing import StandardScaler


def preprocess():
    data_dir = Path("data")
    raw_path = data_dir / "iris.csv"
    prep_path = data_dir / "iris_preprocessed.csv"

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Fichier {raw_path} introuvable. Lancez d'abord scripts/download_iris.py"
        )

    df = pd.read_csv(raw_path)

    # On suppose que la dernière colonne est la cible
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    df_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    df_scaled["target"] = y

    prep_path.parent.mkdir(parents=True, exist_ok=True)
    df_scaled.to_csv(prep_path, index=False)
    print(f"Dataset prétraité sauvegardé dans {prep_path}")

