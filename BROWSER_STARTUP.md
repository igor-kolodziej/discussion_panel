# Browser Startup Instructions

Use this when an agent needs to open and control ChatGPT through gstack browser in this workspace.

## Key Rule

Prefer the foreground headed-server path below. In this workspace, the normal `browse connect` flow can report `Mode: headed` briefly and then fall back to a non-visible `Mode: launched` session. Running the server in the foreground kept the headed browser stable.

## Paths

Workspace:

```bash
/Users/igor/Desktop/discussion_panel
```

Browse binary:

```bash
/Users/igor/.codex/skills/gstack/browse/dist/browse
```

Bun:

```bash
/Users/igor/.bun/bin/bun
```

Browser server source:

```bash
/Users/igor/.codex/skills/gstack/browse/src/server.ts
```

State file:

```bash
/Users/igor/Desktop/discussion_panel/.gstack/browse.json
```

## Start Clean

Run this before starting the headed browser if the browser state is stale, invisible, or stuck on `about:blank`.

```bash
cd /Users/igor/Desktop/discussion_panel

_STATE="/Users/igor/Desktop/discussion_panel/.gstack/browse.json"
if [ -f "$_STATE" ]; then
  _OLD_PID=$(grep -o '"pid":[0-9]*' "$_STATE" 2>/dev/null | grep -o '[0-9]*')
  [ -n "$_OLD_PID" ] && kill "$_OLD_PID" 2>/dev/null || true
  sleep 1
  [ -n "$_OLD_PID" ] && kill -9 "$_OLD_PID" 2>/dev/null || true
  rm -f "$_STATE"
fi

_PROFILE_DIR="$HOME/.gstack/chromium-profile"
for _LF in SingletonLock SingletonSocket SingletonCookie; do
  rm -f "$_PROFILE_DIR/$_LF" 2>/dev/null || true
done
```

## Start The Headed Browser Server

Run this in a long-running terminal session and keep it open while using the browser.

```bash
cd /Users/igor/Desktop/discussion_panel

BROWSE_HEADED=1 \
BROWSE_PORT=34567 \
BROWSE_SIDEBAR_CHAT=1 \
BROWSE_PARENT_PID=0 \
BROWSE_STATE_FILE=/Users/igor/Desktop/discussion_panel/.gstack/browse.json \
/Users/igor/.bun/bin/bun run /Users/igor/.codex/skills/gstack/browse/src/server.ts
```

Expected output includes:

```text
[browse] Launched headed Chromium with extension
[browse] Server running on http://127.0.0.1:34567
```

Do not close this terminal while work is ongoing. Closing it shuts down the browser server.

## Open ChatGPT

In a separate command session:

```bash
cd /Users/igor/Desktop/discussion_panel
/Users/igor/.codex/skills/gstack/browse/dist/browse goto https://chatgpt.com
/Users/igor/.codex/skills/gstack/browse/dist/browse focus
```

To open the pinned `Zero to One` custom GPT, open ChatGPT and click the pinned GPT in the sidebar. If the direct URL is known from the current browser session, it can be used, but do not hard-code old chatbot names or old URL slugs in prompts or docs.

```bash
/Users/igor/.codex/skills/gstack/browse/dist/browse snapshot -i
```

## Verify

After the foreground server is running, this should be safe:

```bash
/Users/igor/.codex/skills/gstack/browse/dist/browse status
```

Expected:

```text
Status: healthy
Mode: headed
```

If it says `Mode: launched` or `URL: about:blank`, stop and restart using the clean foreground-server path above.

Useful checks:

```bash
/Users/igor/.codex/skills/gstack/browse/dist/browse url
/Users/igor/.codex/skills/gstack/browse/dist/browse snapshot -i
/Users/igor/.codex/skills/gstack/browse/dist/browse text
```

## Important Avoidance Rules

- Do not rely on `browse connect` if the visible browser does not stay open.
- Do not repeatedly run ordinary `status` commands before the foreground headed server is started; that can autostart a non-headed `launched` session.
- Do not proceed with ChatGPT work unless `status` shows `Mode: headed`.
- Keep the foreground server terminal alive until all browser work is complete.
- Use `focus` after navigation if the browser is open but not visible.

## Stop The Browser

When finished, stop the foreground server with `Ctrl-C` in the terminal running `server.ts`.

Expected shutdown output:

```text
^C[browse] Shutting down...
```
