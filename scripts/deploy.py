import json
import shutil
from pathlib import Path

def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None

def main():
    # Paths
    metrics_dir = Path("metrics")
    models_dir = Path("models")
    
    eval_metrics_path = metrics_dir / "eval_metrics.json"
    best_metrics_path = metrics_dir / "best_metrics.json"
    
    current_model_path = models_dir / "random_forest.pkl"
    production_model_path = models_dir / "production_model.pkl"

    # Load metrics
    eval_metrics = load_json(eval_metrics_path)
    if not eval_metrics:
        print(f"Error: {eval_metrics_path} not found.")
        return

    current_acc = eval_metrics.get("accuracy_full_data", 0.0)
    print(f"Current Accuracy: {current_acc:.4f}")

    best_metrics = load_json(best_metrics_path)
    best_acc = 0.0
    if best_metrics:
        best_acc = best_metrics.get("accuracy_full_data", 0.0)
        print(f"Best Recorded Accuracy: {best_acc:.4f}")
    else:
        print("No best metrics found. Initializing...")

    # Compare and Deploy
    if current_acc >= best_acc:
        print("New model is better or equal. Deploying to production...")
        
        # Copy model
        shutil.copy(current_model_path, production_model_path)
        print(f"Model copied to {production_model_path}")
        
        # Update best metrics
        # We save the whole eval_metrics content as the new best_metrics
        with open(best_metrics_path, "w") as f:
            json.dump(eval_metrics, f, indent=4)
        print(f"Best metrics updated in {best_metrics_path}")
    else:
        print("New model is not better. Skipping deployment.")

if __name__ == "__main__":
    main()
