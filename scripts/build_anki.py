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

import re

from common import REF_RE, ROOT, iter_text, load_all, render_inline

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

    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    entries, areas = load_all()
    titles = {e["id"]: e["title"] for e in entries}
    area_label = {a["id"]: a["label"] for d in areas.values() for a in d["areas"]}
    site = (cfg.get("site_url") or "").rstrip("/")
    root_name = cfg["anki"]["deck_name"]
    details = cfg["anki"].get("detail_cards", False)

    decks = {}
    for i, (dom, d) in enumerate(areas.items()):
        decks[dom] = genanki.Deck(DECK_ID_BASE + i, f"{root_name}::{d['label']}")
    detail_deck = genanki.Deck(DECK_ID_BASE + 99, f"{root_name}::Details (optional)")

    # Who links to whom (both directions), and which threads pass through each entry.
    nb = {e["id"]: [] for e in entries}
    for e in entries:
        refs = list(dict.fromkeys((e.get("connections") or []) + [m.group(1) for x in iter_text(e) for m in REF_RE.finditer(x)]))
        for r in refs:
            if r in nb and r != e["id"]:
                if r not in nb[e["id"]]: nb[e["id"]].append(r)
                if e["id"] not in nb[r]: nb[r].append(e["id"])
    dom_of = {e["id"]: e["domain"] for e in entries}
    names = lambda ids: ", ".join(titles[i] for i in ids) or "—"

    n = 0
    for e in entries:
        eid, title, dom = e["id"], e["title"], e["domain"]
        link = f"{site}/#{eid}" if site else ""
        ctx = html.escape(area_label.get(e["area"], ""))
        base_tags = [f"bigpicture::{dom}::{e['area']}::{eid}"] + [f"bigpicture::tag::{t}" for t in e.get("tags", [])]

        def add(q, a, key, kind, deck=None):
            nonlocal n
            note = genanki.Note(
                model=MODEL,
                fields=[render_inline(q, titles, "anki"), a, html.escape(title), ctx, link, eid],
                guid=genanki.guid_for(eid, key),
                tags=base_tags + [f"bigpicture::kind::{kind}"],
            )
            (deck or decks[dom]).add_note(note)
            n += 1

        t = f"**{title}**"
        if dom in ("physics", "math"):
            # The deck is about context, not about memorising each framework.
            add(f"What is {t} about?", as_html(e["one_liner"], titles), "auto:one-liner", "context")
            fields = [x for x in nb[eid] if dom_of[x] in ("physics", "math")]
            exps = [x for x in nb[eid] if dom_of[x] == "experiment"]
            threads = [x for x in nb[eid] if dom_of[x] == "concept"]
            where = (f"<b>Cluster:</b> {ctx}<br><b>Builds on:</b> {html.escape(names(e.get('prerequisites') or []))}"
                     f"<br><b>Connected to:</b> {html.escape(names(fields[:8]))}"
                     + (f"<br><b>Experiments:</b> {html.escape(names(exps))}" if exps else "")
                     + (f"<br><b>Threads through it:</b> {html.escape(names(threads))}" if threads else ""))
            add(f"Where does {t} sit on the map?", where, "auto:map", "context")
            if e.get("big_goal"):
                add(f"What is the big goal of {t}?", as_html(e["big_goal"], titles), "auto:big-goal", "context")
            if e.get("essentials"):
                add(f"{t}: which results are worth remembering?", as_html(e["essentials"], titles), "auto:essentials", "context")
            if e.get("broken_promises"):
                add(f"What did {t} hope to answer, and why can't it?", as_html(e["broken_promises"], titles), "auto:broken-promises", "context")
        elif dom == "concept":
            add(f"Thread {t}: the idea in one sentence?", as_html(e["one_liner"], titles), "auto:one-liner", "thread")
            steps = [m.group(1) for x in e.get("thread", []) for m in [re.match(r"\*\*(.+?)\*\*", x)] if m]
            if steps:
                add(f"Thread {t}: what are its steps, in order?", "<ol>" + "".join(f"<li>{render_inline(x, titles, 'anki')}</li>" for x in steps) + "</ol>", "auto:steps", "thread")
            for c in [c for c in e.get("cards", []) or [] if not c.get("detail")]:   # thread cards ask *why* fields connect
                add(c["q"], as_html(c["a"], titles), c.get("id") or c["q"], "thread")
        elif dom == "experiment" and e.get("significance"):
            when = f" ({e['year']})" if e.get("year") else ""
            tested = [x for x in nb[eid] if dom_of[x] == "physics"]
            add(f"What did {t}{when} establish, and why does it matter?",
                as_html(e["significance"], titles) + (f"<p><b>Fields it supports:</b> {html.escape(names(tested))}</p>" if tested else ""),
                "auto:significance", "context")
        if details and dom != "concept":
            for c in e.get("cards", []) or []:
                add(c["q"], as_html(c["a"], titles), c.get("id") or c["q"], "detail", detail_deck)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(list(decks.values()) + ([detail_deck] if details else [])).write_to_file(out)
    print(f"Wrote {out.relative_to(ROOT)}: {n} notes from {len(entries)} entries")


if __name__ == "__main__":
    main()
