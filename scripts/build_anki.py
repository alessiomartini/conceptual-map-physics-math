#!/usr/bin/env python3
"""Build dist/big-picture.apkg from content/.

Card GUIDs are stable (derived from entry id + card id or question text), so
re-importing an updated deck updates existing cards and keeps your review
history. Changing a card's question text creates a new card unless you give
the card an explicit `id:`.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path

import genanki
import yaml

from common import ROOT, load_all, render_inline

MODEL_ID = 1730091001  # never change: Anki uses it to recognise the note type
DECK_ID_BASE = 1730092000

CSS = """
.card { font-family: -apple-system, 'Segoe UI', Roboto, sans-serif; font-size: 19px;
        line-height: 1.45; text-align: left; color: #17202b; background: #f6f7f9;
        max-width: 640px; margin: 0 auto; padding: 8px 14px; }
.nightMode.card, .night_mode .card { color: #e3e8ef; background: #12171e; }
.ctx { font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: #5b6878; margin-bottom: 10px; }
.ctx b { color: #2f4fd1; font-weight: 600; }
.nightMode .ctx b, .night_mode .ctx b { color: #8ea5ff; }
.q { font-size: 21px; font-weight: 600; }
.a { margin-top: 4px; }
.a ul { padding-left: 1.1em; margin: .3em 0; }
.a li { margin: .25em 0; }
.more { margin-top: 14px; font-size: 13px; color: #5b6878; }
.more a { color: inherit; }
code { font-size: .9em; background: rgba(120,130,150,.15); padding: 0 .25em; border-radius: 3px; }
hr#answer { border: none; border-top: 1px solid rgba(120,130,150,.35); margin: 14px 0; }
"""

MODEL = genanki.Model(
    MODEL_ID,
    "Big Picture",
    fields=[
        {"name": "Front"}, {"name": "Back"}, {"name": "Field"},
        {"name": "Context"}, {"name": "Link"}, {"name": "EntryId"},
    ],
    templates=[{
        "name": "Card",
        "qfmt": '<div class="ctx"><b>{{Field}}</b>{{#Context}} · {{Context}}{{/Context}}</div><div class="q">{{Front}}</div>',
        "afmt": '{{FrontSide}}<hr id="answer"><div class="a">{{Back}}</div>'
                '{{#Link}}<div class="more"><a href="{{Link}}">Open in Big Picture →</a></div>{{/Link}}',
    }],
    css=CSS,
)


def as_html(value, titles) -> str:
    if isinstance(value, list):
        items = "".join(f"<li>{render_inline(v, titles, 'anki')}</li>" for v in value)
        return f"<ul>{items}</ul>"
    return render_inline(value, titles, "anki")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "dist" / "big-picture.apkg"))
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / "config.yaml").read_text())
    entries, areas = load_all()
    titles = {e["id"]: e["title"] for e in entries}
    area_label = {a["id"]: a["label"] for d in areas.values() for a in d["areas"]}
    site = (cfg.get("site_url") or "").rstrip("/")
    root_name = cfg["anki"]["deck_name"]
    overview = cfg["anki"].get("overview_cards", True)

    decks = {}
    for i, (dom, d) in enumerate(areas.items()):
        decks[dom] = genanki.Deck(DECK_ID_BASE + i, f"{root_name}::{d['label']}")

    n = 0
    for e in entries:
        eid, title, dom = e["id"], e["title"], e["domain"]
        link = f"{site}/#{eid}" if site else ""
        ctx = html.escape(area_label.get(e["area"], ""))
        base_tags = [f"bigpicture::{dom}::{e['area']}::{eid}"] + [f"bigpicture::tag::{t}" for t in e.get("tags", [])]

        def add(q, a, key, kind):
            nonlocal n
            note = genanki.Note(
                model=MODEL,
                fields=[render_inline(q, titles, "anki"), a, html.escape(title), ctx, link, eid],
                guid=genanki.guid_for(eid, key),
                tags=base_tags + [f"bigpicture::kind::{kind}"],
            )
            decks[dom].add_note(note)
            n += 1

        if overview:
            if dom == "experiment" and e.get("significance"):
                when = f" ({e['year']})" if e.get("year") else ""
                add(f"What did <b>{title}</b>{when} establish, and why does it matter?",
                    as_html(e["significance"], titles), "auto:significance", "overview")
            elif dom != "experiment":
                add(f"<b>{title}</b> in one sentence?",
                    as_html(e["one_liner"], titles), "auto:one-liner", "overview")
                if e.get("asks"):
                    add(f"What questions does <b>{title}</b> try to answer?",
                        as_html(e["asks"], titles), "auto:asks", "overview")
        for c in e.get("cards", []) or []:
            add(c["q"], as_html(c["a"], titles), c.get("id") or c["q"], "atomic")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(list(decks.values())).write_to_file(out)
    print(f"Wrote {out.relative_to(ROOT)}: {n} notes from {len(entries)} entries")


if __name__ == "__main__":
    main()
