# codex/gpt-6-2.md

Target: `~/.codex/AGENTS.md`, the Codex global instruction file, for the GPT-6.2 family.

## Sources read (2026-11-22)

- "Custom instructions with AGENTS.md", "Models", and "Prompting GPT-6.2 in Codex" on `learn.chatgpt.com`, where `developers.openai.com/codex` redirects.

## Decisions

- **One file for the whole family**. Status: vendor. The global file is read for every model, and the prompting guide says its techniques "apply across the GPT-6.2 model family, including GPT-6.2 Astra and GPT-6.2 Sol".
- **Leaner than the Antigravity file**. Status: vendor. The guide says: "Use `AGENTS.md` for project requirements and conventions that Codex can't infer from the code, tests, or docs. ... Leave routine decisions about how to do the work to Codex."
  - Dropped "repository instructions take precedence": Codex already places project files after the global file so that they override it.
  - Dropped "read the code first and match its conventions": a routine decision.
- **"Stop the background jobs you started and remove the temporary files you created"**. Status: vendor. Taken from the same guide's advice for the personal `~/.codex/AGENTS.md`.
- **No brevity instruction**. Status: vendor. The guide says GPT-6.2 writing "gets to the point sooner".
- **Verification and git rules**. Status: proposed. See `notes/shared.md`.

## Limits

- The combined size of global and project files stops at `project_doc_max_bytes`, 32 KiB by default.

## Open questions

- Not tested in Codex.
