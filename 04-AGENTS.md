GAB'S WORKFLOW - Agents Catalog

Agent list (Task tool subagents)

| Agent | Description | Notes |
| --- | --- | --- |
| general | General-purpose agent for researching complex questions and executing multi-step tasks. | Use for multiple units of work in parallel. |
| explore | Fast agent specialized for exploring codebases. | Use for finding files or understanding code; specify thoroughness: quick, medium, very thorough. |
| build-small | Fast coding agent for small edits and quick fixes. | Use for small changes. |
| build-large | High-capability coding agent for large refactors and risky changes. | Use for big or risky work. |
| planner | Expert planning specialist for complex features and refactoring. | Use for implementation planning and architecture changes. |
| architect | Software architecture specialist for system design, scalability, and technical decision-making. | Use for system design. |
| code-reviewer | Expert code review specialist. Reviews code for quality, security, and maintainability. | Use immediately after writing or modifying code. |
| security-reviewer | Security vulnerability detection and remediation specialist. | Use after writing code that handles user input, auth, API endpoints, or sensitive data. |
| tdd-guide | Test-driven development specialist enforcing write-tests-first methodology. | Use when writing new features, fixing bugs, or refactoring. |
| build-error-resolver | Build and TypeScript error resolution specialist. | Use when build fails or type errors occur. |
| e2e-runner | End-to-end testing specialist using Playwright. | Use for critical user flows. |
| doc-updater | Documentation and codemap specialist. | Use to update docs and codemaps. |
| refactor-cleaner | Dead code cleanup and consolidation specialist. | Use to remove unused code and refactor. |
| go-reviewer | Expert Go code reviewer. | Focuses on idiomatic Go, concurrency, error handling, performance. |
| go-build-resolver | Go build, vet, and compilation error resolution specialist. | Fixes Go build errors with minimal diffs. |
| database-reviewer | PostgreSQL database specialist. | Query optimization, schema design, security, performance, Supabase best practices. |

When to use Task tool
- When a task matches an agent description.
- When executing a custom slash command.
- When you need an autonomous multi-step effort.

When NOT to use Task tool
- If you want to read a specific file path (use Read).
- If you want to find files by pattern (use Glob).
- If you want to search specific content (use Grep).
- If the task is not related to agent descriptions.

Task tool usage notes
- Launch multiple agents concurrently when possible.
- Each agent starts with fresh context unless task_id is provided.
- Provide detailed task description and expected output.
- Tell the agent whether to write code or only research.
