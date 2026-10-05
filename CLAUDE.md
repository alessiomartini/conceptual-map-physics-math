# CLAUDE.md

Big Picture: YAML content → static site (`docs/index.html`, GitHub Pages) + Anki deck (`dist/big-picture.apkg`).
Read `README.md` first (philosophy, schema, commands). Talk to Alessio in Italian; content and code are in English.

## Layout
- `content/{physics,math,experiments,concepts}/*.yaml` — one entry per file; `content/areas.yaml` clusters.
  `concept` domain = cross-field *threads* (`thread:` + `caveats:`); keep `concept` last in `areas.yaml`
  (Anki subdeck ids follow the order of the top-level keys).
- `scripts/common.py` (load, validate, warnings, inline markup), `build_site.py`, `build_anki.py`,
  `template.html` (the whole site: CSS + JS, d3 map, MathJax, feedback widget), `new_entry.py`.
- `worker/` — Cloudflare Worker + D1 for feedback (write-only). DB id is committed in `wrangler.jsonc`.
- `docs/` is committed (built site); `dist/` is ignored. The GitHub Action rebuilds both on push to main.

## Commands
- `make check` (validate; warnings for physics fields without experiments), `make` (check+site+anki), `make serve`.
- On Windows `make` works (python3 resolves); the preview config is `.claude/launch.json` ("site", port 8000).
- Read feedback: `cd worker && npx wrangler d1 execute conceptual-map-feedback --remote --command "select * from notes order by id desc"`.

## Content rules
- Never delete content; correct it. When a claim of Alessio's is imprecise, keep it and put the precise
  version in `caveats:` (see `concepts/eom-action-quantum.yaml`).
- Quote YAML items containing `": "` or starting with `* [ { \``. LaTeX: `$...$`; links `[[id]]`.
- After content edits: `make`, then check pages in the browser (MathJax errors show as red).
- Bump nothing for cache-busting: the site is a single self-contained HTML file.
