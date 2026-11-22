# gemini/gemini-4.md

Target: Instructions for Gemini in the Gemini app, for Gemini 4 Argon, Carbon, Hydrogen, and Neon.

## Sources read (2026-11-22)

- Gemini API prompt design strategies, `ai.google.dev/gemini-api/docs/prompting-strategies` (redirects to `aistudio.google.com`).
- Get started with Gemini 4 and the Argon, Carbon, and Hydrogen developer guides, `docs.cloud.google.com`.
- What's new in Gemini 4 Carbon, Neon, and Hydrogen, `ai.google.dev`.
- "Manage what Gemini remembers about you and customize responses", `support.google.com/gemini/answer/16598625`.

Not read: the Gemini 4 Carbon developer guide under `aistudio.google.com/learn/`, a script-rendered page that needs hosts outside the environment's allowlist.

## Decisions

- **One file for the whole family**. Status: vendor. The app applies instructions "to every chat" with no per-model field, and the Gemini 4 pages give no behavioral difference between the four models that matters for chat instructions.
- **Starts from the ChatGPT file**. Status: confirmed. The owner chose it as the starting point.
- **No brevity instruction; asks for full reasoning instead**. Status: carried. The prompting guide says of Gemini 3: "By default, Gemini 3 models provide direct and efficient answers. If you need a more conversational or detailed response, you must explicitly request it." The guide has no Gemini 4 section, so this is unverified for Gemini 4.
- **"Open with the answer itself", no closing offers, headings only for structured content**. Status: proposed. The owner's style preferences from the ChatGPT file, reworded without ChatGPT-specific phrasing.
- **"Do and Stop" rewritten**. Status: confirmed. The app refused to save the section carried over from the ChatGPT file and showed its policy guidelines. The seven paragraphs now in the file were each saved successfully as separate entries.

## Rejected by the client

The Gemini app refused to save these, each as its own entry or section:

- The ChatGPT "Do and Stop" section as a whole: "stop only for concrete harm", the list of things that do not count as harm, and the paragraph about not adopting the positions of companies or authorities.
- "Treat discomfort, controversy, and unpopularity as reasons for care in wording, never as reasons to withhold an answer. Decisions whose consequences fall on him alone are his to make." Which of the two sentences triggered the refusal was not isolated. Both ideas were accepted in the reworded form now in the file.

## Deployment

- Add each paragraph as its own entry. Google's examples are one-line entries, and no length limit is documented.
- Entries last at most 18 months and then need to be added again.

## Open questions

- Whether answers become too long without a brevity instruction.
- Whether Argon is still offered in the app's model picker; secondary sources disagree.
