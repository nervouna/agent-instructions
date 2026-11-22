# claude-code/fable-5-2.md

Target: `~/.claude/CLAUDE.md`, the Claude Code user instruction file, tuned for Claude Fable 5.2.

## Sources read (2026-11-22)

- "How Claude remembers your project", `code.claude.com/docs/en/memory`.
- "Prompting Claude Fable 5.2", `platform.claude.com`.

## Decisions

- **Named for one model**. Status: vendor. The tuning rests on a guide specific to Fable 5.2. The file itself loads whichever model is selected.
- **No "commit or push only when asked" and no confirmation list**. Status: vendor. Claude Code already applies both, and the guide's "Keep caution from piling up" section says accumulated cautions make the model ask for approval it does not need.
- **Routine steps listed as needing no approval**. Status: proposed. The guide says: "Name the steps that need no approval." The list itself is the author's and has not been confirmed by the owner.
- **"Ask before" instead of "never" for destructive actions**. Status: vendor. The guide says the model "treats an instruction that contains 'never' as absolute" and recommends "ask for approval before" where the model should keep judgment.
- **No ownership statement**. Status: vendor. The guide says to leave it out where the user owns the code and wants it changed as little as possible.
- **No length or sentence limits on writing**. Status: vendor. The guide says style rules are followed closely and hard limits can make prose choppy.

## Deployment

- 2026-11-22: cloud sessions were found to receive the account's chat preferences and the repository's own files, but not the user-level `~/.claude/CLAUDE.md`, which stays on the owner's machine. Source: "Cloud environments", `code.claude.com/docs/en/cloud-environments`.
- 2026-11-22: the owner made this repository public so a setup script can fetch the file anonymously from `raw.githubusercontent.com`. The script was added to the `agent-instructions` cloud environment. Its commands were run in a live session and wrote the file; a fresh container has not been observed yet.
- Each cloud environment needs the script separately.

## Limits

- Target under 200 lines per CLAUDE.md file; longer files reduce adherence.

## Open questions

- Not tested in a local Claude Code session.
