# antigravity/gemini-4.md

Target: `~/.gemini/GEMINI.md`, the Antigravity global rule file, for the Gemini 4 family.

## Sources read (2026-11-22)

- Rules, Customization discovery, and Models under `antigravity.google/docs/`.

## Decisions

- **One file for the whole family**. Status: vendor. A global rule file is always active and applies to every model in the selector, including the Claude models and the Orchestrator pairing. Gemini 4 Neon is the default model.
- **Written for a coding agent, not derived from a chat file**. Status: confirmed. Repository convention.
- **"A repository's own instructions take precedence"**. Status: proposed. Antigravity combines global and workspace rules cumulatively, so the file states the priority itself.
- **"Read the relevant code before changing it, and match the conventions already there"**. Status: proposed. 2026-11-22: "comment density" was removed from its list of conventions when the no-comments rule was added. Kept here and dropped from the Codex and Claude Code files, whose vendors say to leave routine decisions to the agent.
- **Verification and git rules**. Status: proposed. See `notes/shared.md`.

## Limits

- A rule file is truncated above 24,000 bytes, and all global and always-on rules share a 20,000-token budget.

## Open questions

- No vendor guidance on how Gemini 4 behaves as a coding agent was found, so no rule corrects a specific model habit.
- Not tested in Antigravity.
