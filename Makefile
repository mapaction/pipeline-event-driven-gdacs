.PHONY: all
all = help

.venv:
	@echo "Installing project dependencies.."
	@poetry install --no-root


hooks:
	@echo "Adding pre-commit hooks.."
	@poetry run pre-commit install
	

test:
	@echo "Running unit tests.."
	@poetry run python -m pytest

lint:
	@echo "Running lint tests.."
	@poetry run pre-commit run --all-files

clean:
	@echo "Removing .venv"
	@rm -rf .venv
	@poetry env remove --all

database:
	@echo "Creating database.."
	@poetry run python util/util.py

gdacs_reader:
	@echo "Running gdacs reader.."
	@poetry run python src/data_retrieval/retriever.py

lab:
	@echo "Running jupyter lab.."
	@poetry run jupyter lab

monitor:
	@echo "Running monitor.."
	@poetry run python src/monitor/monitor.py

help:
	@echo "Available make targets:"
	@echo " make help           - Print help"
	@echo " make .venv          - Install project dependencies"
	@echo " make hooks          - Add pre-commit hooks"
	@echo " make test           - Run unit tests"
	@echo " make lint           - Run lint tests"
	@echo " make clean          - Remove .venv"
	@echo " make database       - Create database"
	@echo " make gdacs_reader   - Run gdacs reader"
	@echo " make lab            - Run jupyter lab"