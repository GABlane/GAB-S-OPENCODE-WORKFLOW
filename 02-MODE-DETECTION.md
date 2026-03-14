GAB'S WORKFLOW - Mode Detection

Size thresholds (single source of truth)
- small: 1 file or less than 50 LOC
- medium: 2 to 4 files or 50 to 300 LOC
- large: 5 or more files or more than 300 LOC

L1 (simple)
- Direct answer, no plan.
- Single file or less than 20 lines change, or pure question/explanation.

L2 (moderate)
- Short plan (3 to 5 steps) plus ask "go?".
- Single concern.
- 2 to 3 files or 20 to 150 lines.
- Needs tradeoffs but not architecture change.

L3 (complex)
- Structured plan plus checkpoints.
- 4 or more files or cross-concern.
- More than 150 lines expected.
- Architecture, data, auth, migrations, or background tasks.
- Likely more than 1 hour or high uncertainty.

Risk override
- If the change touches risk triggers, floor mode at L2 minimum.
- State reason briefly, e.g. "Flagged L2: touches auth."

Risk triggers (single source of truth)
- auth
- payments
- database schema/migrations
- env/config
- security
- PII

Session state header
- Show only in L2 or L3:
  `Active project: <name> | Mode: L# | Last action: <short> | Focus: <optional>`
- Hide in L1 unless asked.
