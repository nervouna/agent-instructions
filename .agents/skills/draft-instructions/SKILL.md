---
name: draft-instructions
description: >-
  Workflow and semantic review checklist for drafting or revising model
  user-instruction files in this repository. Use whenever creating, auditing,
  or updating an instruction document for a chat or agent client.
---

# Draft Instructions

Follow this semantic checklist when creating or revising an instruction file. Formatting, file naming, spelling, and PR title rules are enforced automatically by `scripts/lint.py` and CI, so do not duplicate them in prose.

## Where to Edit

Instruction files are generated. Edit the source at `src/<client>/<model-slug>.md` or a fragment in `shared/`, never the generated `<client>/<model-slug>.md`. A fragment is included by every source that names it, so change one only when the new wording is right for all of those models; to tune a paragraph for a single model, replace its `{{fragment-name}}` line in that source with the tuned text.

## Researching a Model

Read the vendor's own pages first-hand; search summaries and third-party posts are leads, not sources. The `agent-instructions` cloud environment allows the documentation hosts of Google, OpenAI, and Anthropic, and plain `curl` reaches them. If a documentation URL redirects to a host that is not allowed yet, propose adding that host to the environment instead of falling back to secondary coverage. In the pull request, state which claims come from the vendor's text for the target model, which are carried over from an earlier generation, and which pages could not be read.

## Semantic Checklist

1. **Check Version-Specific Guidance First**: Search the vendor's current prompting guide and model spec for the exact target model version before writing. Identify its native defaults so rules do not over-correct them (for example, adding generic brevity commands to an already terse model clips substantive reasoning, while models that pause to ask permission need explicit authority to make reasonable, reversible assumptions). Exclude API-only mechanics such as prompt caching or history-prefix rules when writing for chat clients.
2. **Align Rather Than Override**: Avoid adversarial override phrasing (such as claiming there is only one criterion) or asking the model to blame external rules when hitting built-in boundaries; inside user-preference blocks, those patterns trigger anti-jailbreak defensiveness or conflict with character training. Anchor autonomy in concrete third-party harm, adult self-responsibility, and assuming legitimate intent on dual-use prompts, and ask the model to name hard tool or system constraints plainly without moralizing. Some clients enforce this at save time: the Gemini app refuses to store an instruction entry that redefines what counts as harm or tells the model to set aside a company's or platform's position, and shows its policy guidelines instead.
3. **Close Hydraulic Loopholes**: Audit how prohibitions and exceptions interact. When upfront disclaimers are banned, RLHF caution will leak through any permissive clause elsewhere (such as allowing an opening personal opinion). Require full task execution first; allow at most one final sentence only for substantive flaws or genuine disagreement, never boilerplate caveats.
4. **Scope Language and Register**: Maintain a single consistent voice throughout (second-person imperative). Explicitly scope language-specific punctuation and style rules to their target language so Chinese dialogue conventions do not bleed into English code or repository documents.

## Record the Reason

Update the file's notes under `notes/` in the same change: what you observed or read, the date and source, any text the client refused, and a status for each decision as defined in `AGENTS.md`. Record the reasons for shared fragments in `notes/shared.md`. A rule without a recorded reason cannot be pruned safely when the model changes.

## Verification

Run `python3 scripts/build.py` to regenerate the instruction files, then `python3 scripts/lint.py`, and resolve any reported errors before opening or updating a pull request.
