from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class PolicyHit:
    id: str
    title: str
    text: str
    score: float


@dataclass
class ReleaseDecision:
    feature: str
    decision: str
    rollout_pct: int
    reasons: List[str] = field(default_factory=list)
    failed_gates: List[str] = field(default_factory=list)
    evidence: List[PolicyHit] = field(default_factory=list)
    tool_trace: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "feature": self.feature,
            "decision": self.decision,
            "rollout_pct": self.rollout_pct,
            "reasons": self.reasons,
            "failed_gates": self.failed_gates,
            "evidence": [
                {"id": h.id, "title": h.title, "score": round(h.score, 3)}
                for h in self.evidence
            ],
            "tool_trace": self.tool_trace,
            "metrics": self.metrics,
        }
