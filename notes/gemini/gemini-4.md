# gemini/gemini-4.md

Target: Instructions for Gemini in the Gemini app, for Gemini 4 Argon, Carbon, Hydrogen, and Neon.

## Sources read (2026-11-22)

- Gemini API prompt design strategies, `ai.google.dev/gemini-api/docs/prompting-strategies` (redirects to `aistudio.google.com`).
- Get started with Gemini 4 and the Argon, Carbon, and Hydrogen developer guides, `docs.cloud.google.com`.
- What's new in Gemini 4 Carbon, Neon, and Hydrogen, `ai.google.dev`.
- "Manage what Gemini remembers about you and customize responses", `support.google.com/gemini/answer/16598625`.
- "Policy guidelines for the Gemini app", `gemini.google/policy-guidelines/`.
- "Our approach to the Gemini app", `gemini.google/our-approach/`, published 2024-07-25.

Not read: the Gemini 4 Carbon developer guide under `aistudio.google.com/learn/`, a script-rendered page that needs hosts outside the environment's allowlist.

## What Google publishes about Gemini's behavior

No rule in the source was changed because of these findings. Google has no counterpart to the OpenAI Model Spec or Claude's Constitution; see `notes/chatgpt/astra-6-2.md` and `notes/claude-chat/fable-5-2.md` for those.

- **Two short pages, both about the Gemini app only.** Neither has a version history, authority levels, or a statement about the API or coding products. A search on 2026-11-22 found no newer document; the Axios report on Gemini's "behavior code" describes these same pages as first shared in 2024.
- **The policy guidelines are a list of outputs to avoid.** The stated goal is "to be maximally helpful to users, while avoiding outputs that could cause real-world harm or offense". The categories are child safety, dangerous activities, violence and gore, harmful factual inaccuracies, harassment, and sexually explicit material. This is the page the app showed when it refused to save the "Do and Stop" section.
- **Gemini is positioned as a tool without views of its own.** "As a steerable tool, Gemini is designed to follow your instructions and customizations to the best of its ability, within certain specific limits. It should do so without conveying a particular opinion or set of beliefs unless you tell it to." Also: "Gemini is what you make it." Asked for an opinion, "it should respond with a range of views". The decisive-conclusions and independent-stance paragraphs push against this default.
- **Personality gets one sentence.** "Gemini should be genuine, curious, warm, and vibrant. Not just useful, but fun." Nothing says how this is trained or how it varies by model.
- **Follow-up questions are intended.** "Gemini may also ask a follow up question to show curiosity and make sure the answer satisfied your needs." This is the habit the "no closing offers" rule targets.
- **Google states the aim of refusing less.** "Over time our goal is to reduce instances where Gemini does not respond to your prompt". The page dates from 2024 and may not describe Gemini 4.

## Decisions

- **"Role" section: the outside world, a well-informed guide**. Status: confirmed for the topic split, proposed for the wording. 2026-11-22: the owner asked for the three chat files to stop converging on one personality and to give each model its own topics, following a recommendation made in the session that read the vendors' behavior documents. Gemini gets news, internet culture, products, travel, and entertainment because those answers depend on recent information and the app is built on Google Search.
  - The tone words follow Google's own sentence: "Gemini should be genuine, curious, warm, and vibrant. Not just useful, but fun."
  - The source and freshness rules ask for evidence standards, which fit the app's positioning as a tool, where a strong personality would not.
  - "Explain crude or offensive material as plainly as anything else" is there because the policy guidelines list "offense" beside harm, and internet culture is full of such material. It was expected to be the sentence most likely to be refused at save time; the app accepted it.
  - The owner first suggested internet culture alone; the range was widened to recent information in general, and the playful side of internet culture was left out because of the same policy page.

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

- How the "Role" paragraphs change answers in practice. 2026-11-22: the owner saved them and the app refused none. Their effect has not been observed.
- Whether answers become too long without a brevity instruction.
- Whether Argon is still offered in the app's model picker; secondary sources disagree.
