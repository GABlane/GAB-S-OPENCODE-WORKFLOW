GAB'S WORKFLOW - Inbox Auto Worker

Goal
- Instantly detect new `TASK-*.md` files in `~/ai-bridge/inbox`.
- Notify you on pickup and completion.
- Automatically execute each task with `codex exec`.

Worker script
- Path: `scripts/ai_bridge_worker.py`

Quick start (foreground)

```bash
python3 scripts/ai_bridge_worker.py
```

Quick start (background)

```bash
nohup python3 scripts/ai_bridge_worker.py > ~/ai-bridge/worker.log 2>&1 &
```

Stop background worker

```bash
pkill -f "scripts/ai_bridge_worker.py"
```

What it does
- Polls inbox every 0.5s by default.
- Uses a single-instance lock file at `~/ai-bridge/.worker.lock` (prevents duplicate workers).
- Picks up pending task files (`TASK-*.md`) that do not yet have matching outbox result.
- Updates `~/ai-bridge/status.json`:
  - `active_task` while processing
  - `queue` with remaining pending tasks
- Calls `codex exec --full-auto` to process the task.
- Writes execution logs to `~/ai-bridge/archive/TASK-###.worker.log`.
- If Codex exits without creating result file, writes fallback failed result to outbox.

Notifications
- Uses macOS Notification Center via `osascript`.
- Disable with `--no-notify`.

Useful flags

```bash
# Run once over current pending tasks, then exit
python3 scripts/ai_bridge_worker.py --once

# Dry-run (no codex execution)
python3 scripts/ai_bridge_worker.py --dry-run --once

# Custom workspace and poll interval
python3 scripts/ai_bridge_worker.py \
  --workspace-dir ~/GAB-S-OPENCODE-WORKFLOW \
  --poll-interval 0.3
```

Auto-start at login (launchd)

1. Save this plist as `~/Library/LaunchAgents/com.gab.ai-bridge-worker.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.gab.ai-bridge-worker</string>

    <key>ProgramArguments</key>
    <array>
      <string>/usr/bin/python3</string>
      <string>/Users/gearworxdev/GAB-S-OPENCODE-WORKFLOW/scripts/ai_bridge_worker.py</string>
    </array>

    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/Users/gearworxdev/ai-bridge/worker.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/gearworxdev/ai-bridge/worker.err.log</string>
  </dict>
</plist>
```

2. Load it:

```bash
launchctl load ~/Library/LaunchAgents/com.gab.ai-bridge-worker.plist
```

3. Restart after edits:

```bash
launchctl unload ~/Library/LaunchAgents/com.gab.ai-bridge-worker.plist
launchctl load ~/Library/LaunchAgents/com.gab.ai-bridge-worker.plist
```
