# makememe — a meme CLI your coding agent can drive

A tiny, **zero-dependency** meme generator built for **coding agents and CI**.
It ships a bundled Claude Code skill, so you can just say *"drop a 'this is fine'
meme on the PR"* and the agent runs it — and a copy-paste GitHub Action that
memes your build status. No API key, no signup, stdlib-only (wraps the free
[memegen.link](https://memegen.link) API).

![demo](docs/demo.gif)

**Let your agent meme.** Install once, and Claude Code / Codex drive it for you:

```text
you:   make a "this is fine" meme about prod being down
agent: $ meme -t fine "prod is down" "this is fine" --print-url
       → https://api.memegen.link/images/fine/prod_is_down/this_is_fine.png
```

…and that URL renders straight into your PR or Slack — no download, no hosting:

<p>
  <img src="https://api.memegen.link/images/fine/prod_is_down/this_is_fine.png" height="170" alt="this is fine meme">
  <img src="https://api.memegen.link/images/drake/manual_deploys/ci~scd.png" height="170" alt="drake meme">
</p>

**Meme your CI.** A `this is fine` meme on every red build — the complete
copy-paste workflow is in [Integrations](#integrations) below:

```bash
url=$(meme -t fine "tests failed" "this is fine" --print-url)
gh pr comment "$PR" --body "![meme]($url)"
```

It's a normal CLI too — `meme drake "manual deploys" "ci/cd"` works from any
terminal. See [Usage](#usage).

## Install

Requires Python 3.8+. Easiest is [uv](https://docs.astral.sh/uv/) (installs
the `meme` command in its own isolated environment):

```bash
uv tool install makememe          # or: pipx install makememe
```

Update later with:

```bash
uv tool upgrade makememe
```

Run once without installing anything:

```bash
uvx --from makememe meme drake "a" "b"
```

(If you specifically want pip: `python3 -m pip install makememe`.)

Check the version anytime:

```bash
meme --version
```

## Usage

```bash
meme <template> "top line" "bottom line" [-o out.png]
```

| Flag | Meaning |
|------|---------|
| `-t, --template` | template id as a flag (alternative to the positional). Agents should use this so a single permission approval covers every template |
| `-o, --out` | output file (default: a unique file in a temp folder, so it never writes into your current directory) |
| `--bg URL` | use a custom background image instead of a template |
| `--ext` | `png` (default), `jpg`, `webp`, or `gif` |
| `--style` / `--font` | template style variant / font override |
| `--open` | open the finished image in your default viewer |
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

## Integrations

For sharing (CI, chat, comments) you usually want the **public URL**, not a
local file — `--print-url` returns a permanent memegen.link URL you can embed
anywhere with `![meme](url)`. No download, no image hosting.

**GitHub Actions → PR comment.** Drop this in `.github/workflows/pr-meme.yml`,
change the one test line to your command, and every PR gets a success / "this is
fine" meme based on whether tests passed. That's the whole setup — no secrets,
no image hosting (`GITHUB_TOKEN` is built in):

```yaml
name: pr-meme
on: pull_request
permissions:
  pull-requests: write          # to post the comment
jobs:
  meme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        id: tests
        run: echo "replace this with your test command (e.g. pytest, npm test)"
      - name: Comment a meme with the result
        if: always()            # run even when tests fail
        run: |
          pip install --quiet makememe
          if [ "${{ steps.tests.outcome }}" = "success" ]; then
            url=$(meme -t success "tests" "passed" --print-url)
          else
            url=$(meme -t fine "tests failed" "this is fine" --print-url)
          fi
          gh pr comment "${{ github.event.pull_request.number }}" --body "![meme]($url)"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

(Also saved at [`examples/pr-meme.yml`](examples/pr-meme.yml).)

**Slack/Discord:** post a `--print-url` URL to a channel; it auto-unfurls into a
preview.

```bash
url=$(meme -t success "build" "passed" --print-url)   # -> public URL, embed it anywhere
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
  { "path": "/tmp/makememe/meme-ab12cd.png", "bytes": 12345, "url": "https://api.memegen.link/..." }
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

The package bundles a Claude Code skill. After installing, run one command to
make Claude Code auto-discover the tool:

```bash
meme --install-skill              # installs into ~/.claude/skills/meme/ (all projects)
meme --install-skill --project    # or into ./.claude/skills/meme/ (this repo only)
```

Restart Claude Code, then just ask things like *"make a drake meme about
writing tests"* and it will call `meme` for you.

(Other agents like Codex don't use this skill format — they discover everything
through `meme --help` and `meme --list`, which already works out of the box.)

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
