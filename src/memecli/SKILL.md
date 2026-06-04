---
name: meme
description: Generate meme images from a template and caption text using the `meme` CLI (a wrapper over the free memegen.link API). Use whenever the user asks to make/create/generate a meme, add a caption to a meme template, or wants a funny image with top/bottom text. Handles popular templates (drake, distracted boyfriend, two buttons, etc.) and custom background images.
---

# meme

Generate memes from the command line. The `meme` command wraps the free
[memegen.link](https://api.memegen.link) API — no API key needed.

## Prerequisite

The `meme` command must be installed. Check with `meme --list`. If it's missing,
install it:

```bash
uv tool install makememe
# or: pipx install makememe
```

## Workflow

1. **Pick a template.** If you don't already know a valid template id, list them:

   ```bash
   meme --list --json
   ```

   Common ids: `drake`, `db` (distracted boyfriend), `ds` (daily struggle /
   "two buttons"), `gru` (gru's plan), `cmm` (change my mind),
   `fine` (this is fine), `success` (success kid), `rollsafe`,
   `same` (same picture), `regret`.

   **Always verify an id with `meme --list --json` before using it** — guessing
   ids (e.g. `buttons`, `twobuttons`) leads to 404s. When unsure, list first.

2. **Generate.** Pass the template id with `-t` (as a flag, not the leading
   word) then the caption lines in order. Always use `--json` (reliable output
   path) and `--open` (opens the finished meme in the user's default viewer).

   Using `-t` matters: every call starts with the same `meme -t ...` prefix, so
   the user only has to approve the command **once** — not once per template.

   ```bash
   meme -t drake "writing code by hand" "asking the meme cli" --json --open
   ```

   Output:

   ```json
   { "path": "/tmp/makememe/meme-ab12cd.png", "bytes": 12345, "url": "https://api.memegen.link/..." }
   ```

3. **Tell the user the path.** The `--open` flag already popped the image open
   for them; just report where it was saved.

## Key flags

- By default the image is saved to a temp folder (`<tmp>/makememe/`) with a
  unique name, so it never clutters the user's working directory. The path is
  in the output — report it to the user. Use `-o path.png` only if the user
  wants it saved somewhere specific.
- `--bg <image-url>` — use a custom background image instead of a template;
  pass caption lines as usual.
- `--ext png|jpg|webp|gif` — output format.
- `--open` — open the finished image in the user's default viewer (use this so
  they can see the meme).
- `--print-url` — get the image URL without downloading.
- `--json` — machine-readable output (always prefer this when scripting).

## Tips

- Number of caption lines depends on the template (`--list` shows each
  template's `lines` count). Most use 2 (top/bottom).
- For an empty line, pass `"_"` (memegen renders it blank).
- Text escaping (spaces, `?`, `/`, `%`, emoji, etc.) is handled automatically —
  just pass natural text in quotes.
- If a caption line starts with `-` (e.g. `"-26%"`), insert `--` before the
  lines so it isn't read as a flag: `meme regret --json -- "-26%" "WHY"`.
  (Flags like `--json`/`-o` go before the `--`.)
- If a download fails, the JSON output includes the `url` and `error` — inspect
  the URL to debug the template id or line count.

## Examples

```bash
meme -t drake "old way" "new way" --json --open
meme -t same "after I sold" "if I held" "same picture" --json --open
meme -t cmm "tabs are better than spaces" --json --open
meme --bg https://example.com/cat.png "_" "DEPLOY ON FRIDAY" --json --open
```
