import json
from pathlib import Path
from typing import Dict, Any, List

ROOT = Path(__file__).resolve().parents[2]


def _load(name: str):
    return json.loads((ROOT / "data" / name).read_text())


def get_feature_status(feature: str) -> Dict[str, Any]:
    data = _load("features.json")
    if feature not in data:
        raise KeyError(f"Unknown feature: {feature}")
    return data[feature]


def get_eval_result(feature: str) -> Dict[str, Any]:
    data = _load("eval_runs.json")
    if feature not in data:
        raise KeyError(f"No eval result for feature: {feature}")
    return data[feature]


def get_incident_status(feature: str) -> List[Dict[str, Any]]:
    data = _load("incidents.json")
    return data.get(feature, [])
