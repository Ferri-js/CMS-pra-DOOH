#!/usr/bin/env python3
"""
Lightweight SQL pattern scanner to detect risky SQL string construction in Python files.

It flags lines that contain SQL keywords (SELECT/INSERT/UPDATE/DELETE/DROP/CREATE)
and also contain string concatenation (+), f-strings, or .format() usage which can indicate
an insecure construction if used with untrusted input. It also flags `cursor.execute(`
lines that use f-strings or '+' concatenation directly.

This is intentionally conservative: it's designed to help catch risky patterns in PRs.
If a flagged occurrence is intentional and safe, update the code to use parameterized
queries or add a short code comment "# sql-scan: ignore" on the same line to silence the scanner.
"""
from __future__ import annotations
import os
import re
import sys
from typing import List, Tuple

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

IGNORED_DIRS = {
    '.git', '__pycache__', 'env', 'venv', 'node_modules', 'migrations', 'media', 'static'
}

SQL_KEYWORDS_RE = re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE)\b", re.I)
FSTRING_RE = re.compile(r"\bf[\"']")
FORMAT_RE = re.compile(r"\.format\(")
PLUS_RE = re.compile(r"\+")
PERCENT_S_RE = re.compile(r"%s")
CURSOR_EXEC_RE = re.compile(r"cursor\.execute\s*\(")
EXEC_HELPERS_RE = re.compile(r"execute_fetchall|execute_commit")

def should_ignore(path: str) -> bool:
    parts = set(path.split(os.sep))
    return bool(parts & IGNORED_DIRS)

def scan_file(path: str) -> List[Tuple[int, str, str]]:
    matches: List[Tuple[int, str, str]] = []
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            for i, raw_line in enumerate(fh, start=1):
                line = raw_line.strip()
                if not line or line.startswith('#'):
                    continue
                if '# sql-scan: ignore' in line:
                    continue

                # If the line contains SQL keyword and suspicious string ops, flag it
                if SQL_KEYWORDS_RE.search(line):
                    # Heuristic: treat parameterized queries using %s as safe (common DB-driver style)
                    if PERCENT_S_RE.search(line):
                        continue
                    # Heuristic: treat our helper wrappers as safe when they include %s
                    if EXEC_HELPERS_RE.search(line) and PERCENT_S_RE.search(line):
                        continue

                    if PLUS_RE.search(line) or FSTRING_RE.search(line) or FORMAT_RE.search(line):
                        matches.append((i, 'sql_keyword_with_concat_or_format', raw_line.rstrip('\n')))
                        continue

                # If cursor.execute is used with f-strings or concatenation, flag it
                if CURSOR_EXEC_RE.search(line):
                    # If using %s placeholders it's likely parameterized and safe
                    if PERCENT_S_RE.search(line):
                        continue
                    if FSTRING_RE.search(line) or PLUS_RE.search(line) or FORMAT_RE.search(line):
                        matches.append((i, 'cursor_execute_with_concat_or_format', raw_line.rstrip('\n')))
                        continue

    except (UnicodeDecodeError, OSError) as e:
        # Skip binary or unreadable files
        print(f"[sql-scan] skipping {path}: {e}", file=sys.stderr)
    return matches

def main() -> int:
    problems = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # prune ignored directories
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for fname in filenames:
            if not fname.endswith('.py'):
                continue
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, ROOT)
            if should_ignore(rel):
                continue
            file_matches = scan_file(full)
            for lineno, kind, code in file_matches:
                problems.append((rel, lineno, kind, code))

    if problems:
        print('\n[sql-scan] Found potentially risky SQL patterns:')
        for rel, lineno, kind, code in problems:
            print(f"- {rel}:{lineno} [{kind}] -> {code}")
        print('\nIf these are false positives, add a comment "# sql-scan: ignore" on the same line to bypass the check.')
        return 2

    print('[sql-scan] No suspicious SQL patterns found.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
