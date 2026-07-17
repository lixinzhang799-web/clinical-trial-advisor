#!/usr/bin/env python3
"""Search distilled Markdown references with regex terms."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Search skill reference notes")
    parser.add_argument("pattern", help="Regex, for example: 估计目标|伴发事件")
    parser.add_argument("--context", type=int, default=1, help="Context lines")
    args = parser.parse_args()

    try:
        expression = re.compile(args.pattern, re.IGNORECASE)
    except re.error as exc:
        parser.error(f"invalid regex: {exc}")

    reference_dir = Path(__file__).resolve().parent.parent / "references"
    matched = False
    for path in sorted(reference_dir.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        hit_indexes = [i for i, line in enumerate(lines) if expression.search(line)]
        if not hit_indexes:
            continue
        matched = True
        print(f"\n## {path.name}")
        shown: set[int] = set()
        for index in hit_indexes:
            start = max(0, index - args.context)
            end = min(len(lines), index + args.context + 1)
            for current in range(start, end):
                if current in shown:
                    continue
                shown.add(current)
                marker = ">" if current == index else " "
                print(f"{marker}{current + 1}: {lines[current]}")
    return 0 if matched else 1


if __name__ == "__main__":
    raise SystemExit(main())
