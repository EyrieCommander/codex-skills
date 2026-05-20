# AI Writing Tells

Use this reference when the input is long, public-facing, especially generic, or when the user asks for an audit. The pattern list is adapted from the MIT-licensed `blader/humanizer` skill, which itself points to Wikipedia's "Signs of AI writing" cleanup guidance.

## Fast Audit Checklist

- Does the text announce what it is about to do instead of doing it?
- Does it inflate ordinary facts into historical significance?
- Does it rely on vague authorities instead of named evidence?
- Does it use polished abstractions where concrete nouns would work?
- Does every paragraph have the same shape and emotional temperature?
- Did the rewrite accidentally add facts, citations, or examples?

## Pattern Categories

### Empty Openings And Closings

Watch for "Great question", "Let's dive in", "Here's what you need to know", "In conclusion", "The future looks bright", and "Let me know if you want me to expand".

Fix by starting with the actual claim, scene, instruction, or answer.

### Significance Inflation

Watch for "pivotal", "crucial", "testament", "underscores", "highlights", "marks a shift", "broader landscape", "lasting impact", and "sets the stage".

Fix by saying what happened and why it matters in concrete terms. If it does not matter, cut the claim.

### Promotional Texture

Watch for "vibrant", "rich", "seamless", "robust", "cutting-edge", "groundbreaking", "must-visit", "stunning", "nestled", and "showcase".

Fix by replacing marketing adjectives with observable details.

### Vague Attribution And Fake Evidence

Watch for "experts say", "industry observers", "studies show", "many argue", "critics note", and unsourced media-name stacking.

Fix by naming the source, qualifying the claim, or deleting the attribution.

### Present-Participle Padding

Watch for sentence tails beginning with "highlighting", "showcasing", "reflecting", "underscoring", "ensuring", "contributing to", or "fostering".

Fix by splitting the real point into a separate sentence or cutting the padding.

### Fake Balance And Tidy Contrast

Watch for "not just X, but Y", "from A to B", "whether X or Y", and overly neat two-sided framing.

Fix by choosing the real contrast, or by admitting that the issue is messier than the formula suggests.

### Rule Of Three And Synonym Stacking

Watch for strings like "innovate, collaborate, and transform" or "a catalyst, a partner, and a foundation".

Fix by keeping the one word that actually means something.

### Abstract Nouns And Faux Depth

Watch for "interplay", "landscape", "tapestry", "ecosystem", "journey", "alignment", "impact", "innovation", and "transformation" when they are not doing technical work.

Fix with actors, verbs, objects, dates, places, and consequences.

### Excessive Hedging

Watch for "it could potentially be argued", "may possibly", "in some ways", "to a certain extent", and "while specific details are limited".

Fix by either making the claim plainly or saying the evidence is not enough.

### Over-Neat Structure

Watch for identical paragraph lengths, mirrored sentence openings, generic headers, and a heading followed by a line that simply restates the heading.

Fix by varying paragraph size and cutting warm-up sentences.

### Formatting Tells

Watch for unnecessary emoji, boldface labels, decorative bullets, title case everywhere, overuse of em dashes, and perfectly consistent hyphenation.

Fix by using the formatting the situation actually needs.


## Integrity Pass

After rewriting, compare the new text against the original and check:

- no new names, numbers, dates, quotes, studies, source claims, or credentials appeared;
- uncertainty was not removed where it matters;
- quoted text stayed exact unless the user explicitly asked to paraphrase;
- sensitive/private material did not move to a broader surface;
- the text sounds like someone making choices, not a generic model smoothing prose.
