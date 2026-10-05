PY ?= python3

.PHONY: all check site anki serve

all: check site anki

check:
	cd scripts && $(PY) -c "from common import load_all; e,_ = load_all(); print(f'OK: {len(e)} entries')"

site:
	cd scripts && $(PY) build_site.py

anki:
	cd scripts && $(PY) build_anki.py

serve: site
	$(PY) -m http.server -d docs 8000
