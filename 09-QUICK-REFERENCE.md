GAB'S WORKFLOW - Quick Reference

Modes

| Mode | When to use | Output behavior |
| --- | --- | --- |
| L1 | Single file or <20 lines change, or pure question | Direct answer, no plan |
| L2 | 2 to 3 files or 20 to 150 lines, single concern | Short plan (3 to 5 steps) plus ask "go?" |
| L3 | 4+ files or >150 lines, cross-concern or architecture | Structured plan with checkpoints |

Risk triggers (force L2 or higher)
- auth
- payments
- database schema/migrations
- env/config
- security
- PII

Agent quick pick

| Need | Agent |
| --- | --- |
| Multi-step research | general |
| Codebase exploration | explore |
| Small change | build-small |
| Large/risky change | build-large |
| Planning/architecture | planner or architect |
| Code review | code-reviewer |
| Security review | security-reviewer |
| TDD guidance | tdd-guide |
| Build/type errors | build-error-resolver |
| E2E tests | e2e-runner |
| Documentation | doc-updater |
| Cleanup/refactor | refactor-cleaner |
| Go review | go-reviewer |
| Go build errors | go-build-resolver |
| Database review | database-reviewer |

Tool quick pick

| Need | Tool |
| --- | --- |
| Read a file | read |
| Find files by name | glob |
| Search content | grep |
| Edit/add file | apply_patch |
| Terminal command | bash |
| Use a subagent | task |
| Ask a question | question |
| Fetch URL | webfetch |

Overrides

| Command | Effect |
| --- | --- |
| !L1 / !L2 / !L3 | Force mode for this request |
| !ForceModel <tier> | Force model for this request |
| !LockModel <tier> | Lock model until cleared |
| !ClearModel | Clear model lock |

Routine triggers

| Trigger | Action |
| --- | --- |
| "morning" | Run priority arbitration, output morning template |
| "eod" | Output EOD template, then ask carry-over confirmation |
| "what should i work on now" | Run priority arbitration |
