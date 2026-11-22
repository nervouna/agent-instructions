# opencode/all-models.md

Target: `~/.config/opencode/AGENTS.md`, the OpenCode global instruction file. Written for the models the owner runs through OpenCode: DeepSeek, GLM, and MiniMax.

## Sources read (2026-11-22)

First-hand:

- OpenCode: Instructions, Agents, and Config under `opencode.ai/docs/`.
- DeepSeek: "Your First API Call" and "Integrate with OpenCode", `api-docs.deepseek.com`.
- Z.ai: GLM-5.3, "Best Practice" for coding agents, and the documentation index, `docs.z.ai`.
- MiniMax: Models, "Model Invocation", and "Tool Use & Interleaved Thinking", `platform.minimax.io`.

Second-hand, from search summaries of GitHub issues, blog posts, and preprints. `github.com` is not on the environment's allowlist, so the issues themselves were not read.

## Decisions

- **One file for every model**. Status: vendor. The global file applies to all models. The only per-model mechanism is a custom agent, and an agent's body replaces the provider's base system prompt, which is too heavy for personal preferences.
- **Named `all-models`**. Status: confirmed. The owner accepted one file per harness, since the slot is shared by models from several vendors and no vendor documents behavior that would justify separate wording.
- **Shorter than the Codex file**. Status: proposed. Community reports say these models often skip or disregard instruction files, so the file keeps the rules that matter most. Left out: `current-docs`, `checks-over-prose`, and `external-limits`.
- **`act-then-stop`**. Status: proposed. Answers the two behaviors reported most often: announcing an action and ending the turn without doing it, and continuing to call tools after the task is finished.
- **Git and confirmation rules kept**. Status: proposed. See Open questions.

## Models

Vendor material describes API mechanics only: none of the three publishes guidance on default behavior that could shape a rule file. The owner asked for community reports to be weighed alongside vendor claims, which he expects to overstate capability.

- **DeepSeek**. Current models: `deepseek-flash`, served by DeepSeek-V4.1-Flash-1017, and `deepseek-v4-pro`.
  - Reported: tool-call loops after the task is done, turns that end after "Let me look into this" with no tool call, unstable parallel tool calls, and repeated violation of agent and global rules in OpenCode.
- **GLM**. Current models: GLM-5.3 and GLM-5.3-Flash. Reasoning is always on, and the default effort is `max`.
  - Reported: mostly routing and hosting failures, such as errors on the Anthropic-compatible route and endless reasoning on third-party hosting. One account of the model quitting right after reading the specification. High cost at the default effort.
- **MiniMax**. Current models: MiniMax-M3.1-Flash and MiniMax-M3. Thinking cannot be turned off.
  - Reported: turns that stop abruptly or finish with no output, and instruction files being skipped or disregarded in most sessions.
- **Independent benchmark**. One third-party coding test scored DeepSeek V4.1 Flash 73.2%, MiniMax M3.1 Flash 66.7%, and GLM 5.3 66.2%, with GLM ranking higher over a 20-turn session. No rigorous independent study of long-horizon reliability was found, and no reports of faked implementations or deleted tests.

## Limits of rule text

- Silent stops and endless reasoning were mostly traced to the harness or API layer, such as reasoning content not being kept between tool calls. Rules cannot fix those.
- OpenCode's maintainers answer reports of ignored rules by pointing to its permissions system.

## Deployment

- Without `~/.config/opencode/AGENTS.md`, OpenCode reads `~/.claude/CLAUDE.md`, so the Claude Code file would otherwise reach these models.
- OpenCode combines global and project files and does not resolve conflicts between them.

## Open questions

- Whether to keep commit and confirmation limits in an OpenCode permissions configuration instead of prose. The owner has not decided.
- Not tested in OpenCode.
