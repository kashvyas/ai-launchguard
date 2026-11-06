# AI LaunchGuard — Portfolio One-Pager

## Problem
AI product teams need a fast, auditable answer to a recurring launch question: **is this feature safe and ready to ship?** Evidence is fragmented across evals, Responsible AI reviews, incidents, rollout state, and policy.

## Product hypothesis
A tool-using copilot can reduce PM decision friction **without weakening controls** if it retrieves the minimum relevant policy, fetches live structured evidence through tools, and keeps explicit release thresholds deterministic.

## Prototype
- Retrieves relevant launch policy.
- Calls tools for feature state, eval metrics, and incidents.
- Produces `SHIP`, `HOLD`, or `LIMITED_ROLLOUT`.
- Explains failed gates with policy evidence.
- Exposes capabilities through MCP.
- Runs a golden-set regression suite before changes ship.

## Eval contract
| Metric | Prototype target | Current |
|---|---:|---:|
| Decision accuracy | 100% | 100% |
| Citation coverage | 100% | 100% |
| Required-tool correctness | 100% | 100% |
| Guardrail recall | 100% | 100% |
| Golden-set regression rate | 0% | 0% |

## Key product decision
**Do not let the model own hard launch gates.** Retrieval handles ambiguous policy context; tools fetch current system state; deterministic logic applies explicit thresholds. An LLM can improve explanation and exception investigation without becoming the control plane.

## Production roadmap
**V1:** authenticated integrations + trace store + policy versioning.  
**V2:** hybrid retrieval/reranking + experiment telemetry + human-rater pipeline.  
**V3:** event-driven monitoring + exception workflow + automated regression/drift alerts.

## What this demonstrates
Agent orchestration • tool use • retrieval/context engineering • MCP • eval-first PM • regression testing • Responsible AI • observability • written product judgment.
