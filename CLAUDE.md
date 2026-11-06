# CLAUDE.md — AI LaunchGuard

## Product intent
Build the smallest reliable system that helps an AI PM decide whether a feature is ready to ship.

## Operating rules
1. Prefer explicit tools and typed state over hidden prompt context.
2. Never infer a missing release metric. Mark it missing and fail closed for critical gates.
3. Keep launch thresholds in policy/data, not scattered through prose.
4. Every decision must include evidence and a trace of tools used.
5. Preserve deterministic release gates; LLM-generated text must never override them.
6. Add or update a golden-set test for every behavior change.
7. Treat Responsible AI, incident status, and rollback readiness as release requirements.
8. Avoid collecting or storing personal customer, financial, or other sensitive data in this portfolio project.

## Definition of done
A change is done only when:
- unit tests pass,
- golden-set decision accuracy is 100%,
- guardrail recall is 100%,
- no critical release gate can silently pass with missing data,
- README or decision memo is updated if behavior changes.

## Product review checklist
- What business/user problem changed?
- What new failure mode did we introduce?
- Which metric proves the change is better?
- Which golden case proves it?
- What is the rollback path?
