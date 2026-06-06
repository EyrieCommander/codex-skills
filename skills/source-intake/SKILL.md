---
name: source-intake
description: Use when an inbound source should be preserved, interpreted, and optionally propagated into durable project state, including screenshots, web pages, social posts, articles, books, papers, meeting snippets, email excerpts, PDFs, repo notes, product pages, or user-provided source material. Do not use for one-off summaries unless the user asks to incorporate the source into a system, project, board, doc, skill, notice, or follow-up.
---

# Source Intake

Use this skill to turn an inbound source into durable project context without losing provenance or over-propagating weak ideas. It is source-type neutral: use it for social media, articles, books, PDFs, videos after transcription or perception, product pages, meeting snippets, email excerpts, screenshots, repo notes, or user-provided source material.

The goal is not a polished summary. The goal is a source-backed capture, a clear value judgment, and only the justified downstream updates.

## Choose The Owner

Store the capture under the project that owns the source or follow-up.

Use an existing project intake surface when one exists. If there is no project convention, use:

```text
<project>/captures/source-captures/YYYY-MM-DD-short-slug.md
<project>/captures/entity-propagation/YYYY-MM-DD-short-slug.md
```

If a platform-specific readback skill exists for a source, such as a social-media, email, browser, repository, calendar, or document connector workflow, use that focused skill first to retrieve the source accurately. Return here when the fetched source needs capture, interpretation, propagation, routing, or durable follow-up.

Do not copy every source into a central folder. Add only a pointer when the source changes cross-project priority, creates a shared task, affects doctrine, or needs approval from another owner.

## Preserve Provenance

Start every capture with the best available source trail:

- source URL, local file path, screenshot path, connector output, copied excerpt, bibliographic reference, or user-provided text;
- capture date and source date if known;
- who flagged it and why;
- source limits, missing context, or readback problems;
- sensitivity: public, private, work-sensitive, personal, connector-derived, or unknown.

For long-form sources such as books, papers, reports, PDFs, and articles, include title, author or publisher, edition/version when known, publication date, page/chapter/section/location references, and ISBN/DOI/URL when available.

Use small frontmatter when creating a capture:

```yaml
---
source_type:
source_ref:
captured_at:
sensitivity:
owner:
related_entities:
propagation_status:
---
```

Valid `propagation_status` values: `propagated`, `partial`, `deferred`, or `reference_only`. `reference_only` is a successful outcome when a source is worth preserving but does not justify edits elsewhere.

## Connector Privacy

Connector-derived sources need a sharper boundary than public web sources. Email, meeting notes, Drive-like documents, calendars, private repos, chat exports, and local files may be useful for local synthesis, but do not quote them into public artifacts, repo docs, launch materials, examples, or broadly shared notices unless the user explicitly approves that specific reuse.

When provenance is sensitive, preserve the pointer locally and summarize only what is safe for the target surface.

## Separate Facts From Use

In the capture, separate:

- what the source directly says or shows;
- what is inferred;
- what remains unverified;
- why the source matters to the current project;
- what should not be repeated publicly without approval.

Do not overquote. Use short excerpts only when exact wording matters; otherwise summarize. For books, articles, and other copyrighted long-form sources, prefer concise summaries with page or section references over extended quotation.

## Value Checkpoint

Before changing board items, doctrine, skills, notices, indexes, launch packets, or project docs, decide whether the user asked to propagate or only asked to consider.

Always allowed before the checkpoint:

- capture the source;
- summarize the core thesis;
- identify affected entities;
- draft a candidate propagation plan.

Pause for approval or discussion when:

- the user says "consider this", "what do you think", "could this be useful", or similar;
- the source implies adopting a new workflow, tool, protocol, public claim, or ongoing commitment;
- the value is uncertain;
- the change would create maintenance work;
- the source is interesting but may be overfit.

Proceed directly when the user explicitly asks to incorporate, update, deploy, propagate, generalize, or apply the source, or when the change is mechanical within an already approved intake task.

## Extract Entities

List affected entities before propagating:

- people;
- projects and repos;
- agents, assistants, or runtime helpers;
- workflows and concepts;
- board items and commitments;
- docs, skills, reports, packets, and indexes;
- approval needs, risks, and open questions.

For each entity choose one action:

- propagate now;
- create or update a board item;
- create or update a skill candidate;
- route to an owner;
- leave as reference only;
- defer with a visible follow-up.

## Update Only Justified Surfaces

Respect ownership. If the source belongs to another project, route to that project or create a local response artifact instead of editing its source-of-truth docs.

Common landing surfaces:

- capture and propagation report;
- board/status item;
- project source index;
- design log or lessons doc;
- vocabulary or doctrine;
- skill or skill candidate;
- notice or project message;
- launch packet or proof packet.

Do not send email, post publicly, mutate GitHub, publish, push, contact upstream, or make external changes unless the user explicitly approves that specific action.

## Finish

When propagation happens, create a short propagation report beside the capture. Include each entity, action taken, landing surface, and unresolved follow-up.

When propagation does not happen, end the capture with a no-propagation note explaining whether the outcome is `reference_only` or `deferred`.

Before treating a capture as ready, run this public-readiness check in plain language:

- source, date, and provenance are preserved;
- facts are separated from interpretation;
- sensitivity is named;
- every durable update is justified;
- `reference_only` was considered;
- no external mutation happened without approval;
- a brief propagation report or explicit no-propagation note exists.

Run only the validators required by touched surfaces:

- board/status item changed: regenerate board data;
- notice or hierarchy-visible state changed: validate notices and regenerate hierarchy data;
- Markdown/docs changed: run `git diff --check`.

End with capture path, propagation path if created, updated surfaces, unresolved follow-ups, and approval boundaries.

For human-readable Markdown, use one physical line per paragraph and blank lines only between paragraphs or sections. Lists, tables, frontmatter, and code blocks are exceptions.
