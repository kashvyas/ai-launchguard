# AI LaunchGuard — Architecture Decision Memo

## Decision
Use a **tool-using orchestration layer + lightweight retrieval + deterministic release policy engine** instead of a free-form LLM agent making the final ship decision.

## Problem
AI PMs often need to combine multiple kinds of evidence: quality evals, incidents, rollout state, responsible-AI checks, and release policy. A single long prompt is hard to audit and regression-test.

## Architecture
1. **Retriever** finds the minimum relevant policy context.
2. **Tools** fetch current structured facts for the feature.
3. **Agent/orchestrator** decides which tools are required.
4. **Policy engine** applies explicit thresholds.
5. **Response layer** explains the decision with citations and trace.
6. **Eval harness** tests expected outcomes and regressions.

## Tradeoffs

### Why not pure RAG?
RAG is useful for policy evidence, but release metrics are structured state. Tool calls are cleaner, fresher, and easier to validate.

### Why not let an LLM decide?
Launch gates are control logic. A model can explain, summarize, or help investigate exceptions, but explicit thresholds should remain deterministic.

### Why a small custom retriever?
This keeps the portfolio project zero-key and reproducible. In production, the retrieval layer could be replaced with hybrid/vector retrieval and reranking without changing the agent contract.

### Why MCP?
The same capabilities should be reusable by different AI clients and PM workflows. MCP gives a standard interface for tools without coupling the core product logic to one chat UI.

## What I would add in production
- authenticated service-to-service access,
- event-driven updates for eval/incident state,
- model/version registry integration,
- hybrid retrieval + reranking,
- human approval workflow for exceptions,
- online experiment metrics,
- trace store and dashboards,
- role-based access controls,
- policy versioning and signed decisions.
