# Agent Instructions

This repository is the source of truth for the global (user-level) instructions given to each AI client. Nothing here is loaded automatically: a file takes effect only after its contents are pasted into the matching client.

## Layout

```
<client>/<model-slug>.md       generated instruction file, the text pasted into the client
src/<client>/<model-slug>.md   source for that file, one per client and target model
shared/<fragment-name>.md      paragraphs reused by several sources
scripts/build.py               builds the instruction files from src/ and shared/
scripts/lint.py                linter for instruction files, docs, and PR titles
.agents/skills/                skills for agents working in this repository
.claude/skills                 symlink to .agents/skills, so Claude Code loads them too
```

## Sources and Generated Files

Never edit `<client>/<model-slug>.md` by hand. Edit its source under `src/` or a fragment under `shared/`, run `python3 scripts/build.py`, and commit the sources together with the regenerated files. The linter fails when a generated file is stale or has no source.

In a source, a line holding only `{{fragment-name}}` is replaced by the contents of `shared/fragment-name.md`. Everything else is copied as written.

- **Share a paragraph only while it is identical.** Editing a fragment changes every file that includes it. To tune a paragraph for one model, replace the include line in that source with the tuned text and leave the fragment alone.
- **One paragraph per fragment.** Headings and section order belong to each source.

## Conventions

- **One directory per client.** Chat clients and coding agents are separate clients with separate directories, even from the same vendor (`claude-chat` and `claude-code`, `chatgpt` and `codex`), because their model lineups and instruction needs differ. Do not derive a coding-agent file from a chat file or the reverse.
- **One file per target model.** Name the file after the model it was tuned for, in lowercase kebab-case (`fable-5-2.md`). When a client applies one instruction field to a whole model family and its models need no separate wording, one file named after the family (`gemini-4.md`) covers them; split it once a model needs its own tuning.
- **Add, never rename, on a model upgrade.** When a client gains a new model, add a new source tuned for it and leave the existing files in place. Instructions follow the model version, so several files in one directory can be in effect at the same time, each for its own model.
- **A generated file is the pasted text, verbatim.** No front matter, titles, or notes that should not reach the model.

## Deployment

Deployment is manual: copy the whole generated file to the place its client reads global instructions from. Make changes here first and deploy afterwards, so a client never holds edits that are missing from this repository.

- `chatgpt/`: the ChatGPT custom instructions field.
- `claude-chat/`: the Claude user preferences field.
- `gemini/`: Instructions for Gemini in the Gemini app, under Personal Intelligence. Add each paragraph as its own entry; the app checks entries when saving and may refuse one.
- `codex/`: the file `~/.codex/AGENTS.md`, which Codex reads before project files for every model. Project `AGENTS.md` files come later in the prompt and override it; the combined size is capped at 32 KiB by default.
- `antigravity/`: the file `~/.gemini/GEMINI.md`, which Antigravity loads as an always-on global rule for every model in its selector. A rule file is truncated above 24,000 bytes.

## Changing Instructions

Follow the `draft-instructions` skill in `.agents/skills/` when creating or revising an instruction file, then run `python3 scripts/build.py` and `python3 scripts/lint.py` before opening or updating a pull request. Repository documents, commits, and PR titles are written in English.

Pull requests are squash-merged only, to keep the history on `main` linear. After a merge, a reused branch has diverged from `main`: merge `main` into it before adding new commits.
