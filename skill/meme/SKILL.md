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
pip install makememe
# or: uv tool install makememe
```

## Workflow

1. **Pick a template.** If you don't already know a valid template id, list them:

   ```bash
   meme --list --json
   ```

   Common ids: `drake`, `db` (distracted boyfriend), `buttons` (two buttons),
   `gru` (gru's plan), `cmm` (change my mind), `fine` (this is fine),
   `success` (success kid), `rollsafe`, `same` (same picture), `regret`.

2. **Generate.** Pass the template id then the caption lines in order. Use
   `--json` so you can capture the output path reliably:

   ```bash
   meme drake "writing code by hand" "asking the meme cli" --json
   ```

   Output:

   ```json
   { "path": "meme.png", "bytes": 12345, "url": "https://api.memegen.link/..." }
   ```

3. **Tell the user the path** (and show the image if the surface supports it).

## Key flags

- `-o out.png` — choose the output filename (default `meme.png`). Pick a
  descriptive name when generating several.
- `--bg <image-url>` — use a custom background image instead of a template;
  pass caption lines as usual.
- `--ext png|jpg|webp|gif` — output format.
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
meme drake "old way" "new way" -o drake.png --json
meme same "after I sold" "if I held" "same picture" --json
meme cmm "tabs are better than spaces" --json
meme --bg https://example.com/cat.png "_" "DEPLOY ON FRIDAY" --json
```
