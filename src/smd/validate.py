from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .model import Directive, StoryDocument

SCENE_PURPOSE_NAMES = {"takeaway", "ask", "decision", "claim"}
CLAIM_NAMES = {"claim", "evidence"}
SOURCE_ATTRS = {"source", "sources"}


@dataclass
class Issue:
    level: str
    code: str
    message: str
    line: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "level": self.level,
            "code": self.code,
            "message": self.message,
            "line": self.line,
        }


def validate(doc: StoryDocument, *, strict: bool = False) -> list[Issue]:
    issues: list[Issue] = []
    seen_ids: dict[str, int] = {}

    if not doc.title and not doc.metadata.get("title"):
        issues.append(Issue("warning", "missing-title", "Document should have a title"))

    if not doc.scenes:
        issues.append(Issue("error", "missing-scenes", "Document must contain at least one ::scene"))

    for scene in doc.scenes:
        if not scene.id:
            issues.append(Issue("error", "scene-missing-id", "Scene is missing id", scene.line))
        else:
            _track_id(scene.id, scene.line, seen_ids, issues)

        if not scene.title:
            issues.append(Issue("warning", "scene-missing-title", "Scene should have a heading title", scene.line))

        if not _has_scene_purpose(scene.directives):
            issues.append(
                Issue(
                    "warning",
                    "scene-missing-purpose",
                    "Scene should include a takeaway, ask, decision, or claim",
                    scene.line,
                )
            )

        reveals = []
        for directive in scene.directives:
            directive_id = directive.id
            if directive_id:
                _track_id(directive_id, directive.line, seen_ids, issues)

            source_required = directive.name in CLAIM_NAMES or directive.role in CLAIM_NAMES
            if source_required and strict and not _has_source(directive):
                issues.append(
                    Issue(
                        "warning",
                        "claim-missing-source",
                        f"{directive.name} should include source= or sources= in strict mode",
                        directive.line,
                    )
                )

            if "reveal" in directive.attrs:
                reveal = directive.attrs["reveal"]
                if not isinstance(reveal, int):
                    issues.append(Issue("error", "invalid-reveal", "Reveal value must be an integer", directive.line))
                else:
                    reveals.append((reveal, directive.line))

        sorted_reveals = sorted(reveals)
        expected = list(range(1, len(sorted_reveals) + 1))
        actual = [reveal for reveal, _line in sorted_reveals]
        if actual and actual != expected:
            issues.append(
                Issue(
                    "warning",
                    "non-contiguous-reveals",
                    f"Reveal sequence should be contiguous from 1; found {actual}",
                    scene.line,
                )
            )

    return issues


def _track_id(id_value: str, line: int, seen_ids: dict[str, int], issues: list[Issue]) -> None:
    if id_value in seen_ids:
        issues.append(Issue("error", "duplicate-id", f"Duplicate id '{id_value}'", line))
    else:
        seen_ids[id_value] = line


def _has_scene_purpose(directives: Iterable[Directive]) -> bool:
    return any(directive.name in SCENE_PURPOSE_NAMES or directive.role in SCENE_PURPOSE_NAMES for directive in directives)


def _has_source(directive: Directive) -> bool:
    return any(attr in directive.attrs for attr in SOURCE_ATTRS)
