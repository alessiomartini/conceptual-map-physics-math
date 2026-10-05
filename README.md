# Big Picture

A personal atlas of physics (especially theoretical), mathematics and the experiments behind them.
One source of truth — a YAML file per field — builds two things:

- **a static website** (`docs/index.html`): an interactive map of fields and their connections,
  one page per field, *lenses* that compare every field's answer to the same question, and a
  timeline of key experiments;
- **an Anki deck** (`dist/big-picture.apkg`): atomic flashcards plus auto-generated overview cards.

Every field answers the same guiding questions:

| key | question |
|---|---|
| `asks` | What questions does it try to answer? |
| `key_results` | What are its fundamental results? |
| `experiments` | Which experiments is it built on? (physics) |
| `motivating_examples` | Where does it come from? (math) |
| `limits` | Where does it break / what is open? |
| `applications` | What is it used for? |
| `frontiers` | Where is research going? |

Experiments use `year`, `who`, `measured`, `result`, `significance`. Two overview pages collect
**what we are trying to measure now** and **what we cannot measure**.

## Quick start

```bash
pip install -r requirements.txt
make            # validate + build site + build Anki deck
make serve      # open http://localhost:8000
```

Import `dist/big-picture.apkg` into Anki (File → Import).

## Adding or editing content

```bash
python scripts/new_entry.py physics hep "Supersymmetry"   # creates content/physics/supersymmetry.yaml
make check                                                 # reports broken links / malformed YAML
```

- Fields live in `content/physics/`, `content/math/`, `content/experiments/`; clusters in `content/areas.yaml`.
- See `templates/entry.yaml` for every available key. Any extra list key you invent
  (e.g. `famous_people:`) is rendered as an extra section automatically.
- Inline markup in any text: `**bold**`, `*italic*`, `` `code` ``, `$\LaTeX$`, `[[entry-id]]` links,
  `[[entry-id|custom label]]`, `[text](https://…)`.
- YAML gotcha: quote an item (`'…'`) if it contains `": "` or starts with `*`, `[`, `{` or a backtick.
  `make check` tells you which file and item.

## Anki notes

- Re-importing an updated deck **updates** existing cards and keeps your review history: card
  identities come from the entry id + question text. If you reword a question but want to keep its
  history, give the card an explicit `id:` first.
- Tags are hierarchical: `bigpicture::physics::hep::qft`, `bigpicture::kind::atomic|overview`.
  Use them for filtered decks (e.g. `tag:bigpicture::math::*`).
- Subdecks: `Big Picture::Physics`, `::Mathematics`, `::Experiments`.
- Set `site_url` in `config.yaml` (your GitHub Pages URL) so each card links back to its page.
- Turn off auto-generated overview cards with `anki.overview_cards: false`.

## Publishing the site

Push to GitHub and enable Pages with "GitHub Actions" as source; `.github/workflows/build.yml`
rebuilds the site and the deck on every push. (Alternatively serve the `docs/` folder from the main branch.)

## Suggested study loop

1. Read one field page end to end, then its lens neighbours (e.g. *Limits* across the Fields cluster).
2. Do the Anki reviews daily; when a card feels empty, open its page via the link.
3. When you learn something new (a paper, a talk), add one bullet and one card to the relevant file.
4. Every few months, rewrite the `frontiers` sections — they age fastest.
