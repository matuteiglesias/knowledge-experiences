.PHONY: check seed-check census-check test doctor example producer-receipt-build clean

PROJECTS_ROOT ?=

producer-receipt-build:
	@test -n "$(PROJECTS_ROOT)" || { echo "PROJECTS_ROOT is required" >&2; exit 2; }
	python3 "$(PROJECTS_ROOT)/scripts/producer_local_receipt.py" --producer producer.manual.knowledge-experience-composer --cwd "$(CURDIR)" --evidence-changed "$(OUT)/experience.release.json" --evidence-json "$(OUT)/experience.release.json#/schema_id=knowledge.experience-release" --enforce-evidence -- env PYTHONPATH=src $(PYTHON) -m knowledge_experiences.cli build "$(SPEC)" --out "$(OUT)"

SPEC ?= examples/fixture/demo.experience.json
OUT ?= dist/example

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
