from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Directive:
    name: str
    attrs: dict[str, Any] = field(default_factory=dict)
    content: str = ""
    line: int = 0

    @property
    def id(self) -> str | None:
        value = self.attrs.get("id")
        return str(value) if value is not None else None

    @property
    def role(self) -> str | None:
        value = self.attrs.get("role")
        return str(value) if value is not None else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "attrs": self.attrs,
            "content": self.content,
            "line": self.line,
        }


@dataclass
class Scene:
    id: str | None
    title: str | None = None
    attrs: dict[str, Any] = field(default_factory=dict)
    content: str = ""
    directives: list[Directive] = field(default_factory=list)
    line: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "attrs": self.attrs,
            "content": self.content,
            "directives": [directive.to_dict() for directive in self.directives],
            "line": self.line,
        }


@dataclass
class StoryDocument:
    metadata: dict[str, Any] = field(default_factory=dict)
    title: str | None = None
    preamble: str = ""
    scenes: list[Scene] = field(default_factory=list)
    directives: list[Directive] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata,
            "title": self.title,
            "preamble": self.preamble,
            "directives": [directive.to_dict() for directive in self.directives],
            "scenes": [scene.to_dict() for scene in self.scenes],
        }
