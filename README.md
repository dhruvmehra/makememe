# meme

A tiny, zero-dependency CLI for generating memes via the free
[memegen.link](https://memegen.link) API. No API key, no signup, stdlib-only.

Built to be **agent-friendly**: predictable stdout, a `--json` mode, and a
bundled Claude Code skill so coding agents (Claude Code, Codex, etc.) can drive
it directly.

```bash
meme drake "not reading docs" "reading docs" -o out.png
```

## Install

Requires Python 3.8+.

```bash
pip install makememe
# or, as an isolated tool:
uv tool install makememe      # or: pipx install makememe
```

Run once without installing:

```bash
uvx --from makememe meme drake "a" "b"
```

## Usage

```bash
meme <template> "top line" "bottom line" [-o out.png]
```

| Flag | Meaning |
|------|---------|
| `-o, --out` | output file (default `meme.png`) |
| `--bg URL` | use a custom background image instead of a template |
| `--ext` | `png` (default), `jpg`, `webp`, or `gif` |
| `--style` / `--font` | template style variant / font override |
| `--print-url` | print the image URL, don't download |
| `--json` | machine-readable output (for scripts/agents) |
| `--list` | list available template ids |

### Examples

```bash
meme drake "manual deploys" "ci/cd"
meme same "after I sold" "if I held" "same picture"
meme --bg https://example.com/pic.png "_" "DODGED"
meme regret "SOLD @ 620" "NOW 780 (+26%)" --print-url
meme --list
meme --list --json
```

### Text that starts with `-`

If a caption line begins with `-` (e.g. `"-26%"`), put `--` before your lines so
it isn't parsed as a flag:

```bash
meme regret --json -- "-26%" "WHY"
```

(Put flags like `--json`/`-o` *before* the `--`.)

## For agents (Claude Code / Codex / scripts)

The tool is designed to be parsed:

- **Plain mode** prints *only the output path* to stdout (status goes to stderr),
  so `path=$(meme drake "a" "b")` just works.
- **`--json` mode** prints a single JSON object:

  ```json
  { "path": "meme.png", "bytes": 12345, "url": "https://api.memegen.link/..." }
  ```

  `--list --json` returns the template catalog as JSON; `--print-url --json`
  returns `{"url": "..."}`; failures return `{"error": "...", "url": "..."}`
  with a non-zero exit code.

Typical agent flow:

```bash
meme --list --json                       # discover template ids
meme drake "old way" "new way" --json    # generate, capture the path
```

### Claude Code skill

A ready-made skill lives in [`skill/meme/`](skill/meme/SKILL.md). Install it so
Claude Code auto-discovers the tool:

```bash
# user-level (all projects)
mkdir -p ~/.claude/skills
cp -r skill/meme ~/.claude/skills/meme

# or project-level
mkdir -p .claude/skills
cp -r skill/meme .claude/skills/meme
```

Then just ask Claude Code things like *"make a drake meme about writing tests"*
and it will call `meme` for you.

## Robustness

The CLI is built to fail gracefully, never with a raw traceback:

- Network errors, dead hosts, bad template ids (404), oversized text (414), and
  non-image backgrounds (415) all exit non-zero with a one-line message — and
  **no partial/garbage file is written**.
- `Ctrl-C` exits cleanly (code 130); piping into `head` etc. won't spew a
  `BrokenPipeError`.
- Arbitrary text — emoji, CJK, `% # & / ? " \`, tabs, control chars, 10k-char
  lines — is escaped safely.

Run the test suite (stdlib only, no network needed):

```bash
python -m unittest discover -s tests
```

## How it works

It builds a memegen.link URL from your template + text (handling all the fiddly
path-segment escaping — spaces, `_`, `-`, `?`, `/`, `%`, etc.), downloads the
image, and saves it. That's the whole trick.

## License

MIT
