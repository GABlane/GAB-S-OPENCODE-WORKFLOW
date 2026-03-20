GAB'S WORKFLOW - Model Registry and Routing

Model registry (single update point)

| Key | Model | Notes |
| --- | --- | --- |
| manager-default | claude-sonnet-4-6 | Default manager/orchestrator |
| claude-premium | claude-opus-4-6 | Higher tier Claude |
| planner-default | claude-sonnet-4-5 | Planning tasks and planner agent |
| gemini-default | gemini-1.5-flash | Reading/search/docs |
| gemini-large | gemini-1.5-pro | Large context or architecture analysis |
| codex-small | gpt-5.1-codex-mini | Small coding tasks (forced only) |
| codex-medium | gpt-5.2-codex | Medium coding tasks (forced only) |
| codex-large | gpt-5.3-codex | Large or high-risk coding tasks |
| build-default | gpt-5.3-codex | Default build agent (high) |

Model routing policy
- Default manager/orchestrator: manager-default.
- Planner: use planner-default for planning tasks and the Task tool planner agent.
- Claude: triage, plan, delegate, synthesize. Do not do deep analysis or coding unless forced by user.
- Gemini: reading/search/docs. Default gemini-default; use gemini-large for large context or multi-file architecture.
- Codex (building agent): coding/cli/testing/debugging/install deps. Default build-default (high).
  - codex-small for small only if explicitly forced by user.
  - codex-medium for medium only if explicitly forced by user.
  - codex-large for large or high-risk.

Bridge routing (Codex terminal)
- Claude Code never executes code inline. All build work is dispatched via ~/ai-bridge/inbox/.
- Codex picks up TASK files, executes, writes results to ~/ai-bridge/outbox/.
- Claude Code reads results, synthesizes, and plans follow-up if needed.
- See 10-CODEX-BRIDGE.md for protocol details.

Risk overrides (routing)
- Always escalate when touching risk triggers.
- Codex: minimum codex-medium, prefer codex-large.
- Gemini: prefer gemini-large for analysis.

Escalation rules (step-up)
- Start at cheapest suitable tier.
- Escalate if output is uncertain/contradictory or fails validation.
- Escalate to top tier only after step-up fails.
- If ambiguity is product intent: ask user.

Subagent output contracts
- Gemini: summary plus file/section references plus open questions.
- Codex: plan plus diff impact plus tests run/results.
- Claude: final synthesis plus next step or decision.
