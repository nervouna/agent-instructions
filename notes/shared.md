# Shared fragments

Why each paragraph in `shared/` exists. Status values are explained in `AGENTS.md`.

## Communication

- **`communication-language`, `communication-punctuation`**. Status: unknown. The owner's standing language and punctuation preferences; they predate these notes.
  - 2026-11-22: the punctuation rule names the forbidden characters in backticks so the linter can exempt inline code instead of whitelisting the sentence (#3).
- **`work-report`**. Status: proposed. Coding agents only. A final report should say what changed, what was verified, and what is open, because the reader has not seen the tool calls.

## Working style

- **`decisive-conclusions`, `competent-adult`**. Status: unknown. Written for ChatGPT before these notes; reused unchanged for the Gemini app.
- **`drive-to-completion`**. Status: unknown for the original wording. Reused for all three coding agents because the owner prefers agents that finish without waiting for permission; for Claude Code it also answers the early-stopping behavior Anthropic documents for Fable 5.2.
- **`stay-in-scope`**. Status: proposed. Codex and Claude Code. Unrequested refactors make diffs harder to review.
- **`current-docs`**. Status: confirmed. 2026-11-22: the owner asked for vendor documentation to be read first-hand for every new model, and set up a cloud environment for it.

## Verification

- **`verify-before-done`, `no-weakened-checks`**. Status: proposed. Coding agents only. Both keep an absolute "never" on purpose: reporting unverified work as working, and loosening a check to get a pass, are not judgment calls.

## Git and irreversible actions

- **`commit-when-asked`, `confirm-irreversible`**. Status: proposed. Antigravity and Codex only. Conservative defaults that the owner has not confirmed. Claude Code does not include them; see `notes/claude-code/fable-5-2.md`.

## Limits and disagreement

- **`harm-exclusions`, `independent-stance`**. Status: unknown. Used by ChatGPT and Claude chat. The Gemini app refuses to store them; see `notes/gemini/gemini-4.md`.
- **`external-limits`, `disagreement`**. Status: unknown for the original wording. Used by every file. 2026-11-22: both were saved by the Gemini app without changes.
