GAB'S WORKFLOW - Overrides and Escape Hatches

Mode override
- If user message starts with `!L1`, `!L2`, or `!L3`:
  - force that level for this request
  - skip auto-detection

Model override
- If user message starts with `!ForceModel <tier>`:
  - force routing to that tier for this request only
- If user message starts with `!LockModel <tier>`:
  - force routing to that tier for all requests until cleared
- Clear with: `!ClearModel`
- If tier not found in registry, reject and list valid keys.

Valid tier keys
- manager-default
- claude-premium
- planner-default
- gemini-default
- gemini-large
- codex-small
- codex-medium
- codex-large
- build-default

Examples
- `!L2 add pagination to the API`
- `!ForceModel codex-large refactor the worker`
- `!LockModel gemini-large`
- `!ClearModel`
