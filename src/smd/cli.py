from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .parser import parse_file
from .validate import validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="smd", description="Story Markdown tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_parser = subparsers.add_parser("parse", help="Parse a .smd file and print JSON AST")
    parse_parser.add_argument("path")

    validate_parser = subparsers.add_parser("validate", help="Validate a .smd file")
    validate_parser.add_argument("path")
    validate_parser.add_argument("--strict", action="store_true", help="Warn when claims lack sources")
    validate_parser.add_argument("--json", action="store_true", help="Print validation issues as JSON")

    export_parser = subparsers.add_parser("export", help="Export a .smd file")
    export_parser.add_argument("path")
    export_parser.add_argument("--format", choices=["json"], default="json")

    args = parser.parse_args(argv)
    path = Path(args.path)

    if args.command == "parse":
        doc = parse_file(path)
        print(json.dumps(doc.to_dict(), indent=2))
        return 0

    if args.command == "export":
        doc = parse_file(path)
        print(json.dumps(doc.to_dict(), indent=2))
        return 0

    if args.command == "validate":
        doc = parse_file(path)
        issues = validate(doc, strict=args.strict)
        if args.json:
            print(json.dumps([issue.to_dict() for issue in issues], indent=2))
        else:
            if not issues:
                print(f"{path}: OK")
            for issue in issues:
                location = f":{issue.line}" if issue.line else ""
                print(f"{path}{location}: {issue.level}: {issue.code}: {issue.message}")
        return 1 if any(issue.level == "error" for issue in issues) else 0

    print("Unknown command", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
