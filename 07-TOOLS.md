GAB'S WORKFLOW - Tools

Available tools

| Tool | Purpose | Key rules |
| --- | --- | --- |
| question | Ask user questions during execution | Use for clarifying preferences or decisions. If custom enabled, a "Type your own answer" option is added automatically. |
| bash | Terminal operations (git, npm, docker, scripts) | Avoid file ops if a specialized tool exists. Verify parent directory exists before creating files/dirs. Use workdir instead of `cd`. Quote paths with spaces. Avoid `find`, `grep`, `cat`, `head`, `tail`, `sed`, `awk`, `echo` unless necessary. |
| read | Read a file or directory | Use absolute paths. Supports offset and limit. |
| glob | File pattern matching | Use for filename searches. |
| grep | Content search by regex | Use for content searches; supports include patterns. |
| task | Launch specialized subagents | Use for complex tasks or slash commands. Provide detailed prompt and expected output. |
| webfetch | Fetch URL content | Use for web content retrieval. |
| todowrite | Manage structured task lists | Use for complex multi-step tasks. Do not use for single trivial tasks. |
| skill | Load a specialized skill | Use when task matches skill description. |
| apply_patch | Edit or add files using patch format | Add or update files; use for single-file edits by default. |
| skill_use | Load one or more skills | Provide array of skill names. |
| skill_find | Search skills | Use to locate skills by query. |
| skill_resource | Read a resource file from a skill | Provide skill name and relative path. |
| multi_tool_use.parallel | Run multiple tools concurrently | Only for independent calls. |

Tool selection guidance
- Prefer specialized tools over shell for file operations.
- Use Read to view files, apply_patch to edit files.
- Use Glob to find files, Grep to search contents.
- Use Bash for terminal operations only when needed.
- Run tool calls in parallel when independent; use a single Bash call for sequential dependencies.

Bash tool usage (highlights)
- Use `workdir` instead of `cd`.
- Quote paths with spaces using double quotes.
- Check parent directory exists before creating files or directories.
- Avoid interactive git commands and flags like `-i`.

Git commit workflow (only when user explicitly requests)
- Never update git config.
- Never run destructive git commands unless explicitly requested.
- Never skip hooks unless explicitly requested.
- Avoid `git commit --amend` unless user explicitly asked and all safety conditions are met.
- If commit fails due to hook, fix issue and create a NEW commit.
- Never commit secrets (warn user if asked to commit such files).

Pull request workflow (only when user explicitly requests)
- Use `gh` for GitHub tasks.
- Gather status, diff, log, and base-branch comparison before creating PR.
- Push branch with `-u` if needed.
- Create PR with a Summary section in the body via heredoc.
- Return PR URL when done.
