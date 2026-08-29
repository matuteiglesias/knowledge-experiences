.PHONY: check seed-check census-check test doctor example clean

PYTHON ?= python3
PYTHONPATH_ENV := PYTHONPATH=src

check: seed-check census-check test doctor

seed-check:
	$(PYTHON) scripts/check_seed.py

census-check:
	$(PYTHON) scripts/check_census.py

test:
	$(PYTHONPATH_ENV) $(PYTHON) -m unittest discover -s tests -v

doctor:
	$(PYTHONPATH_ENV) $(PYTHON) -m knowledge_experiences.cli doctor examples/fixture/demo.experience.json

example:
	rm -rf dist/example
	$(PYTHONPATH_ENV) $(PYTHON) -m knowledge_experiences.cli build examples/fixture/demo.experience.json --out dist/example
	@echo "Open dist/example/site/index.html"

clean:
	rm -rf dist .pytest_cache .mypy_cache
