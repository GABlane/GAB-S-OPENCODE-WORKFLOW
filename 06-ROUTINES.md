GAB'S WORKFLOW - Routines

Priority arbitration
Trigger
- Use when user asks: "what should i work on now / what's next / prioritize".

Inputs
- If active project exists: use that project's tasks.md first.
- Always include global tasks.md.
- Include other projects only if user asks "all projects".
- If required files are missing or inaccessible, ask user to paste them.

Scoring
- Score each candidate 0 to 10: U (urgency), I (impact), E (effort), D (dependency).
- D: +2 if unblocks others, -3 if blocked now.
- Total = U + I + D - E.

Choose
- Pick top 1 by total.
- Show next 2 backups.
- If top totals are within 2 points, ask one question: "quick wins or high impact?"

Transparency
- Do not show scores unless asked.
- If asked, show a small table: task | U | I | D | E | total.

Output format
- Pick now: <task> -- <1-line why>
- Next: <task>, <task>
- If you have 15 mins: <micro-task>
- If a timebox is given, apply timebox behavior.

Focus lock
Activation
- Activate when a task is selected or when user says "let's work on X".
- Set Focused task = X. Show in session header (L2 or L3 only).

Locked behavior
- Keep suggestions aligned to Focused task.
- If request is unrelated: ask "pause or switch focus?"
- Do not auto-switch tasks.

Stale task detection
- If a new task is selected or project switch occurs without explicit "continue focus":
  ask once: "still focused on <task>?"
- If user confirms yes, continue.
- If no or no response after one more exchange, clear focus and announce it.

Unlock
- Unlock only when user says "pause / switch task / change focus / reprioritize / switch project".
- Unlock automatically if task is completed or blocked.
- Announce: "focus cleared."

Timebox behavior
- If a timebox is given, prefer tasks that fit it.
- If focused task does not fit, ask whether to continue or switch.
- If effort is unknown, infer lightly and say it's an estimate.

Morning routine
- Run priority arbitration (active project + global).
- Output exactly:
  Pick now:
  Next:
  If you have 15 mins:
  Focus suggestion: <1> -> ask "lock focus on this?"

EOD routine
- Output:
  Touched today:
  Completed:
  In progress:
  Blockers:
  Journal (1 line):
- If timebox given, apply timebox behavior.
- Then ask: "what should i mark done and what carries over?"
- After user confirms:
  - mark confirmed done items with checkmark in tasks.md
  - move carry-overs to top of backlog with a "-> carry" tag
  - do not modify tasks.md until user confirms the list
