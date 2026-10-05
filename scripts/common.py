"""Shared loading, validation and inline-markup rendering for Big Picture.

Content lives in content/**/*.yaml. A file may hold a single entry (a mapping)
or a list of entries. See content/SCHEMA.md for the fields.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# Order and labels of the "guiding question" sections. Unknown list/str keys
# found in an entry are still rendered (title-cased) after these.
SECTIONS = [
    ("asks", "What questions does it try to answer?"),
    ("key_results", "Fundamental results"),
    ("experiments", "Empirical basis"),
    ("motivating_examples", "Motivating examples"),
    ("limits", "Limits & open problems"),
    ("applications", "Applications"),
    ("frontiers", "Where research is going"),
    # experiment entries
    ("measured", "What was measured"),
    ("result", "Result"),
    ("significance", "Why it matters"),
    # overview pages
    ("measuring_now", "What we are trying to measure"),
    ("cannot_measure", "What we cannot (yet) measure"),
]
SECTION_LABELS = dict(SECTIONS)

# Keys that are metadata, not sections.
META_KEYS = {
    "id", "title", "domain", "area", "one_liner", "summary", "connections",
    "prerequisites", "cards", "resources", "year", "who", "tags", "aliases",
    "status", "short", "order",
}

REQUIRED = ["id", "title", "domain", "area", "one_liner"]
DOMAINS = ["physics", "math", "experiment"]


def load_areas() -> dict:
    data = yaml.safe_load((CONTENT / "areas.yaml").read_text(encoding="utf-8"))
    return data


def load_entries() -> list[dict]:
    entries = []
    for path in sorted(CONTENT.rglob("*.yaml")):
        if path.name == "areas.yaml":
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data is None:
            continue
        items = data if isinstance(data, list) else [data]
        items = [_norm_backslashes(i) for i in items]
        for item in items:
            item["_file"] = str(path.relative_to(ROOT))
            entries.append(item)
    return entries


def _norm_backslashes(x):
    """Accept both \\alpha and \\\\alpha for LaTeX, whatever YAML quoting style was used."""
    if isinstance(x, str):
        return x.replace("\\\\", "\\")
    if isinstance(x, list):
        return [_norm_backslashes(y) for y in x]
    if isinstance(x, dict):
        return {k: _norm_backslashes(v) for k, v in x.items()}
    return x


REF_RE = re.compile(r"\[\[([a-z0-9\-]+)(?:\|([^\]]+))?\]\]")


def iter_text(entry):
    """Yield every string inside an entry (for ref checking)."""
    def walk(x):
        if isinstance(x, str):
            yield x
        elif isinstance(x, list):
            for y in x:
                yield from walk(y)
        elif isinstance(x, dict):
            for k, v in x.items():
                if not str(k).startswith("_"):
                    yield from walk(v)
    yield from walk(entry)


def validate(entries: list[dict], areas: dict) -> list[str]:
    errors = []
    ids = {}
    area_ids = {a["id"] for d in areas.values() for a in d["areas"]}
    for e in entries:
        where = e.get("_file", "?")
        for k in REQUIRED:
            if not e.get(k):
                errors.append(f"{where}: missing required key '{k}'")
        eid = e.get("id")
        if eid in ids:
            errors.append(f"{where}: duplicate id '{eid}' (also in {ids[eid]})")
        ids[eid] = where
        if e.get("domain") not in DOMAINS:
            errors.append(f"{where}: domain must be one of {DOMAINS}")
        if e.get("area") not in area_ids:
            errors.append(f"{where}: unknown area '{e.get('area')}' (define it in content/areas.yaml)")
        def ok_text(v):
            return isinstance(v, (str, int, float)) or (isinstance(v, list) and all(isinstance(x, (str, int, float)) for x in v))
        for key, _label, val in sections_of(e):
            if not ok_text(val):
                errors.append(f"{where} [{eid}]: section '{key}' must be text or a list of text "
                              f"(quote items containing ': ' or starting with * [ {{ ): {val!r:.120}")
        for k in ("one_liner", "summary", "who"):
            if e.get(k) is not None and not isinstance(e[k], str):
                errors.append(f"{where} [{eid}]: '{k}' must be text: {e[k]!r:.100}")
        for c in e.get("cards", []) or []:
            if not (isinstance(c, dict) and c.get("q") and c.get("a")):
                errors.append(f"{where} [{eid}]: every card needs 'q' and 'a' ({c!r:.80})")
            elif not (isinstance(c["q"], str) and ok_text(c["a"])):
                errors.append(f"{where} [{eid}]: card text malformed (quote it): {c!r:.120}")
    for e in entries:
        where = e.get("_file", "?")
        for key in ("connections", "prerequisites"):
            for ref in e.get(key, []) or []:
                if ref not in ids:
                    errors.append(f"{where}: {key} -> unknown id '{ref}'")
        for s in iter_text(e):
            for m in REF_RE.finditer(s):
                if m.group(1) not in ids:
                    errors.append(f"{where}: [[{m.group(1)}]] -> unknown id")
    return errors


def load_all(strict: bool = True):
    areas = load_areas()
    entries = load_entries()
    errors = validate(entries, areas)
    if errors:
        print("Content errors:", file=sys.stderr)
        for err in errors:
            print("  - " + err, file=sys.stderr)
        if strict:
            sys.exit(1)
    return entries, areas


# ---------------------------------------------------------------- markup
# Inline markup supported in every text field:
#   **bold**  *italic*  `code`  $math$  [[id]]  [[id|label]]  [text](https://url)
MATH_RE = re.compile(r"\$([^$]+)\$")
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def render_inline(text: str, titles: dict, target: str = "site") -> str:
    """Render the inline markup to HTML.

    target='site': math stays as $...$ for KaTeX, refs become hash links.
    target='anki': math becomes \\(...\\) for Anki's MathJax, refs become italics.
    """
    text = str(text)
    stash: list[str] = []

    def keep(s: str) -> str:
        stash.append(s)
        return f"\x00{len(stash) - 1}\x00"

    def math(m):
        body = html.escape(m.group(1), quote=False)
        return keep(f"\\({body}\\)" if target == "anki" else f"${body}$")

    text = MATH_RE.sub(math, text)
    text = html.escape(text, quote=False)

    def ref(m):
        rid, label = m.group(1), m.group(2)
        label = label or titles.get(rid, rid)
        if target == "anki":
            return keep(f"<i>{label}</i>")
        return keep(f'<a class="ref" href="#{rid}">{label}</a>')

    text = REF_RE.sub(ref, text)
    text = LINK_RE.sub(lambda m: keep(f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>'), text)
    text = re.sub(r"`([^`]+)`", lambda m: keep(f"<code>{m.group(1)}</code>"), text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
    return text


def sections_of(entry: dict):
    """Return [(key, label, value)] in canonical order, then any extra keys."""
    out = []
    seen = set()
    for key, label in SECTIONS:
        if entry.get(key):
            out.append((key, label, entry[key]))
            seen.add(key)
    for key, val in entry.items():
        if key in seen or key in META_KEYS or key.startswith("_"):
            continue
        if isinstance(val, (str, list)) and val:
            out.append((key, key.replace("_", " ").capitalize(), val))
    return out
