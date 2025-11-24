from pathlib import Path

import pandas as pd
from sklearn.datasets import load_iris


def main():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    iris = load_iris(as_frame=True)
    df = iris.frame

    out_path = data_dir / "iris.csv"
    df.to_csv(out_path, index=False)
    print(f"Dataset Iris sauvegardé dans {out_path}")


if __name__ == "__main__":
    main()
