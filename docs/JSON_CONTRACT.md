# SMD JSON Contract

Status: draft 0.1

The SMD JSON contract is the reference interchange shape for renderers, UI agents, ingestion pipelines, and tests.

Generate it with:

```bash
smd export examples/contextfit.smd --format json
```

## Top-Level Shape

```json
{
  "metadata": {},
  "title": "Example",
  "preamble": "",
  "directives": [],
  "scenes": []
}
```

## Scene

```json
{
  "id": "intro",
  "title": "Opening",
  "attrs": {
    "id": "intro",
    "role": "hook"
  },
  "content": "",
  "directives": [],
  "line": 12
}
```

## Directive

```json
{
  "name": "claim",
  "attrs": {
    "id": "main-claim",
    "source": "whitepaper#claim"
  },
  "content": "The claim text.",
  "line": 18
}
```

## Compatibility Rules

- Unknown top-level fields should be ignored.
- Unknown `attrs` fields should be preserved.
- Scene IDs and directive IDs are stable handles.
- UI state that is not semantically meaningful should live outside SMD.
- Renderers should not replace SMD source with slide-specific output.
