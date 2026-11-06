import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import List

from .schemas import PolicyHit

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "data" / "policies.json"


def _tokens(text: str):
    return re.findall(r"[a-z0-9]+", text.lower())


class PolicyRetriever:
    """Tiny TF-IDF-like retriever so the demo is deterministic and zero-key."""

    def __init__(self, path: Path = POLICY_PATH):
        self.docs = json.loads(path.read_text())
        self.doc_tokens = [Counter(_tokens(d["title"] + " " + d["text"])) for d in self.docs]
        self.df = Counter()
        for counts in self.doc_tokens:
            for token in counts:
                self.df[token] += 1
        self.n = len(self.docs)

    def _idf(self, token: str) -> float:
        return math.log((self.n + 1) / (self.df.get(token, 0) + 1)) + 1.0

    def search(self, query: str, k: int = 4) -> List[PolicyHit]:
        q = Counter(_tokens(query))
        scored = []
        for doc, counts in zip(self.docs, self.doc_tokens):
            score = 0.0
            for token, qtf in q.items():
                if token in counts:
                    score += qtf * counts[token] * self._idf(token)
            if score > 0:
                scored.append(PolicyHit(doc["id"], doc["title"], doc["text"], score))
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:k]
