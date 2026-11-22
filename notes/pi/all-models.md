# pi/all-models.md

Target: `~/.pi/agent/AGENTS.md`, the Pi coding agent's global context file. Written for the models the owner runs through Pi: DeepSeek, GLM, and MiniMax.

## Sources read (2026-11-22)

- Pi: Configuration, `docs.pi.dev/latest/configuration`, where `pi.dev/docs` redirects.
- Model sources and community reports: see `notes/opencode/all-models.md`.

## Decisions

- **One file for every model**. Status: vendor. Context files in the agent directory apply across working directories, and the configuration page describes no way to load instructions per model.
- **Same content as the OpenCode file**. Status: proposed. The rules address the models, and nothing read about Pi calls for different wording. Split the two sources when a harness-specific rule appears.
- **`AGENTS.md`, not `APPEND_SYSTEM.md`**. Status: proposed. Both would reach the model; the context file is the documented place for user instructions, and `APPEND_SYSTEM.md` files of the same name are not combined across directories.

## Deployment

- Pi also reads context files from the working directory and its parents, and combines them with the global one.
- `AGENTS.override.md` in the agent directory would replace this file.

## Open questions

- Not tested in Pi.
