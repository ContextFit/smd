# SMD Specification

Status: draft 0.1

SMD, or Story Markdown, is a Markdown-compatible format for agent-native presentations and structured storytelling.

## Design Goals

- Preserve readable Markdown as the source of truth.
- Make every meaningful story unit addressable with stable IDs.
- Represent a presentation as an argument graph, not just a list of slides.
- Keep layout and animation guidance semantic rather than pixel-bound.
- Let renderers, agents, and retrieval systems consume the same artifact.

## File Extension

SMD files use the `.smd` extension.

## Frontmatter

Files may start with YAML frontmatter:

```yaml
---
type: story-deck
version: 0.1
title: Product Narrative
audiences:
  investor:
    emphasis: market, moat, traction
render:
  template: investor-briefing
  aspect: "16:9"
---
```

Recommended fields:

- `type`: `story`, `story-deck`, `briefing`, or another stable document type
- `version`: SMD spec version
- `title`: document title
- `audience` or `audiences`: target audience definition
- `render`: renderer-neutral template hints

## Directives

SMD uses colon directives:

```markdown
::scene id=intro role=hook
::layout mode=hero emphasis=title

:::claim id=main-claim source=research-note#claim
The story claim goes here.
::
```

Single-colon-pair directives are inline metadata markers. Triple-colon directives contain block content.

Attribute values support strings, integers, booleans, and simple arrays:

```markdown
::beat id=proof role=evidence reveal=2 tags=[benchmarks,retrieval]
```

## Core Primitives

- `scene`: a slide-like narrative unit
- `beat`: a reveal or reasoning step inside a scene
- `claim`: an assertion
- `evidence`: support for a claim
- `example`: concrete illustration
- `counterpoint`: objection or alternate framing
- `reframe`: shift in interpretation
- `ask`: requested decision or action
- `takeaway`: what the audience should remember
- `layout`: semantic placement guidance
- `motion`: semantic animation and reveal guidance
- `speaker-notes`: presenter-only notes
- `viewer-notes`: export or article-mode notes
- `agent-notes`: future-agent guidance
- `include`: reusable story atom reference

## IDs

Every `scene`, `claim`, `beat`, `evidence`, `ask`, and `takeaway` should have a stable `id`.

IDs should be lowercase, readable, and durable:

```markdown
:::claim id=ai-data-buyer-value
AI buyers care about coverage, metadata, rights, and model usefulness.
::
```

## Roles

Common roles:

- `hook`
- `problem`
- `claim`
- `evidence`
- `example`
- `counterpoint`
- `reframe`
- `decision`
- `ask`
- `takeaway`
- `transition`

## Layout

Layout guidance is semantic:

```markdown
::layout mode=compare primary=claim secondary=evidence
```

Recommended layout modes:

- `hero`
- `compare`
- `stack`
- `timeline`
- `grid`
- `quote`
- `chart-focus`
- `image-led`

Renderers decide concrete placement.

## Motion

Motion guidance should encode reveal meaning, not CSS implementation:

```markdown
::motion sequence=claim-then-proof pace=deliberate emphasis=final-takeaway
```

Recommended motion values:

- `none`
- `reveal`
- `sequence`
- `build`
- `zoom`
- `pan`
- `fade`
- `morph`

## Sources

Claims and evidence may include `source=` or `sources=` references:

```markdown
:::claim id=gtm-split source=meeting-2026-05-29#gtm-split
AI-company buyers and traditional drone-data buyers need different GTM motions.
::
```

Sources are renderer-neutral strings. A ContextFit integration can resolve them to indexed spans.

## Validation

The reference validator checks:

- document has a title
- document has at least one scene
- scenes have IDs
- IDs are unique
- scenes have a title
- scenes include a purpose marker such as claim, ask, decision, or takeaway
- reveal numbers are integer and contiguous
- strict mode warns when claims lack sources

## UI Integration

Renderers and UI agents should start from the JSON export contract rather than scraping raw SMD text.

See:

- [UI integration guide](docs/UI_INTEGRATION.md)
- [JSON contract](docs/JSON_CONTRACT.md)
- [Edit operations](docs/EDIT_OPERATIONS.md)
- [JSON schema](schema/smd.schema.json)
