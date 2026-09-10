# test_friday_sample.py — run with: pytest test_friday_sample.py
import json
from pathlib import Path

REQUIRED_MODELS = {"baseline", "logistic_regression", "decision_tree", "random_forest"}
REQUIRED_METRIC_KEYS = {"accuracy", "precision", "recall", "f1", "roc_auc"}

def test_model_metrics_shape():
    data = json.loads(Path("model_metrics.json").read_text())
    assert REQUIRED_MODELS <= data.keys()
    for m in REQUIRED_MODELS:
        assert REQUIRED_METRIC_KEYS <= data[m].keys()
    assert "credit_score_imputation_value" in data
    assert data["final_model"] in REQUIRED_MODELS

def test_charts_exist():
    for name in ["chart_model_comparison.png", "chart_calibration.png"]:
        p = Path(name)
        assert p.exists() and p.stat().st_size > 1000

def test_report_and_defense_exist():
    assert Path("evaluation_report.md").exists()
    assert Path("defense_answers.md").exists()