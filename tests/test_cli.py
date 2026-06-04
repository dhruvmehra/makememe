"""Offline tests for meme's URL building / escaping and crash-safety.

Run with:  python -m unittest discover -s tests
No network access required (network paths are covered by --print-url style asserts).
"""

import io
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout

from memecli import cli


class TestEscape(unittest.TestCase):
    def test_empty_is_underscore(self):
        self.assertEqual(cli.escape(""), "_")

    def test_space(self):
        self.assertEqual(cli.escape("a b"), "a_b")

    def test_literal_underscore_and_dash(self):
        self.assertEqual(cli.escape("a_b"), "a__b")
        self.assertEqual(cli.escape("a-b"), "a--b")

    def test_special_tokens(self):
        self.assertEqual(cli.escape("really?"), "really~q")
        self.assertEqual(cli.escape("a/b"), "a~sb")
        self.assertEqual(cli.escape('say "hi"'), "say_''hi''")

    def test_percent_and_hash_are_encoded_not_dropped(self):
        # the bare-% problem: must be percent-encoded, never left raw
        self.assertEqual(cli.escape("50%"), "50%25")
        self.assertIn("%23", cli.escape("#tag"))

    def test_unicode_roundtrips_to_ascii_url(self):
        out = cli.escape("café 🚀")
        self.assertTrue(out.isascii(), "URL segment must be ascii-safe")

    def test_no_input_ever_raises(self):
        for s in ["", " ", "\n", "\t", "\x07", "%%%", "----", "____",
                  "a" * 10000, "🚀" * 100, "?/\"\\#&=+"]:
            cli.escape(s)  # should not raise


class TestBuildUrl(unittest.TestCase):
    def test_basic(self):
        u = cli.build_url("drake", ["a b", "c"])
        self.assertEqual(u, "https://api.memegen.link/images/drake/a_b/c.png")

    def test_no_lines_gives_single_underscore(self):
        u = cli.build_url("drake", [])
        self.assertTrue(u.endswith("/drake/_.png"))

    def test_custom_background(self):
        u = cli.build_url("x", ["t"], bg="https://e.com/p.png")
        self.assertIn("/images/custom/", u)
        self.assertIn("background=https%3A%2F%2Fe.com%2Fp.png", u)

    def test_ext_and_style_and_font(self):
        u = cli.build_url("drake", ["a"], ext="jpg", style="s", font="impact")
        self.assertIn(".jpg?", u)
        self.assertIn("style=s", u)
        self.assertIn("font=impact", u)


class TestCrashSafety(unittest.TestCase):
    """The CLI must exit cleanly, never propagate a raw exception."""

    def _exit_code(self, argv):
        try:
            cli.main(argv)
            return 0
        except SystemExit as e:
            return e.code if isinstance(e.code, int) else 1

    def test_missing_template_is_clean_exit(self):
        with redirect_stderr(io.StringIO()):
            self.assertEqual(self._exit_code([]), 2)

    def test_print_url_no_network(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli.main(["drake", "a", "b", "--print-url"])
        self.assertIn("api.memegen.link/images/drake/a/b.png", buf.getvalue())

    def test_keyboard_interrupt_becomes_130(self):
        orig = cli.download
        cli.download = lambda *a, **k: (_ for _ in ()).throw(KeyboardInterrupt())
        try:
            with redirect_stderr(io.StringIO()):
                self.assertEqual(self._exit_code(["drake", "a", "b"]), 130)
        finally:
            cli.download = orig

    def test_download_failure_is_clean_exit_in_json(self):
        orig = cli.download
        cli.download = lambda *a, **k: (_ for _ in ()).throw(OSError("boom"))
        try:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(self._exit_code(["drake", "a", "--json"]), 1)
        finally:
            cli.download = orig


class TestNewCommands(unittest.TestCase):
    def test_version_flag_prints_and_exits(self):
        buf = io.StringIO()
        with self.assertRaises(SystemExit) as ctx, redirect_stdout(buf):
            cli.main(["--version"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertIn("meme", buf.getvalue())

    def test_install_skill_writes_file(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            old = os.environ.get("HOME")
            os.environ["HOME"] = d
            try:
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    cli.main(["--install-skill"])
                dest = os.path.join(d, ".claude", "skills", "meme", "SKILL.md")
                self.assertTrue(os.path.exists(dest))
                self.assertIn("name: meme", open(dest).read())
            finally:
                if old is not None:
                    os.environ["HOME"] = old


if __name__ == "__main__":
    unittest.main()
