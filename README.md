# AI LaunchGuard — AI Product Leadership Proof

A compact portfolio prototype built to demonstrate **AI-native product management craft**: agentic workflow design, retrieval/context engineering, tool use, MCP exposure, eval-first release gates, observability, and responsible-AI decisioning.

> **Important:** This is a synthetic portfolio project. It uses only synthetic data and does not use employer systems, customer data, policies, or proprietary information.

## What it does

The copilot answers one high-value PM question:

**“Should this AI feature ship?”**

It combines:
- a lightweight retrieval layer over product/release policy,
- structured tool calls for eval results, incidents, and feature metadata,
- deterministic release-gate logic,
- citations to the retrieved policy snippets,
- trace output showing which tools and evidence were used,
- a golden-set evaluation harness for regression testing.

## Why this matters for AI product leadership

The design demonstrates the ability to:
- translate ambiguous business questions into an agent-shaped workflow,
- define “good” numerically before launch,
- use tools rather than stuffing all context into a prompt,
- expose reusable capabilities through MCP,
- instrument output quality and regressions,
- preserve responsible-AI and release controls.

## 5-minute demo

```bash
python -m src.ai_launchguard.demo
python -m evals.run_evals
```

Example question:

> Can campaign-copilot-v17 ship to 100% of users on Friday?

The system returns:
- **SHIP / HOLD / LIMITED ROLLOUT**
- reasons tied to release thresholds
- policy evidence
- tool trace
- failed gates

## Optional MCP server

The core demo has no external dependencies. To expose the tools through the current MCP Python SDK:

```bash
pip install "mcp[cli]>=2,<3"
python mcp_server.py
```

The server exposes:
- `get_feature_status`
- `get_eval_result`
- `get_incident_status`
- `assess_release`

## Project layout

```text
src/ai_launchguard/
  agent.py          # orchestration + release decision
  retrieval.py      # context retrieval
  tools.py          # structured tools
  schemas.py        # typed domain objects
  demo.py           # interactive/demo path

data/
  policies.json     # synthetic release policy corpus
  features.json     # synthetic feature state
  eval_runs.json    # synthetic eval results
  incidents.json    # synthetic incidents

evals/
  golden_set.json   # expected behavior
  run_evals.py      # quality/regression harness
mcp_server.py       # MCP v2 server
CLAUDE.md           # AI coding/product operating instructions
DECISION_MEMO.md    # product/architecture tradeoffs
```

## Core product metrics

The prototype treats AI quality as a product surface. The eval harness checks:
- **decision accuracy** — expected release decision
- **citation coverage** — answer cites relevant policy evidence
- **tool-use correctness** — required tools were invoked
- **guardrail recall** — critical failure conditions are caught
- **regression rate** — golden cases that changed unexpectedly

## Design choice: deterministic release gate

The release decision is intentionally deterministic. An LLM may help summarize or explain evidence, but it should not be the final authority for a launch gate with explicit thresholds. This keeps the decision:
- auditable,
- testable,
- reproducible,
- easy to override with policy changes.

That is the product point of the prototype: **use AI where ambiguity exists; keep hard controls hard.**

## Repository

https://github.com/kashvyas/ai-launchguard
