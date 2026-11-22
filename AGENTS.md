# Agent Instructions

This repository is the source of truth for the global (user-level) instructions given to each AI client. Nothing here is loaded automatically: a file takes effect only after its contents are pasted into the matching client.

## Layout

```
<client>/<model-slug>.md   one instruction file per client and target model
.agents/skills/            skills for agents working in this repository
.claude/skills             symlink to .agents/skills, so Claude Code loads them too
scripts/lint.py            linter for instruction files, docs, and PR titles
```

## Conventions

- **One directory per client.** Chat clients and coding agents are separate clients with separate directories, even from the same vendor (`claude-chat` and `claude-code`, `chatgpt` and `codex`), because their model lineups and instruction needs differ. Do not derive a coding-agent file from a chat file or the reverse.
- **One file per target model.** Name the file after the model it was tuned for, in lowercase kebab-case (`fable-5-2.md`).
- **Add, never rename, on a model upgrade.** When a client gains a new model, add a new file tuned for it and leave the existing files in place. Instructions follow the model version, so several files in one directory can be in effect at the same time, each for its own model.
- **File content is the pasted text, verbatim.** No front matter, titles, or notes that should not reach the model.

## Deployment

Deployment is manual: copy the whole file into the client's global custom-instruction field. Make changes here first and paste them into the client afterwards, so the text in the client never contains edits that are missing from this repository.

## Changing Instructions

Follow the `draft-instructions` skill in `.agents/skills/` when creating or revising an instruction file, and run `python3 scripts/lint.py` before opening or updating a pull request. Repository documents, commits, and PR titles are written in English.
