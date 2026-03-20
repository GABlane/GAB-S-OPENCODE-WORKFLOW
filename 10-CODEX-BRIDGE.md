GAB'S WORKFLOW - Codex Bridge Protocol

Purpose
- Claude Code plans. Codex executes.
- Communication happens via a shared folder: ~/ai-bridge/
- Both processes run in separate terminals and never block each other.

Folder structure

~/ai-bridge/
  inbox/    - Claude Code writes task files here; Codex picks them up
  outbox/   - Codex writes result files here; Claude Code reads them
  archive/  - Completed task pairs are moved here after synthesis
  status.json - Current queue state for quick polling

Task file (Claude Code writes to inbox/)

Filename: TASK-{id}.md
Example:  inbox/TASK-001.md

---
task_id: TASK-001
created: <ISO timestamp>
mode: L1 | L2 | L3
priority: low | normal | high
status: pending
project: <project name if active>
---

## Context
<why this task exists; what the user asked>

## Steps
1. <step>
2. <step>

## Files to Touch
- path/to/file.ts
- path/to/other.go

## Expected Output
<what done looks like; test commands to run; acceptance criteria>

Result file (Codex writes to outbox/)

Filename: TASK-{id}.result.md
Example:  outbox/TASK-001.result.md

---
task_id: TASK-001
completed: <ISO timestamp>
status: done | failed | needs_review
---

## Changes Made
<summary of what was done>

## Files Changed
- path/to/file.ts
- path/to/other.go

## Tests Run
<commands run and pass/fail summary>

## Notes / Blockers
<anything Claude Code needs to know for next steps>

ID convention
- Use zero-padded sequential integers: TASK-001, TASK-002, ...
- Maintain counter in status.json queue array.

Claude Code responsibilities
- Always write a TASK file before any coding work; never code inline.
- Set status: pending in the task frontmatter.
- Update status.json with the new task.
- After result appears in outbox/, read it and synthesize.
- Move both files to archive/ after synthesis.
- If status is failed or needs_review, write a follow-up TASK file.

Codex responsibilities
- Watch inbox/ for new TASK-*.md files.
- Execute steps as specified; do not deviate without writing a note.
- Write result to outbox/ using the exact task_id.
- Do not modify inbox/ files.

Status.json schema

{
  "last_updated": "<ISO timestamp>",
  "active_task": "TASK-001" | null,
  "queue": ["TASK-002", "TASK-003"]
}

Failure handling
- If Codex writes status: failed, Claude Code writes a new task with revised steps.
- If Codex writes status: needs_review, Claude Code reads notes and decides: fix plan or ask user.
- If no result appears after reasonable wait, Claude Code checks with user before re-queuing.

Session cleanup (automatic)
- On every Claude Code session stop, a hook runs automatically:
  1. Writes ~/ai-bridge/archive/SESSION-{timestamp}.md with the project dir and inbox file list
  2. Deletes all TASK-*.md files from inbox/
  3. Resets status.json to initial state
- This ensures each new session starts with a clean inbox regardless of project.
- Archive retains full history of what was pending at each session end.
- Hook script: ~/.claude/hooks/session-end-bridge.sh
- Registered in: ~/.claude/settings.json under Stop event

Override
- User can say "do it yourself" to have Claude Code execute inline (L1 tasks only).
- Use !ForceModel codex-large before task description to force Codex tier escalation.
