# Skillful Bridge

This overlay assumes `opencode-skillful` is available to provide lazy-loaded skills.

## Required Tool Contract

- `skill_find "query"`
- `skill_use "skill_name"`
- `skill_resource skill_name="..." relative_path="..."`

## Recommended OpenCode Plugin Registration

Add plugin to OpenCode config:

```json
{
  "plugins": [
    "@zenobius/opencode-skillful"
  ]
}
```

## Recommended Skill Paths

- Global user skills: `~/.config/opencode/skills/`
- Project-local skills: `.opencode/skills/`

## Overlay Behavior

- Keep workflow docs (`01`-`09`) as policy source of truth.
- Use `skill_find` first for discovery, then `skill_use` for injection.
- Use `skill_resource` when only a specific template/reference is needed.

## Toolchain Note

`opencode-skillful` in this workspace is migrated to a Yarn-based workflow. Use `corepack yarn` for install, test, and build commands.
