from typing import Optional

from .retrieval import PolicyRetriever
from .schemas import ReleaseDecision
from .tools import get_feature_status, get_eval_result, get_incident_status


class LaunchGuard:
    def __init__(self):
        self.retriever = PolicyRetriever()

    def assess(self, feature: str, requested_rollout_pct: Optional[int] = None) -> ReleaseDecision:
        trace = []

        policy_query = (
            "AI production broad release quality critical error regression responsible AI "
            "incident rollout monitoring rollback"
        )
        evidence = self.retriever.search(policy_query, k=5)
        trace.append("policy_retrieval")

        feature_state = get_feature_status(feature)
        trace.append("get_feature_status")

        evals = get_eval_result(feature)
        trace.append("get_eval_result")

        incidents = get_incident_status(feature)
        trace.append("get_incident_status")

        rollout = requested_rollout_pct if requested_rollout_pct is not None else int(feature_state["requested_rollout_pct"])
        failed = []
        reasons = []
        force_limited = False

        required = ["task_success", "critical_error_rate", "regression_rate"]
        missing = [m for m in required if m not in evals]
        if missing:
            failed.append("missing_critical_metrics")
            reasons.append(f"Missing critical eval metrics: {', '.join(missing)}")
        else:
            if evals["task_success"] < 0.90:
                failed.append("task_success")
                reasons.append(f"Task success {evals['task_success']:.2f} is below 0.90")
            if evals["critical_error_rate"] > 0.02:
                failed.append("critical_error_rate")
                reasons.append(f"Critical error rate {evals['critical_error_rate']:.2f} exceeds 0.02")
            if evals["regression_rate"] > 0.03:
                failed.append("regression_rate")
                reasons.append(f"Regression rate {evals['regression_rate']:.2f} exceeds 0.03")

        rai = feature_state.get("rai_status", "MISSING")
        if rai in {"BLOCKED", "MISSING"}:
            failed.append("responsible_ai")
            reasons.append(f"Responsible AI status is {rai}")
        elif rai == "CONDITIONAL":
            force_limited = True
            reasons.append("Responsible AI review is conditional; broad release is not allowed")

        if not feature_state.get("rollback_ready", False):
            failed.append("rollback_readiness")
            reasons.append("Rollback plan is not ready")
        if not feature_state.get("monitoring_ready", False):
            failed.append("monitoring_readiness")
            reasons.append("Runtime monitoring is not ready")

        for incident in incidents:
            if incident.get("status") != "OPEN":
                continue
            sev = int(incident.get("severity", 99))
            if sev <= 2:
                failed.append("open_high_severity_incident")
                reasons.append(f"Open severity-{sev} incident {incident.get('id')}")
            elif sev == 3:
                if not incident.get("workaround_ready", False):
                    failed.append("sev3_without_workaround")
                    reasons.append(f"Severity-3 incident {incident.get('id')} has no tested workaround")
                else:
                    force_limited = True
                    reasons.append(f"Severity-3 incident {incident.get('id')} requires cautious rollout")

        if failed:
            decision = "HOLD"
            rollout = 0
        elif force_limited or rollout > 10 and rai == "CONDITIONAL":
            decision = "LIMITED_ROLLOUT"
            rollout = min(10, rollout)
        else:
            decision = "SHIP"

        if decision == "SHIP":
            reasons.append("All mandatory release gates pass")
        elif decision == "LIMITED_ROLLOUT":
            reasons.append("Release may proceed only with a capped rollout and monitoring")

        return ReleaseDecision(
            feature=feature,
            decision=decision,
            rollout_pct=rollout,
            reasons=reasons,
            failed_gates=failed,
            evidence=evidence,
            tool_trace=trace,
            metrics=evals,
        )
