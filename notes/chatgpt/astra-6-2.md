# chatgpt/astra-6-2.md

Target: ChatGPT custom instructions, tuned for GPT-6.2 Astra.

This file predates these notes, so the observations behind its rules were not recorded. Fill in a rule's reason the next time it is touched.

## Sources read (2026-11-22)

- OpenAI Model Spec, version 2026-10-29, `model-spec.openai.com/2026-10-29.html`. It is the latest version: `model-spec.openai.com/` redirects to it and it is the newest changelog entry. Every version page carries a hidden "A newer version of the Model Spec is available" banner in its HTML, so a text dump of the page shows the banner even on the latest version.
- OpenAI Model Spec, version 2026-08-18, `model-spec.openai.com/2026-08-18.html`, for comparison.
- Model Spec changelog, `github.com/openai/model_spec/blob/main/CHANGELOG.md`.
- "An updated Model Spec for more capable and beneficial AI", `openai.com/index/updated-model-spec`, published 2026-10-29.

- "Customizing your ChatGPT personality", `help.openai.com/en/articles/11899719`.
- "ChatGPT custom instructions", `help.openai.com/en/articles/8096356`.

Not read: the release notes linked from the changelog, and whether GPT-6.2 Astra was trained against the 2026-10-29 or an earlier version. The Spec says only "Our production models do not yet fully reflect the Model Spec".

## What the Model Spec says

No rule in the source was changed because of these findings. They explain how much weight a custom instruction can carry and which rules need blunt wording.

- **Authority levels decide what an instruction can change.** The Spec ranks its own sections as Root, System, Developer, User, or Guideline. Guideline defaults "can also be overridden implicitly when the context clearly calls for it". User-level defaults yield "only by explicit instructions at the user level or higher". Developer-level defaults can be changed by developers and not by users. The Spec does not say which level ChatGPT custom instructions arrive at.
- **Tone is a Guideline.** "Match the situation and audience" sets the default voice: "it should sound like a colleague rather than a close personal friend". Follow-up questions ("asking the user if their problem was solved, or if they'd like for GPT to provide more detail on something") are "encouraged by default if and only if GPT is in an interactive setting", also a Guideline, and most compliant examples in the Spec end with one. This is the behavior the "never append unsolicited follow-up menus" rule pushes against, and a Guideline is the easiest level to override.
- **Honesty, objectivity, and sycophancy are User level.** "Do not lie", "Don't be sycophantic", and "Assume an objective point of view" stay in force unless overridden explicitly. The Overview gives the reason: if the model treated them "as implicitly negotiable based on what it inferred the user wanted to hear, it could mislead the user". On moral questions the default is to present context "without taking a stance", so the decisive-conclusions and independent-stance paragraphs need to stay explicit to have any effect.
- **The regulated-advice disclaimer is Developer level.** "Provide information without giving regulated advice" says "A concise disclaimer should also be included" on legal, medical, and financial topics. By the Spec's own ranking a user cannot turn this off, so the "no domain caveats" sentence in "Do and Stop" asks for something the Spec places above user authority.
- **Personality was removed from the Spec on 2026-10-29.** The 2026-08-18 version had sections titled "Love humanity", "Be warm", "Be curious", "Be interesting and interested", "Be rationally optimistic", "Have conversational sense", "Be clear and direct", "Avoid being condescending or patronizing", and "Don't make unprompted personal comments". The 2026-10-29 version drops them; the changelog entry reads "Removes most detailed style guidance". What remains of style is "Match the situation and audience" and "Be creative". The Overview now says the Spec "intentionally leaves many details of style, personality, and interaction unspecified. User preferences help fill those gaps".
- **OpenAI's stated reason.** From the blog post: "Style should adapt to what people prefer", which it spells out as "in aggregate, within languages and cultures, and for each person", with "user feedback and context providing evidence about those preferences. The Spec retains stronger defaults, such as approaching questions objectively." The post does not say what counts as user feedback or whether the removed traits remain in trained models.
- **The subject was renamed.** The 2026-10-29 version says "GPT" where earlier versions said "the assistant"; the blog post attributes this to "the increasing breadth of our models' use cases and deployment settings".

## Decisions

- **"Role" section: everyday life, a warm friend who knows him**. Status: confirmed for the topic split, proposed for the wording. 2026-11-22: the owner asked for the three chat files to stop converging on one personality and to give each model its own topics, following a recommendation made in the session that read the vendors' behavior documents. ChatGPT gets everyday life because the Model Spec now leaves personality to the user, its memory makes answers about his own life specific, and the traits removed from the Spec on 2026-10-29 (warm, curious, rationally optimistic) describe this role.
  - "Stay honest while being warm" is there because asking for warmth pulls toward flattery; the Spec's own wording is "a firm sounding board" and not "a sponge that doles out praise".
  - "Finish with the concrete step he can take today" names an action of his, so it does not reopen the follow-up offers the Communication section bans.
  - The decisive-conclusions paragraph stays: the topic split changes warmth and focus, and the owner still wants a clear conclusion from every model.

- **"Directness and Initiative" section**. Status: unknown. Present here and absent from the Claude chat file; the reason for the difference was not recorded.
- **Domain caveats named explicitly** (legal, medical, financial, "for authorized testing only"). Status: unknown. Inline in this source; the Claude chat file says "unsolicited safety reminders" instead.
- **"Never pivot to an unrequested high-level overview"**. Status: unknown. Inline in this source only.
- **"Cut throat-clearing and filler"**. Status: unknown. Not carried to the Gemini file; see `notes/gemini/gemini-4.md`.

## Open questions

- Whether the "no domain caveats" sentence works in practice, given that the Model Spec ranks the regulated-advice disclaimer at Developer level. Not tested in the client.
- How the "Role" section changes answers in practice. 2026-11-22: the owner saved the file in the client. Its effect has not been observed.
- Health, legal, and financial questions are everyday-life topics, and they are where the Developer-level disclaimer applies.

## Deployment

- Length: 3,911 characters. The help page says "Free and Go users can save up to 1,500 characters in custom instructions. Plus, Pro, Enterprise, Business, and Education users can save up to 5,000 characters." The file fits only on a paid plan. 2026-11-22: the owner saved it in one piece.
- "Base style and tone" under Personalization selects a preset personality that "works alongside any saved memories or custom instructions". Status: proposed. "Friendly" matches the role; the help page describes it as "Warm and chatty" and best for "Decision support, personal reflection, and planning". The owner's current setting is not recorded.
