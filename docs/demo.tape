# VHS tape for the README demo. Render with: vhs docs/demo.tape
Output docs/demo.gif

Set Shell bash
Set FontSize 22
Set Width 1180
Set Height 640
Set Padding 24
Set Theme "Catppuccin Mocha"

# Hidden setup: put `meme` on PATH, set a clean prompt, clear the screen.
Hide
Type "export PATH=$HOME/.local/bin:$PATH; export PS1='$ '; clear"
Enter
Show

Sleep 800ms
Type "# your coding agent, the moment CI goes red:"
Enter
Sleep 1s
Type `meme -t fine "prod is down" "this is fine" --print-url`
Enter
Sleep 2500ms

Type "# paste that URL into a PR or Slack -- it renders inline, no image hosting"
Enter
Sleep 1800ms

Type `meme -t drake "manual deploys" "ci/cd" --print-url`
Enter
Sleep 2500ms

Type "# zero deps, free API, and a bundled Claude Code skill so agents just drive it"
Enter
Sleep 2500ms
