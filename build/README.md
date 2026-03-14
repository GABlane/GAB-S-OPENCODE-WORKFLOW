# GAB OpenCode Build Output

This directory contains a hydrated and pinned source bundle plus an OpenCode workflow overlay.

## Included

- `LOCK.json`: Reproducible source lock with pinned upstream commits.
- `overlay/OPENCODE-WORKFLOW.md`: Consolidated workflow spec built from `01`-`09` docs.
- `overlay/manifests/*.json`: Machine-readable manifests for routing and behavior.
- `overlay/integration/*`: Source mapping and skillful bridge notes.
- `verification/REPORT.md`: Build and test validation report.

## Hydrated Upstream Sources

- ECC source: `everything-claude-code` at `32e9c293f0d6f04e3b9bf804887747d5c8b5dc10`
- Skillful source: `opencode-skillful` at `9ee443f5d61f1783cdbf6e01acb3a587b3c3b4f8`

## Notes

- `opencode-skillful` has been migrated to a Yarn-based toolchain.
- Validation now runs with `corepack yarn` commands and is recorded in `verification/REPORT.md`.
- Workflow source of truth remains the root docs (`01` to `09`).
