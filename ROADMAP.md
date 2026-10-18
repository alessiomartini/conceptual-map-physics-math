# Roadmap

<!--
Unico file per todo, idee, decisioni e diario, letto da Projects Overview
(https://alessiomartini.github.io/projects-overview/). Protocollo: templates/ROADMAP.md di projects-overview.
-->

## Da fare
- [x] Mappa dei campi con collegamenti ed esperimenti
- [x] Link ai paper originali per circa 120 tappe
- [x] Mazzo Anki
- [ ] Nuovi fili concettuali (principi variazionali, linearità e sovrapposizione…)
- [ ] Link ai paper originali per i risultati restanti
- [ ] Pubblicare il `.apkg` come GitHub Release a ogni push
- [x] Vista "solo fili" sulla mappa

## Idee

- [ ] More threads (`content/concepts/`): variational principles beyond mechanics, linearity & superposition,
  geometry/curvature (GR ↔ gauge ↔ Berry phase), randomness & typicality, Hamiltonian vs Lagrangian in depth,
  "why mathematics fits physics".
- [ ] Original-paper links exist for ~120 milestones; extend to the remaining key results (verify each id via API).
- [ ] `definitions:` sections exist for chaos, non-equilibrium (thermalization), quantum gravity, integrability,
  complex systems, QFT, topological order; candidates: emergence, entropy (Boltzmann vs Gibbs), renormalization schemes.
- [ ] Publish the `.apkg` as a GitHub Release on each push (now only a workflow artifact) so Anki users can
  download it from a stable URL.
- [ ] Scheduled job that syncs the D1 feedback into the repo (as in eating-amsterdam) instead of reading it by hand (now an idea of the shared `site-notes` repo).
- [x] Map: optional "threads only" view that highlights the fields a selected thread passes through.
- [ ] Site note #7 (2026-10-05): use review papers as references for each field, e.g. the Snowmass 2021
  reports for high-energy physics (verify ids via the arXiv API, as for the original-paper links).
- [ ] Site note #9 (2026-10-06): hydrodynamics with higher-form symmetries (MHD as the hydrodynamics of a
  1-form symmetry, Grozdanov–Hofman–Iqbal) and anomalous hydrodynamics (ABJ / chiral magnetic effect), with
  which experiments support it; check whether it has been done beyond 1-form symmetries.

## Decisioni e cose provate

### Done / history

- 2026-10-05 (2): feedback #6 (anomaly taxonomy); Anki deck rebuilt around context (big goal, essentials,
  broken promises, place on the map) — 454 notes instead of 624 technical ones.
- 2026-10-05: site feedback #2–#5 handled — light/dark toggle, original-paper links, `definitions:` sections,
  stability thread; added supersymmetry, soft & active matter, optics, geophysics & climate, statistics, TQFT.
- 2026-10: project created by Cowork in `big-picture/big-picture/`; moved to repo root, ODE/SDE, philosophy
  of physics/mathematics, concept threads, feedback Worker, content review, public GitHub Pages site.

## Log
- 2026-10-18: 🤖 mappa: menu "Thread" che evidenzia il filo scelto e i campi a cui rimanda (`connections`), sfumando il resto
- 2026-10-19: note del sito portate nel ROADMAP (#7 e #9 nelle Idee; #8, TLC generalizzato, era già in `probability-theory`); feedback spostato nel backend unico `site-notes` (tolto `worker/`; vecchio worker `conceptual-map-feedback` e D1 spenti)
- 2026-10-18: FUTURE-ARCHITECTURE.md unito in ROADMAP.md (protocollo unico)
- 2026-10-15: creata la roadmap per Projects Overview
