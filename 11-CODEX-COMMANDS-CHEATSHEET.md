GAB'S WORKFLOW - Codex Commands Cheatsheet

Purpose
- Quick "use this when..." guide for the command set under `everything-claude-code/commands`.

Fast picks (most practical daily)

| Command | Use when | What it does |
| --- | --- | --- |
| `/plan` | Before coding multi-file or risky work | Builds a step-by-step plan and waits for approval. |
| `/tdd` | New features or bug fixes | Enforces RED -> GREEN -> REFACTOR with 80%+ coverage target. |
| `/build-fix` | Build/typecheck is failing | Fixes errors incrementally with minimal diffs. |
| `/verify` | Before commit/PR | Runs build, types, lint, tests, and readiness checks. |
| `/code-review` | After edits | Reviews changed files for security and quality issues. |
| `/test-coverage` | Coverage is low | Finds gaps and generates missing tests toward 80%+. |
| `/refactor-clean` | Suspected dead code | Finds/removes unused code safely with verification loops. |
| `/e2e` | Critical user flow changes | Generates and runs Playwright E2E tests with artifacts. |
| `/update-docs` | Docs drift from code | Syncs docs from source-of-truth files. |
| `/update-codemaps` | Need architecture context | Generates token-lean codemaps for fast AI/human onboarding. |

Planning and orchestration

| Command | Primary use |
| --- | --- |
| `/orchestrate` | Sequential agent workflow (feature, bugfix, refactor, security). |
| `/multi-plan` | Multi-model planning flow (also referenced as `/ccg:plan`). |
| `/multi-execute` | Multi-model implementation flow (also referenced as `/ccg:execute`). |
| `/multi-workflow` | End-to-end multi-model workflow (Research -> Ideation -> Plan -> Execute -> Optimize -> Review). |
| `/multi-backend` | Backend-focused orchestrated workflow (also referenced as `/backend`). |
| `/multi-frontend` | Frontend-focused orchestrated workflow (also referenced as `/frontend`). |

Language-specific

| Command | Primary use |
| --- | --- |
| `/go-build` | Resolve Go build/vet/lint issues. |
| `/go-test` | Go TDD with table-driven tests and coverage checks. |
| `/go-review` | Go-centric review: idioms, concurrency, security, error handling. |
| `/python-review` | Python-centric review: PEP 8, typing, security, Pythonic patterns. |

Learning and instinct system

| Command | Primary use |
| --- | --- |
| `/learn` | Extract reusable patterns from current session. |
| `/learn-eval` | Extract + quality-score + choose global vs project save location. |
| `/skill-create` | Generate SKILL.md patterns from local git history. |
| `/instinct-status` | Show project/global instincts with confidence. |
| `/instinct-import` | Import instincts from file or URL. |
| `/instinct-export` | Export instincts to shareable file. |
| `/promote` | Promote project instincts to global scope. |
| `/projects` | Show known projects and instinct statistics. |
| `/evolve` | Cluster instincts into higher-level skills/commands/agents. |

Sessions and tooling

| Command | Primary use |
| --- | --- |
| `/sessions` | List/load/alias/manage session history. |
| `/checkpoint` | Create and compare workflow checkpoints. |
| `/setup-pm` | Detect/set preferred package manager (npm/pnpm/yarn/bun). |
| `/pm2` | Auto-generate PM2 configs and command helpers. |
| `/claw` | Start persistent NanoClaw REPL session. |
| `/eval` | Define/check/report/list eval-driven checks. |

Recommended flows

| Scenario | Suggested sequence |
| --- | --- |
| New feature | `/plan` -> `/tdd` -> `/build-fix` -> `/verify` -> `/code-review` |
| Bug fix | `/tdd` -> `/build-fix` -> `/verify` -> `/code-review` |
| Risky release | `/verify` -> `/test-coverage` -> `/e2e` -> `/code-review` |
| Cleanup day | `/refactor-clean` -> `/verify` -> `/update-codemaps` |
| Session learning | `/learn-eval` -> `/promote` (if broadly useful) |
