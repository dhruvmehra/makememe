#!/usr/bin/env python3
"""
meme - a tiny CLI over the free memegen.link API.

Builds a meme image URL from a template + text lines, downloads it, saves an
image. No API key, no third-party dependencies (Python stdlib only). Handles URL
escaping so you never hit the bare-% problem.

Examples:
    meme drake "not reading docs" "reading docs"
    meme regret "SOLD IRCTC @ Rs620" "NOW Rs780 (+26%) WHY"
    meme same "after I sold" "if I held" "same picture"
    meme --bg https://example.com/pic.png "_" "DODGED"
    meme drake "a" "b" --print-url        # just print the URL, don't download
    meme drake "a" "b" --json             # machine-readable output for agents
    meme --list                           # list available template ids
    meme --list --json                    # template ids as JSON

Find templates: https://api.memegen.link/templates/  (or `meme --list`)
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

API = "https://api.memegen.link"


def get_version():
    """Read the installed package version; fall back gracefully from source."""
    try:
        from importlib.metadata import version
        return version("makememe")
    except Exception:
        return "0.0.0+source"


def install_skill(project=False):
    """Copy the bundled Claude Code skill into ~/.claude/skills/meme/ (or ./.claude
    with project=True). Returns the path written."""
    try:
        from importlib.resources import files
        content = files("memecli").joinpath("SKILL.md").read_text(encoding="utf-8")
    except Exception:
        # running from a source checkout without installed metadata
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "SKILL.md"), encoding="utf-8") as f:
            content = f.read()
    base = os.getcwd() if project else os.path.expanduser("~")
    dest_dir = os.path.join(base, ".claude", "skills", "meme")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "SKILL.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)
    return dest


# memegen path-segment escaping. Order matters: escape the escape chars first.
# Confirmed from the API: space->_, _->__, -->--, ?->~q, newline->~n, "->''
# Others use memegen's documented tilde codes; verify with --print-url if unsure.
def escape(text):
    if text == "":
        return "_"  # memegen renders an empty line as a single underscore
    text = text.replace("_", "__").replace("-", "--")
    text = text.replace(" ", "_").replace("\n", "~n")
    text = text.replace("?", "~q").replace('"', "''").replace("/", "~s")
    # let quote percent-encode the rest (%, #, etc) - memegen decodes %25 reliably.
    # keep the memegen tokens we just produced intact.
    return urllib.parse.quote(text, safe="_~'.!*()")


def build_url(template, lines, ext="png", bg=None, style=None, font=None):
    parts = [escape(l) for l in lines] if lines else ["_"]
    base = "custom" if bg else template
    path = "/".join(parts)
    url = f"{API}/images/{base}/{path}.{ext}"
    q = {}
    if bg:
        q["background"] = bg
    if style:
        q["style"] = style
    if font:
        q["font"] = font
    if q:
        url += "?" + urllib.parse.urlencode(q)
    return url


def get_templates(timeout=20):
    req = urllib.request.Request(
        f"{API}/templates/", headers={"User-Agent": "meme-cli"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def list_templates(as_json=False):
    data = get_templates()
    if as_json:
        slim = [
            {"id": t["id"], "lines": t.get("lines"), "name": t["name"]}
            for t in data
        ]
        print(json.dumps(slim, indent=2))
        return
    for t in data:
        print(f"{t['id']:<18} {t.get('lines', '?')} lines  {t['name']}")


def download(url, out, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "meme-cli"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    with open(out, "wb") as f:
        f.write(data)
    return len(data)


def build_parser():
    ap = argparse.ArgumentParser(
        prog="meme", description="Generate a meme via memegen.link.",
        epilog="Tip: if a text line starts with '-' (e.g. \"-26%\"), put '--' "
               "before your lines so it isn't read as a flag:\n"
               "  meme regret --json -- \"-26%\" \"WHY\"",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version",
                    version=f"%(prog)s {get_version()}")
    ap.add_argument("--install-skill", action="store_true",
                    help="install the Claude Code skill into ~/.claude/skills/meme/ and exit")
    ap.add_argument("--project", action="store_true",
                    help="with --install-skill: install into ./.claude/skills/ instead of your home dir")
    ap.add_argument("template", nargs="?",
                    help="template id (see --list), or any id when using --bg")
    ap.add_argument("lines", nargs="*", help="text lines, in order")
    ap.add_argument("-o", "--out", default="meme.png",
                    help="output file (default meme.png)")
    ap.add_argument("--bg",
                    help="custom background image URL (uses the 'custom' template)")
    ap.add_argument("--ext", default="png", choices=["png", "jpg", "webp", "gif"])
    ap.add_argument("--style", help="template style variant, if any")
    ap.add_argument("--font", help="font name (see /fonts/)")
    ap.add_argument("--print-url", action="store_true",
                    help="print the URL and exit, no download")
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable JSON (good for agents/scripts)")
    ap.add_argument("--list", action="store_true",
                    help="list template ids and exit")
    return ap


def _run(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)

    if args.install_skill:
        try:
            dest = install_skill(project=args.project)
        except Exception as e:
            sys.exit(f"could not install skill: {e}")
        print(dest)
        print("Skill installed. Restart Claude Code to pick it up.", file=sys.stderr)
        return

    if args.list:
        try:
            list_templates(as_json=args.json)
        except Exception as e:
            sys.exit(f"could not fetch templates: {e}")
        return

    if not args.template and not args.bg:
        ap.error("a template id is required (or use --bg for a custom background)")

    # with --bg there is no template positional, so fold it back into the lines
    if args.bg:
        lines = ([args.template] if args.template else []) + args.lines
        template = "custom"
    else:
        lines = args.lines
        template = args.template

    url = build_url(template, lines, args.ext, args.bg, args.style, args.font)

    if args.print_url:
        if args.json:
            print(json.dumps({"url": url}))
        else:
            print(url)
        return

    try:
        n = download(url, args.out)
    except Exception as e:
        # a 404 almost always means a bad template id — point the user/agent at --list
        hint = None
        if getattr(e, "code", None) == 404 and not args.bg:
            hint = (f"template '{template}' not found (404). "
                    "Run `meme --list` to find the correct id.")
        if args.json:
            out = {"error": str(e), "url": url}
            if hint:
                out["hint"] = hint
            print(json.dumps(out))
            sys.exit(1)
        msg = f"download failed: {e}\nurl was: {url}"
        if hint:
            msg += f"\nhint: {hint}"
        sys.exit(msg)

    if args.json:
        print(json.dumps({"path": args.out, "bytes": n, "url": url}))
    else:
        print(args.out)                   # stdout: just the path, easy to capture
        print(f"saved {n} bytes from {url}", file=sys.stderr)


def main(argv=None):
    """Entry point. Wraps _run so the CLI never dies with a raw traceback."""
    try:
        return _run(argv)
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        sys.exit(130)
    except BrokenPipeError:
        # downstream closed the pipe (e.g. `meme --list | head`). Silence the
        # traceback Python would otherwise emit when flushing stdout at exit.
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(0)


if __name__ == "__main__":
    main()
