#!/usr/bin/env python3
"""Build the static site from content/.

Outputs
  docs/index.html      full HTML document (serve docs/ with GitHub Pages)
  dist/artifact.html   same page without the <html>/<head> wrapper (for hosts
                       that add their own skeleton)
The page is a single self-contained file: all content is embedded as JSON.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from common import ROOT, SECTION_LABELS, load_all, render_inline, sections_of

LENSES = ["thread", "asks", "key_results", "experiments", "limits", "applications", "frontiers"]

WRAP = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
</head>
<body>
{body}
</body>
</html>
"""


def build_data(entries, areas, cfg):
    titles = {e["id"]: e["title"] for e in entries}
    r = lambda s: render_inline(s, titles, "site")
    # keep areas.yaml order, then file order inside each area
    order = {a["id"]: i for i, a in enumerate(a for d in areas.values() for a in d["areas"])}
    entries = sorted(entries, key=lambda e: (order[e["area"]], e.get("order", 10**6), e["title"]))
    out, n_cards = [], 0
    for e in entries:
        secs = []
        for key, label, val in sections_of(e):
            secs.append({"key": key, "label": label,
                         "value": [r(v) for v in val] if isinstance(val, list) else r(val)})
        cards = []
        for c in e.get("cards", []) or []:
            a = c["a"]
            cards.append({"q": r(c["q"]), "a": ("<ul>" + "".join(f"<li>{r(x)}</li>" for x in a) + "</ul>") if isinstance(a, list) else r(a)})
        n_cards += len(cards)
        search = " ".join([e["title"], e.get("short", ""), e["one_liner"], " ".join(e.get("aliases", []) or []),
                           " ".join(e.get("tags", []) or [])]).lower()
        out.append({
            "id": e["id"], "title": e["title"], "short": e.get("short"), "domain": e["domain"], "area": e["area"],
            "one_liner": r(e["one_liner"]), "summary": r(e["summary"]) if e.get("summary") else "",
            "who": r(e["who"]) if e.get("who") else "", "year": str(e["year"]) if e.get("year") else "",
            "sections": secs, "connections": e.get("connections", []) or [],
            "prerequisites": e.get("prerequisites", []) or [],
            "resources": [r(x) for x in e.get("resources", []) or []],
            "cards": cards, "search": search,
        })
    return {
        "config": {"title": cfg["title"], "subtitle": cfg.get("subtitle", ""),
                   "philosophy": [r(p) for p in cfg.get("philosophy", [])],
                   "feedback_url": cfg.get("feedback_url", ""), "repo": cfg.get("repo", "")},
        "areas": areas,
        "entries": out,
        "lenses": [{"key": k, "label": SECTION_LABELS[k]} for k in LENSES],
        "nCards": n_cards,
    }


def main():
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    entries, areas = load_all()
    data = build_data(entries, areas, cfg)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    tpl = (Path(__file__).parent / "template.html").read_text(encoding="utf-8")
    body = (tpl.replace("%%TITLE%%", cfg["title"]).replace("%%SUBTITLE%%", cfg.get("subtitle", ""))
               .replace("%%DATA%%", payload))
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "docs" / "index.html").write_text(WRAP.format(body=body), encoding="utf-8")
    (ROOT / "dist" / "artifact.html").write_text(body, encoding="utf-8")
    print(f"Wrote docs/index.html: {len(data['entries'])} entries, {data['nCards']} hand-written cards")


if __name__ == "__main__":
    main()
