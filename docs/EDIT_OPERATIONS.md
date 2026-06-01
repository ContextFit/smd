# SMD Edit Operations

Status: draft 0.1

This document defines semantic mutations a UI or agent should perform on SMD files.

## Create Scene

Required:

- stable `id`
- heading/title

Recommended:

- `role`
- purpose directive such as `claim`, `ask`, `decision`, or `takeaway`

## Update Scene

Allowed:

- update title
- update scene attrs
- update scene markdown content
- add, update, or remove directives

Do not change `id` through this operation. Use rename ID.

## Create Directive

Required:

- directive `name`
- stable `id` for meaningful story atoms such as claims, evidence, asks, and takeaways

Recommended:

- `role`
- `source` or `sources` for claims and evidence
- `reveal` for ordered builds

## Rename ID

When renaming a scene or directive ID, update known references:

- source refs that point at the old ID
- include refs
- navigation state
- any renderer links

## Reorder Reveals

Reveal values should be contiguous integers starting at 1 inside each scene.

## Validate Before Save

Always validate before save:

```bash
smd validate path/to/file.smd --strict
```

Blocking errors should stop save unless the user explicitly saves a draft.
