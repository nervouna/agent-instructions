# pi/all-models.md

Target: `~/.pi/agent/AGENTS.md`, the Pi coding agent's global context file. Written for the models the owner runs through Pi: DeepSeek, GLM, and MiniMax.

## Sources read (2026-11-22)

- Pi: Configuration, `docs.pi.dev/latest/configuration`, where `pi.dev/docs` redirects.
- Model sources and community reports: see `notes/opencode/all-models.md`.

## Sources read (2026-11-28)

- Pi docs, `docs.pi.dev/latest/`: Codemode, Command Line ("Enable codemode"), Settings ("Terminal and display"), Terminal setup, and Choose a Model ("Use image models").
- Pi changelog, `pi.dev/changelog`: 1.0.3 ("Codemode images saved to files") and 1.0.4 ("Codemode persists images").
- Published code of `@earendil-works/pi-coding-agent` 1.7.0 and `@earendil-works/pi-ai` 1.7.0 from npm, read because the docs do not say how tool-result images are displayed: `modes/interactive/components/tool-execution.js`, `extensions/codemode/renderer.js`, `core/tools/read.js`, and `api/transform-messages.js`.

## Decisions

- **One file for every model**. Status: vendor. Context files in the agent directory apply across working directories, and the configuration page describes no way to load instructions per model.
- **Same content as the OpenCode file, except the image paragraph**. Status: proposed. The rules address the models, and nothing read about Pi calls for different wording. The image paragraph is the first harness-specific rule, so it is written in this source only, not as a shared fragment.
- **Display images inline**. Status: confirmed for the rule, proposed for the wording. 2026-11-28: the owner asked for a rule to prefer `image(block)` for showing an image inline in the terminal. Checked against the sources above:
  - `image()` is a global of codemode scripts, not a tool. Codemode is off by default and is turned on with `"defaultTools": ["+codemode"]`. Hence the `read` alternative, so the rule still works in sessions without codemode.
  - The interactive UI draws the image blocks of every tool result inline, not only codemode results (`tool-execution.js`). A `read` of an image file therefore displays it as well. Inside a script, `tools.read()` returns an image block that is shown only once passed to `image()`.
  - `image()` takes a base64 `data:` URL, an `{ image_url }` object, or an image block, in PNG, JPEG, GIF, or WebP; remote URLs are refused. It also saves each image to a temp file and names the path in the result.
  - Inline display needs a terminal with the Kitty or iTerm2 image protocol and `terminal.showImages` (default true). Otherwise the UI prints a text placeholder, and the model receives the same tool result either way, so it cannot tell. Hence "Still give the path".
  - The image also enters the model's context. A model whose `input` lacks `"image"` receives "(tool image omitted: model does not support images)" instead, so the request does not fail.
  - Codemode already tells the model to call `image(block)` when a script generates images and does not show them, so the rule matters most for images that already exist as files.
- **`AGENTS.md`, not `APPEND_SYSTEM.md`**. Status: proposed. Both would reach the model; the context file is the documented place for user instructions, and `APPEND_SYSTEM.md` files of the same name are not combined across directories.

## Deployment

- Pi also reads context files from the working directory and its parents, and combines them with the global one.
- `AGENTS.override.md` in the agent directory would replace this file.
- The `image()` part of the image paragraph applies only where codemode is turned on in `~/.pi/agent/settings.json`, a project's `.pi/settings.json`, or with `pi --tools +codemode`.

## Open questions

- Not tested in Pi.
- Whether DeepSeek, GLM, and MiniMax follow the image paragraph, or keep naming paths only.
