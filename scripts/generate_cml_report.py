import json
from pathlib import Path

def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None

def main():
    # Define paths
    metrics_dir = Path("metrics")
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    train_metrics_path = metrics_dir / "train_metrics.json"
    eval_metrics_path = metrics_dir / "eval_metrics.json"
    feature_importances_path = metrics_dir / "feature_importances.json"
    class_metrics_path = metrics_dir / "class_metrics.json"
    
    report_path = reports_dir / "cml_report.md"

    # Load metrics
    train_metrics = load_json(train_metrics_path)
    eval_metrics = load_json(eval_metrics_path)
    feature_importances = load_json(feature_importances_path)
    class_metrics = load_json(class_metrics_path)

    markdown_lines = ["# CML Report", ""]

    # Training Metrics Section
    if train_metrics:
        markdown_lines.append("## Training Metrics")
        markdown_lines.append("")
        markdown_lines.append("| Metric | Value |")
        markdown_lines.append("| :--- | :--- |")
        markdown_lines.append(f"| Accuracy (Test Split) | {train_metrics.get('accuracy_test', 'N/A'):.4f} |")
        markdown_lines.append(f"| n_estimators | {train_metrics.get('n_estimators', 'N/A')} |")
        markdown_lines.append(f"| max_depth | {train_metrics.get('max_depth', 'N/A')} |")
        markdown_lines.append(f"| test_size | {train_metrics.get('test_size', 'N/A')} |")
        markdown_lines.append("")
    
    # Evaluation Metrics Section
    if eval_metrics:
        markdown_lines.append("## Evaluation Metrics")
        markdown_lines.append("")
        markdown_lines.append(f"**Accuracy (Full Data):** {eval_metrics.get('accuracy_full_data', 'N/A'):.4f}")
        markdown_lines.append("")
        
        if "classification_report" in eval_metrics:
            markdown_lines.append("### Classification Report")
            markdown_lines.append("```")
            markdown_lines.append(eval_metrics["classification_report"])
            markdown_lines.append("```")
            markdown_lines.append("")

    # Feature Importances Section
    if feature_importances:
        markdown_lines.append("## Feature Importances")
        markdown_lines.append("")
        markdown_lines.append("| Feature | Importance |")
        markdown_lines.append("| :--- | :--- |")
        for feature, importance in feature_importances.items():
            markdown_lines.append(f"| {feature} | {importance:.4f} |")
        markdown_lines.append("")

    # Class Metrics Section
    if class_metrics:
        markdown_lines.append("## Class Metrics")
        markdown_lines.append("")
        markdown_lines.append("| Class | Precision | Recall | F1-Score | Support |")
        markdown_lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for cls, metrics in class_metrics.items():
            if isinstance(metrics, dict): # Skip 'accuracy' key which is a float
                markdown_lines.append(f"| {cls} | {metrics.get('precision', 'N/A'):.4f} | {metrics.get('recall', 'N/A'):.4f} | {metrics.get('f1-score', 'N/A'):.4f} | {metrics.get('support', 'N/A')} |")
        markdown_lines.append("")

    # Write report
    with open(report_path, "w") as f:
        f.write("\n".join(markdown_lines))
    
    print(f"Report generated at {report_path}")

if __name__ == "__main__":
    main()
