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

1. **Choose the most apt template — match the joke's *shape*, not a default.**

   The single most important step. Don't reach for `drake` every time — it only
   fits "rejecting A, preferring B." First work out the *rhetorical structure*
   of the user's idea, then pick the template whose format matches it. The
   catalog has ~200 templates; here is the high-value map by structure:

   | The idea is…                                          | Template id   | Lines |
   |-------------------------------------------------------|---------------|-------|
   | Rejecting A, preferring B                             | `drake`       | 2 |
   | Tempted away from the current thing by a shinier one  | `db`          | 3 |
   | Agonizing between two conflicting options             | `ds`          | 3 |
   | Swerving last-second to pick B over the obvious A     | `exit`        | 3 |
   | A multi-step plan whose last step backfires           | `gru`         | 4 |
   | Stating a hot take, daring you to argue               | `cmm`         | 1 |
   | Pretending all is fine amid disaster                  | `fine`        | 2 |
   | A small, satisfying win / "nailed it"                 | `success`     | 2 |
   | Galaxy-brain "can't have the problem if you avoid it" | `rollsafe`    | 2 |
   | Escalating "increasingly enlightened" (often ironic)  | `gb`          | 4 |
   | Two things claimed different but actually identical   | `same`        | 3 |
   | Immediate regret right after a choice                 | `regret`      | 2 |
   | Mocking a statement by repeating it sarcastically     | `spongebob`   | 2 |
   | An accusation vs. a smug, dismissive reply            | `woman-cat`   | 2 |
   | "One does not simply X"                               | `mordor`      | 2 |
   | "Not sure if X… or just Y" (suspicion)                | `fry`         | 2 |
   | "False." + a blunt correction                         | `dwight`      | 2 |
   | A forced smile hiding inner pain                      | `harold`      | 2 |
   | Absurd gains from a dumb move                          | `stonks`      | 2 |
   | "X, X everywhere"                                     | `buzz`        | 2 |
   | "I'm not saying it's X… but it's X"                   | `aag`         | 2 |
   | Smug delight at chaos you caused                      | `disastergirl`| 2 |
   | Crude version vs. fancy/refined version of same thing | `pooh`        | 2 |
   | An escalating back-and-forth argument                 | `chair`       | 6 |
   | "Y U NO [do thing]"                                   | `yuno`        | 2 |

   If none of these fit the joke, **browse the full catalog** instead of forcing
   a bad fit:

   ```bash
   meme --list --json     # ~200 templates; scan the titles for a better match
   ```

   **Always verify the chosen id with `meme --list --json` before using it** —
   guessing ids (e.g. `buttons`, `twobuttons`) leads to 404s. The map above is
   accurate, but confirm anything you pull from memory.

2. **Write the funniest version — reason before you render.** Don't ship the
   first phrasing that comes to mind. Briefly draft 2–3 caption options in your
   head and pick the funniest, then render only that one. What makes it land:

   - **Specificity beats generic.** "the `useEffect` that runs twice" is funnier
     than "a bug." Reach for the concrete, in-context detail.
   - **Punchy and short.** Meme text is read in a second — trim filler words,
     keep each line tight, favor a sharp last word.
   - **Match the template's voice.** Lean into the format's built-in attitude
     (smug `rollsafe`, deadpan `fine`, escalating `gru`, mocking `spongebob`).
   - **Respect the structure.** The funny comes from the *contrast* the template
     sets up — make line A and line B actually play off each other.
   - **Use the user's name/specifics verbatim.** If the user named a person,
     team, tool, or thing ("make a meme about *Raj* and code reviews"), put that
     exact name **into the caption text** — don't genericize it to "my coworker."
     Names and inside-references are what make a meme land for its audience.

3. **Get the URL (default).** Pass the chosen template id with `-t` (as a flag,
   not the leading word) then the caption lines in the template's natural order,
   and use `--print-url`. This returns a public, permanent memegen.link URL — no
   file is downloaded:

   ```bash
   meme -t ds "ship it Friday" "wait till Monday" --print-url
   ```

   Output (just the URL):

   ```
   https://api.memegen.link/images/ds/ship_it_Friday/wait_till_Monday.png
   ```

   Mind the line order for the template you picked — e.g. `db` reads
   *new temptation / you / current thing*; `exit` reads *straight road / exit
   ramp / the car*; `fine` is *top speech / bottom "this is fine"*. If a render
   looks off, it's usually line order or count — re-check against `--list`.

   Using `-t` matters: every call starts with the same `meme -t ...` prefix, so
   the user only has to approve the command **once** — not once per template.

4. **Give the user the URL** as a clickable link — they can open it in a browser
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

Each picks the template that fits the joke's shape — not all drake:

```bash
meme -t drake "old way" "new way" --print-url                       # reject A, prefer B
meme -t ds "merge to main" "open another PR" --print-url            # agonizing between two options
meme -t fine "prod is down" "this is fine" --print-url              # disaster, pretending it's ok
meme -t gru "write the tests" "tests fail" "fix the code" "tests still fail" --print-url   # plan backfires
meme -t same "staging" "prod" "they're the same picture" --print-url  # claimed different, identical
meme -t cmm "tabs are better than spaces" --print-url               # one-line hot take
meme -t mordor "one does not simply" "deploy on Friday" --print-url # "one does not simply X"
meme --bg https://example.com/cat.png "_" "DEPLOY ON FRIDAY" --print-url  # custom background
meme -t success "fixed the bug" "on the first try" --open           # only when the user wants a file
```
