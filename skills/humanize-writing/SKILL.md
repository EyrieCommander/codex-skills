---
name: humanize-writing
description: Rewrite or review prose to remove formulaic LLM tells while preserving meaning, factual claims, citations, privacy boundaries, and the user's intended voice. Use when the user asks to humanize, de-AI, de-slop, make text sound more natural, make prose less generic, match a voice sample, polish public copy, or audit writing for AI-ish patterns. Do not use for deception, citation laundering, factual invention, or bypassing academic, legal, employment, or platform rules.
---

# Humanize Writing

Use this skill to make prose sound more natural, specific, and voiceful without changing what is true.

## Rules

- Preserve meaning, facts, citations, numbers, names, dates, quotes, and scope.
- Do not invent sources, examples, anecdotes, credentials, studies, quotes, or personal experience.
- Do not launder uncertainty into confidence. Keep caveats when they matter.
- Do not remove legally, ethically, or professionally required disclosures.
- Do not help with deception, plagiarism, impersonation, school misconduct, fake reviews, fake testimonials, fake authorship, or AI-detector bypass as the goal.
- Keep private, connector-derived, manuscript, Gmail, Drive, or work-sensitive material inside the owning workspace unless the user explicitly asks otherwise.

## Default Output

Return the rewritten text only unless the user asks for an audit, explanation, alternatives, or tracked changes.

If the user asks for an audit, provide:

1. The main AI-ish tells you found.
2. The rewritten text.
3. Any facts, claims, or citations that need source checking.

If the text is public-facing, high-stakes, quote-heavy, citation-heavy, or especially generic, read `references/ai-writing-tells.md` before rewriting.

If the user provides a voice sample or asks to match a person, brand, publication, or house style, read `references/voice-calibration.md` before rewriting.

## Workflow

1. Identify the purpose, audience, and target voice.
2. Preserve all factual content and source boundaries.
3. Cut generic setup, throat-clearing, recap, and empty signposting.
4. Replace abstract claims with concrete phrasing already supported by the text.
5. Vary rhythm naturally. Use short sentences when the thought is simple.
6. Prefer direct verbs and ordinary nouns over inflated language.
7. Restore a real point of view where appropriate, without forcing jokes or quirks.
8. Read the result aloud mentally and remove anything that sounds like a brochure, LinkedIn post, policy memo, or tutorial intro unless that is the requested voice.
9. Do a final integrity pass: confirm no new facts appeared.

## Common Patterns To Fix

- Signposting: "Let's dive in", "Here's what you need to know", "In conclusion".
- Inflated significance: "pivotal", "transformative", "underscores", "testament".
- Promotional texture: "seamless", "vibrant", "robust", "cutting-edge".
- Vague authority: "experts say", "industry observers", "studies show" without a source.
- Fake balance: "not just X, but Y", "from A to B", tidy rule-of-three lists.
- Excessive hedging: "it could potentially be argued".
- Present-participle padding: sentence tails beginning with "highlighting", "showcasing", "reflecting", "ensuring".
- Perfectly even paragraph rhythm.
- Headers followed by a sentence that merely restates the header.

## Voice Matching

If the user provides a voice sample, preserve its usable traits:

- sentence length and rhythm;
- paragraph openings;
- level of formality;
- punctuation habits;
- tolerance for bluntness, humor, uncertainty, and first person;
- preferred vocabulary.

Do not parody the sample. Match posture and rhythm more than surface tics. If the text will be public or sensitive, keep it cleaner than the sample when needed.

## Refusal And Redirection

If the user wants detector evasion, plagiarism, fake authorship, fabricated experience, or deception, do not provide a bypass. Offer an honest alternative: revise for clarity, cite sources, disclose assistance where required, or turn the text into a legitimate draft in the user's own voice.
