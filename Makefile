.PHONY: install
install: Pipfile
	pipenv install

.PHONY: run-script
run-script: install
	pipenv run python3 ./scripts/$(SCRIPT)
