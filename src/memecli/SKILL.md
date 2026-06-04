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

2. **Get the URL (default).** Pass the template id with `-t` (as a flag, not the
   leading word) then the caption lines, and use `--print-url`. This returns a
   public, permanent memegen.link URL — no file is downloaded:

   ```bash
   meme -t drake "writing code by hand" "asking the meme cli" --print-url
   ```

   Output (just the URL):

   ```
   https://api.memegen.link/images/drake/writing_code_by_hand/asking_the_meme_cli.png
   ```

   Using `-t` matters: every call starts with the same `meme -t ...` prefix, so
   the user only has to approve the command **once** — not once per template.

3. **Give the user the URL** as a clickable link — they can open it in a browser
   or paste it into Slack/GitHub (it renders inline with `![meme](url)`). Don't
   download a file unless they ask for one (see "Saving a local file" below).

## Saving a local file

Only when the user explicitly wants a file (to attach it, edit it, or see it pop
open) — drop `--print-url` and instead:

```bash
meme -t drake "a" "b" --open          # saves to a temp folder AND opens it in the viewer
meme -t drake "a" "b" -o ~/meme.png   # save to a specific path
```

By default (without `-o`) a downloaded file goes to a temp folder
(`<tmp>/makememe/`) with a unique name, so it never clutters the user's working
directory.

## Key flags

- `--print-url` — return the public URL instead of downloading (the default
  choice; prefer this).
- `--open` — download and open the image in the user's default viewer.
- `-o path.png` — save the download to a specific path.
- `--bg <image-url>` — use a custom background image instead of a template;
  pass caption lines as usual.
- `--ext png|jpg|webp|gif` — output format.
- `--json` — machine-readable output (use when you need to parse it in a script).

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
meme -t drake "old way" "new way" --print-url
meme -t same "after I sold" "if I held" "same picture" --print-url
meme -t cmm "tabs are better than spaces" --print-url
meme --bg https://example.com/cat.png "_" "DEPLOY ON FRIDAY" --print-url
meme -t drake "save me" "to a file" --open          # only when the user wants a file
```
