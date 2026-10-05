#!/usr/bin/env python3
"""Create a new entry from templates/entry.yaml.

Usage:  python scripts/new_entry.py physics hep "Supersymmetry"
"""
import re
import sys

from common import ROOT, load_areas

DIRS = {"physics": "physics", "math": "math", "experiment": "experiments"}


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    domain, area, title = sys.argv[1:]
    if domain not in DIRS:
        sys.exit(f"domain must be one of {list(DIRS)}")
    areas = load_areas()
    valid = [a["id"] for a in areas[domain]["areas"]]
    if area not in valid:
        sys.exit(f"area must be one of {valid} (or add it to content/areas.yaml)")
    eid = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if domain == "experiment" and not eid.startswith("exp-"):
        eid = "exp-" + eid
    path = ROOT / "content" / DIRS[domain] / f"{eid}.yaml"
    if path.exists():
        sys.exit(f"{path} already exists")
    tpl = (ROOT / "templates" / "entry.yaml").read_text(encoding="utf-8")
    body = "\n".join(l for l in tpl.splitlines() if not l.startswith("#"))
    body = (body.replace("id: my-field", f"id: {eid}").replace("title: My Field", f"title: {title}")
                .replace("short: My field", f"short: {title}").replace("domain: physics", f"domain: {domain}")
                .replace("area: hep", f"area: {area}"))
    body = re.sub(r"\s+#.*$", "", body, flags=re.M)
    path.write_text(body + "\n", encoding="utf-8")
    print(f"Created {path.relative_to(ROOT)} — fill it in, then run `make`.")


if __name__ == "__main__":
    main()
