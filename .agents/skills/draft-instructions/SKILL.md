---
name: draft-instructions
description: >-
  Workflow and semantic review checklist for drafting or revising model
  user-instruction files in this repository. Use whenever creating, auditing,
  or updating an instruction document for a chat or agent client.
---

# Draft Instructions

Follow this semantic checklist when creating or revising an instruction file. Formatting, file naming, spelling, and PR title rules are enforced automatically by `scripts/lint.py` and CI, so do not duplicate them in prose.

## Semantic Checklist

1. **Check Version-Specific Guidance First**: Search the vendor's current prompting guide and model spec for the exact target model version before writing. Identify its native defaults so rules do not over-correct them (for example, adding generic brevity commands to an already terse model clips substantive reasoning, while models that pause to ask permission need explicit authority to make reasonable, reversible assumptions). Exclude API-only mechanics such as prompt caching or history-prefix rules when writing for chat clients.
2. **Align Rather Than Override**: Avoid adversarial override phrasing (such as claiming there is only one criterion) or asking the model to blame external rules when hitting built-in boundaries; inside user-preference blocks, those patterns trigger anti-jailbreak defensiveness or conflict with character training. Anchor autonomy in concrete third-party harm, adult self-responsibility, and assuming legitimate intent on dual-use prompts, and ask the model to name hard tool or system constraints plainly without moralizing.
3. **Close Hydraulic Loopholes**: Audit how prohibitions and exceptions interact. When upfront disclaimers are banned, RLHF caution will leak through any permissive clause elsewhere (such as allowing an opening personal opinion). Require full task execution first; allow at most one final sentence only for substantive flaws or genuine disagreement, never boilerplate caveats.
4. **Scope Language and Register**: Maintain a single consistent voice throughout (second-person imperative). Explicitly scope language-specific punctuation and style rules to their target language so Chinese dialogue conventions do not bleed into English code or repository documents.

## Verification

Run `python3 scripts/lint.py` locally and resolve any reported errors before opening or updating a pull request.
