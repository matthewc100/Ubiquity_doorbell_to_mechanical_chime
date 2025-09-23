.PHONY: venv run test readme-links

venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	. .venv/bin/activate && waitress-serve --host 0.0.0.0 --port 8080 app:app

test:
	curl -X POST http://127.0.0.1:8080/test

readme-links:
	python3 scripts/update_readme_links.py
