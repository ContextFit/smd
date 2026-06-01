# SMD UI Integration Guide

Status: draft 0.1

This guide is for AI-native UI agents and applications that want to render, edit, and round-trip SMD files.

## Integration Principle

SMD is structured story source, not a slide canvas.

The UI should treat scenes, directives, IDs, roles, reveal order, and sources as canonical story objects. Pixel layout, animation CSS, and renderer-specific templates are outputs or view state.

## Recommended First Path

1. Parse SMD through the reference CLI:

```bash
smd export path/to/file.smd --format json
```

2. Render from the exported JSON object model.
3. Preserve stable IDs during edits.
4. Validate before save:

```bash
smd validate path/to/file.smd --strict
```

5. Round-trip edits back into `.smd` source.

## Object Model

The JSON export has these top-level fields:

- `metadata`: frontmatter key/value data
- `title`: document title
- `preamble`: non-scene introductory text
- `directives[]`: document-level directives
- `scenes[]`: scene objects

Each scene has:

- `id`
- `title`
- `attrs`
- `content`
- `directives[]`
- `line`

Each directive has:

- `name`
- `attrs`
- `content`
- `line`

## UI Surfaces

For a first SMD implementation, build these surfaces before building a slide editor:

- scene rail
- scene stack / preview
- directive inspector
- source/provenance panel
- reveal order panel
- validation panel
- export controls
- raw SMD source pane or revealable editor

## Required Behaviors

- Preserve scene and directive IDs unless the user explicitly renames them.
- Treat `layout` and `motion` as semantic hints, not concrete CSS.
- Treat `source` and `sources` as provenance.
- Keep renderer-only state outside SMD unless it is intentionally promoted to semantic guidance.
- Validate before saving.
- Show strict-mode warnings when claims or evidence lack sources.

## Edit Operations

Recommended primitive operations:

- create scene
- update scene attrs
- create directive in scene
- update directive attrs/content
- reorder scenes
- reorder reveal directives
- rename ID with reference updates
- attach source to claim/evidence
- validate document
- export JSON

## Render Guidance

Renderers should use:

- scene `role` to shape emphasis
- directive `name` and `role` to choose component treatment
- `layout` directive attrs for semantic composition
- `motion` directive attrs for reveal sequencing
- `reveal` attrs for ordered builds

Do not require exact slide coordinates in v1.

## ContextFit Integration

A ContextFit ingestion path should chunk SMD by:

- whole document
- each scene
- each claim/evidence/ask/takeaway directive
- optional scene neighborhoods

Recommended metadata:

- `smd_kind`
- `smd_scene_id`
- `smd_scene_role`
- `smd_scene_title`
- `smd_directive_name`
- `smd_directive_id`
- `smd_sources`
- `smd_reveal`
- `line`
