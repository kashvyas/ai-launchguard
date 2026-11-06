import json
from pathlib import Path

from src.ai_launchguard.agent import LaunchGuard

ROOT = Path(__file__).resolve().parents[1]


def run():
    golden = json.loads((ROOT / "evals" / "golden_set.json").read_text())
    agent = LaunchGuard()

    decision_hits = 0
    citation_hits = 0
    tool_hits = 0
    guardrail_hits = 0
    guardrail_cases = 0
    rows = []

    for case in golden:
        result = agent.assess(case["feature"], case["requested_rollout_pct"])
        decision_ok = result.decision == case["expected_decision"]
        citation_ok = len(result.evidence) > 0
        tools_ok = all(t in result.tool_trace for t in case["required_tools"])

        expected_gate = case.get("expected_failed_gate")
        if expected_gate:
            guardrail_cases += 1
            guardrail_ok = expected_gate in result.failed_gates
            guardrail_hits += int(guardrail_ok)
        else:
            guardrail_ok = True

        decision_hits += int(decision_ok)
        citation_hits += int(citation_ok)
        tool_hits += int(tools_ok)
        rows.append((case["id"], decision_ok, citation_ok, tools_ok, guardrail_ok, result.decision))

    n = len(golden)
    metrics = {
        "decision_accuracy": decision_hits / n,
        "citation_coverage": citation_hits / n,
        "tool_use_correctness": tool_hits / n,
        "guardrail_recall": guardrail_hits / guardrail_cases if guardrail_cases else 1.0,
        "regression_rate": 1.0 - (decision_hits / n),
    }

    print("Golden-set results")
    for row in rows:
        print(row)
    print("\nMetrics")
    print(json.dumps(metrics, indent=2))

    assert metrics["decision_accuracy"] == 1.0
    assert metrics["citation_coverage"] == 1.0
    assert metrics["tool_use_correctness"] == 1.0
    assert metrics["guardrail_recall"] == 1.0

    return metrics


if __name__ == "__main__":
    run()
