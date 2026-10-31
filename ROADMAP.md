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
- [x] Filo "Linearity and superposition" (`content/concepts/linearity-superposition.yaml`)
  - [x] Filo "Variational principles" (`content/concepts/variational-principles.yaml`)
  - [x] Filo "Geometry and curvature" (GR ↔ gauge ↔ fase di Berry) (`content/concepts/geometry-curvature.yaml`)
  - [x] Filo "Fluctuations and response" (fluttuazioni ↔ dissipazione ↔ suscettività) (`content/concepts/fluctuations-response.yaml`)
  - [x] Filo "Scaling and dimensional analysis" (`content/concepts/scaling-dimensional-analysis.yaml`)
  - [x] Filo "Randomness and probability" (ignoranza vs fondamentale, ergodicità, Einstein/Perrin, LGN/TCL, Born, caos, large deviations, matrici casuali; sezione `definitions` sul significato di probabilità) (`content/concepts/randomness-probability.yaml`)
- [ ] Link ai paper originali per i risultati restanti
  - [x] Altri 24 link verificati (arXiv/Crossref) su 21 tappe di fisica (CFT, complessità, QFT/EFT, biofisica, fondamenti quantistici, reti, geofisica…)
  - [x] Quarto lotto: 20 link (Crossref; arXiv via record DataCite) su 17 tappe di fisica, matematica e fili concettuali
  - [x] Quinto lotto: 18 link (Crossref; arXiv via API) su 14 tappe di matematica e fisica (Deligne, AKS, Appel–Haken, Yau, Cohen, Hales, Hairer, Schramm, Hopfield, AlphaFold, Parisi, Maxwell, STED/PALM, Kolmogorov…)
  - [x] Sesto lotto: 30 link (Crossref; arXiv via API) su 27 tappe di fisica e matematica (Parke–Taylor, Nielsen–Ninomiya, Dyson/Altland–Zirnbauer, Tracy–Widom, Coleman–Mandula/HLS, Faddeev–Popov, Landauer, Lawson, Black–Scholes, Markowitz, Hawking, Schoen–Yau/Witten, Onsager, Chandrasekhar, Dirac…)
  - [x] Settimo lotto: 29 link (Crossref; arXiv via API) su 20 tappe di fisica (BEC 1995, Laughlin/Tsui, Wilson-Kondo, Feynman, Goldstone, Choi–Lam–Shao/Córdova–Ohmori, Shor/Steane, Tao–Vu, Zeh/Zurek, swampland, Weizsäcker/Mayer, Newman, Axelrod, Deffuant, Helbing, Alfvén, Polchinski/Wetterich, Hubble, Aharonov–Bohm…)
  - [x] Ottavo lotto: 20 link (esperimenti/tappe: Aharonov–Bohm, Planck, Cavendish, doppia fenditura, Eddington, g−2, superconduttività, Gargamelle/UA1/top, Bednorz–Müller, grafene) su 9 voci
- [x] Pubblicare il `.apkg` come GitHub Release a ogni push
- [x] Vista "solo fili" sulla mappa

## Idee

- [ ] More threads (`content/concepts/`): variational principles beyond mechanics, linearity & superposition,
  geometry/curvature (GR ↔ gauge ↔ Berry phase), randomness & typicality, Hamiltonian vs Lagrangian in depth,
  "why mathematics fits physics".
- [ ] Original-paper links exist for ~120 milestones; extend to the remaining key results (verify each id via API).
- [ ] `definitions:` sections exist for chaos, non-equilibrium (thermalization), quantum gravity, integrability,
  complex systems, QFT, topological order; candidates: emergence, entropy (Boltzmann vs Gibbs), renormalization schemes.
- [x] Publish the `.apkg` as a GitHub Release on each push (now only a workflow artifact) so Anki users can
  download it from a stable URL.
- [ ] Scheduled job that syncs the D1 feedback into the repo (as in eating-amsterdam) instead of reading it by hand (now an idea of the shared `site-notes` repo).
- [x] Map: optional "threads only" view that highlights the fields a selected thread passes through.
- [ ] Site note #7 (2026-10-05): use review papers as references for each field, e.g. the Snowmass 2021
  reports for high-energy physics (verify ids via the arXiv API, as for the original-paper links).
- [ ] Site note #9 (2026-10-06): hydrodynamics with higher-form symmetries (MHD as the hydrodynamics of a
  1-form symmetry, Grozdanov–Hofman–Iqbal) and anomalous hydrodynamics (ABJ / chiral magnetic effect), with
  which experiments support it; check whether it has been done beyond 1-form symmetries.

## Decisioni e cose provate

- 2026-10-21 (link ai paper): saltati perché non verificati o con anno discordante: Hewish et al. (pulsar, pubblicato 1968 contro 1967 nella tappa), Wilson 1971 parte II (esponenti RG), Gopikrishnan et al. (autore/titolo ambigui).

### Done / history

