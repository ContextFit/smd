# SMD: Story Markdown

**Agent-native presentation and storytelling format**

SMD is a markdown-based format for writing structured stories, presentations, briefings, and argument-driven documents that are:

- **Human-readable**: Edit in any text editor
- **Git-friendly**: Clean diffs, durable source files
- **Token-efficient**: Designed for LLM and agent consumption
- **Renderer-neutral**: Web UIs can map semantic guidance into their own templates
- **Argument-aware**: Claims, evidence, asks, reveals, and takeaways are first-class

## Quick Example

```markdown
---
type: story-deck
version: 0.1
title: "ContextFit: Token-Native Agent Memory"
audience: AI infrastructure founders and engineers
render:
  template: investor-briefing
  aspect: "16:9"
---

# ContextFit changes how agents remember {#opening}

::scene id=intro role=hook
::layout mode=hero emphasis=title
::motion sequence=claim-then-proof pace=deliberate

:::claim id=contextfit-thesis source=whitepaper#token-native
Agents do not need bigger context windows as much as they need better memory retrieval.
::

:::beat id=old-way role=problem reveal=1
Most retrieval systems translate memory into vector space and lose source-level structure.
::

:::beat id=new-way role=reframe reveal=2
ContextFit stays token-native, making memory indexable, attributable, and agent-friendly.
::

:::takeaway id=opening-takeaway
The real product is not a slide; it is a structured argument graph.
::
```

## CLI Usage

```bash
# Parse and inspect
smd parse examples/contextfit.smd

# Validate
smd validate examples/contextfit.smd
smd validate examples/contextfit.smd --strict

# Export for renderers or ContextFit ingest
smd export examples/contextfit.smd --format json
```

## Integration Docs

- [UI integration guide](docs/UI_INTEGRATION.md)
- [JSON contract](docs/JSON_CONTRACT.md)
- [Edit operations](docs/EDIT_OPERATIONS.md)
- [JSON schema](schema/smd.schema.json)

## Python API

```python
from smd import parse_file, validate

doc = parse_file("examples/contextfit.smd")
issues = validate(doc, strict=True)

for scene in doc.scenes:
    print(scene.id, scene.title)
```

## Core Idea

SMD separates three concerns:

1. **Content**: plain narrative, claims, quotes, evidence, examples, and notes
2. **Structure**: stable IDs, scenes, beats, roles, sources, and takeaways
3. **Direction**: semantic layout, motion, pacing, emphasis, and audience variants

Content must stand alone. Directives must enhance. Renderers must be replaceable.

See [SPEC.md](SPEC.md) for the draft specification.
