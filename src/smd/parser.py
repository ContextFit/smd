from __future__ import annotations

import re
import shlex
from pathlib import Path
from typing import Any

import yaml

from .model import Directive, Scene, StoryDocument

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+\{#([A-Za-z0-9_.:-]+)\})?\s*$")
DIRECTIVE_RE = re.compile(r"^(::+)([A-Za-z][A-Za-z0-9_-]*)(?:\s+(.*?))?\s*$")
CLOSE_RE = re.compile(r"^::+\s*$")


def parse_file(path: str | Path) -> StoryDocument:
    path = Path(path)
    return parse_text(path.read_text(encoding="utf-8"))


def parse_text(text: str) -> StoryDocument:
    metadata, body = _split_frontmatter(text)
    doc = StoryDocument(metadata=metadata)
    lines = body.splitlines()
    current_scene: Scene | None = None
    scene_content: list[str] = []
    preamble: list[str] = []
    pending_heading: tuple[str, int] | None = None
    i = 0

    while i < len(lines):
        line = lines[i]
        line_no = i + 1
        heading = HEADING_RE.match(line)
        if heading:
            heading_text = heading.group(2).strip()
            heading_id = heading.group(3)
            if heading.group(1) == "#" and doc.title is None:
                doc.title = heading_text
            pending_heading = (heading_text, line_no)
            if current_scene is None:
                preamble.append(line)
            else:
                scene_content.append(line)
            i += 1
            continue

        directive = DIRECTIVE_RE.match(line)
        if directive:
            marker, name, raw_attrs = directive.groups()
            attrs = _parse_attrs(raw_attrs or "")
            block_content = ""
            start_line = line_no
            if len(marker) >= 3:
                content_lines: list[str] = []
                i += 1
                while i < len(lines) and not CLOSE_RE.match(lines[i]):
                    content_lines.append(lines[i])
                    i += 1
                block_content = "\n".join(content_lines).strip("\n")
                if i < len(lines):
                    i += 1
            else:
                i += 1

            item = Directive(name=name, attrs=attrs, content=block_content, line=start_line)
            if name == "scene":
                if pending_heading:
                    while scene_content and scene_content[-1] == "":
                        scene_content.pop()
                    if scene_content and scene_content[-1].startswith("#"):
                        scene_content.pop()
                if current_scene is not None:
                    current_scene.content = "\n".join(scene_content).strip("\n")
                    doc.scenes.append(current_scene)
                    scene_content = []
                scene_id = str(attrs["id"]) if "id" in attrs else None
                scene_title = pending_heading[0] if pending_heading else None
                current_scene = Scene(id=scene_id, title=scene_title, attrs=attrs, line=start_line)
                pending_heading = None
                continue

            if current_scene is None:
                doc.directives.append(item)
                preamble.append(line)
            else:
                current_scene.directives.append(item)
            continue

        if current_scene is None:
            preamble.append(line)
        else:
            scene_content.append(line)
        i += 1

    if current_scene is not None:
        current_scene.content = "\n".join(scene_content).strip("\n")
        doc.scenes.append(current_scene)
    doc.preamble = "\n".join(preamble).strip("\n")
    return doc


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 4 :].lstrip("\n")
    data = yaml.safe_load(raw) if raw else {}
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError("Frontmatter must be a YAML mapping")
    return data, body


def _parse_attrs(raw: str) -> dict[str, Any]:
    attrs: dict[str, Any] = {}
    if not raw.strip():
        return attrs
    for token in shlex.split(raw):
        if "=" not in token:
            attrs[token] = True
            continue
        key, value = token.split("=", 1)
        attrs[key] = _parse_value(value)
    return attrs


def _parse_value(value: str) -> Any:
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.isdigit():
        return int(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip() for part in inner.split(",")]
    return value