- 2026-10-19: `.apkg` pubblicato a ogni push su main come release "rolling" con tag fisso `latest-deck` (asset sostituito con
  `--clobber`, tag spostato al commit costruito), così il link `releases/download/latest-deck/big-picture.apkg` è stabile.
  Scelto al posto di una release per push (accumulerebbe centinaia di release) e di azioni di terze parti (si usa solo `gh`,
  già sul runner). Job `release` separato, `contents: write` solo lì; gira solo su `main` (mai su pull request); il workflow
  non committa `docs/`, e comunque i push fatti con `GITHUB_TOKEN` non rilanciano i workflow, quindi nessun ciclo.

- 2026-10-05 (2): feedback #6 (anomaly taxonomy); Anki deck rebuilt around context (big goal, essentials,
  broken promises, place on the map) — 454 notes instead of 624 technical ones.
- 2026-10-05: site feedback #2–#5 handled — light/dark toggle, original-paper links, `definitions:` sections,
  stability thread; added supersymmetry, soft & active matter, optics, geophysics & climate, statistics, TQFT.
- 2026-10: project created by Cowork in `big-picture/big-picture/`; moved to repo root, ODE/SDE, philosophy
  of physics/mathematics, concept threads, feedback Worker, content review, public GitHub Pages site.

## Log
- 2026-10-31: 🤖 quinto lotto: 18 link a paper originali verificati (Crossref/arXiv, titolo-autore-anno controllati) su 14 tappe; saltati Young 1802 e Tyndall 1861 (DOI Crossref non corrispondente); nuovo filo concettuale "Scaling and dimensional analysis" (Buckingham, Reynolds, Taylor, Kleiber/West, Mandelbrot, Wilson; 7 link verificati su Crossref, Kolmogorov 1941 senza link); sesto lotto: 30 link a paper originali verificati (Crossref/arXiv, titolo-autore-anno controllati) su 27 tappe di fisica e matematica; nuovo filo concettuale "Randomness and probability" (8 link verificati su Crossref: Einstein 1905, Born 1926, Jaynes 1957, Cox 1946, Lorenz 1963, Bohigas et al. 1984, Touchette 2009, Deutsch 1991; Perrin e Birkhoff senza link); settimo lotto: 29 link a paper originali verificati (Crossref/arXiv, titolo-autore-anno controllati) su 20 tappe di fisica; Hubble senza Lemaître 1927 (nessun DOI verificato); ottavo lotto: 20 link a paper originali verificati (Crossref/arXiv) su 9 voci tra esperimenti e tappe; Wiles, Perelman e Christenson già presenti, Mercury/Einstein 1915 senza DOI
- 2026-10-24: 🤖 20 link a paper originali verificati (Crossref/arXiv), quarto lotto; saltati Turing 1936 (Crossref: 1937), Wilson–Kogut e altri riferimenti ambigui
- 2026-10-23: 🤖 nuovo filo concettuale "Geometry and curvature" (GR ↔ gauge ↔ fase di Berry); poi nuovo filo "Fluctuations and response" (Einstein, Johnson–Nyquist, Callen–Welton, Kubo, Onsager; 7 link a paper verificati su Crossref)
- 2026-10-22: 🤖 terzo lotto: 25 link a paper originali verificati (Crossref/arXiv, titolo-autori-anno controllati) su 19 tappe (geometria algebrica, teoria dei numeri, PDE, TQFT, ottica, SUSY, stringhe, reticolo, integrabilità); saltati AKS (arXiv assente, 2004 vs 2002), Bell Burnell–Hewish (1968 vs 1967), Hopfield, Kolmogorov 1941, Landau 1946 (senza DOI/preprint verificabile)
- 2026-10-22: 🤖 19 link a paper originali verificati (Crossref/arXiv, titolo-autori-anno controllati) su 19 tappe (anomalie, SUSY, stringhe, TQFT, reti, metodi numerici, materia attiva); saltati Hafele–Keating (1972 vs 1971 nella tappa) e Pestun (2012 su rivista vs 2007)
- 2026-10-21: 🤖 24 link a paper originali verificati via API arXiv/Crossref su 21 tappe di fisica (CFT, complessità, EFT, biofisica, fondamenti quantistici, reti, geofisica)
- 2026-10-21: 🤖 nuovo filo concettuale "Variational principles"
- 2026-10-20: 🤖 nuovo filo concettuale "Linearity and superposition" (dove la linearità vale, dove si rompe, avvertenze)
- 2026-10-18: 🤖 mappa: menu "Thread" che evidenzia il filo scelto e i campi a cui rimanda (`connections`), sfumando il resto
- 2026-10-19: note del sito portate nel ROADMAP (#7 e #9 nelle Idee; #8, TLC generalizzato, era già in `probability-theory`); feedback spostato nel backend unico `site-notes` (tolto `worker/`; vecchio worker `conceptual-map-feedback` e D1 spenti); le note mandano l'autore (`?sono-alessio` segna il browser di Alessio, le altre sono di visitatori); installabile come app a sé dal telefono (manifest con nome, icona e perimetro propri); il `.apkg` viene pubblicato a ogni push su main nella release `latest-deck` (link stabile nel README)
- 2026-10-18: FUTURE-ARCHITECTURE.md unito in ROADMAP.md (protocollo unico)
- 2026-10-15: creata la roadmap per Projects Overview
