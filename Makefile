# =============================================================================
# GPCICD PPE Detection — automatización de tareas
# =============================================================================

SHELL := /bin/bash

# En Windows, GNU Make debe usar Git Bash para disponer de grep/awk/rm/find.
ifeq ($(OS),Windows_NT)
SHELL := C:/PROGRA~1/Git/bin/bash.exe
endif

.DEFAULT_GOAL := help
.PHONY: help install dev pre-commit-install pre-commit lint format format-check typecheck test check build estado arch clean

# Ruta al CLI de Archify (skill instalado). Sobrescribe con ARCHIFY_BIN=...
ifeq ($(OS),Windows_NT)
ARCHIFY_BIN ?= $(shell cygpath -m "$(USERPROFILE)")/.agents/skills/archify/bin/archify.mjs
else
ARCHIFY_BIN ?= $(HOME)/.agents/skills/archify/bin/archify.mjs
endif

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Sincroniza el entorno virtual e instala dependencias
	uv sync

dev: install pre-commit-install ## Prepara el entorno de desarrollo (sync + hooks)

pre-commit-install: ## Instala los hooks de pre-commit en el repositorio local
	uv run pre-commit install

pre-commit: ## Ejecuta todos los hooks de pre-commit sobre el repositorio
	uv run pre-commit run --all-files

lint: ## Ejecuta Ruff (lint)
	uv run ruff check .

format: ## Formatea el código con Ruff
	uv run ruff format .

format-check: ## Verifica el formato sin modificarlo
	uv run ruff format --check .

typecheck: ## Verifica los tipos con ty (Astral)
	uv run ty check

test: ## Ejecuta las pruebas
	uv run pytest

check: lint format-check typecheck test ## Verificación completa (lint + formato + tipos + pruebas)

build: ## Construye el paquete (sdist + wheel)
	uv build

estado: ## Muestra el estado operativo (git, PRs, issues); usa ARGS=--write para guardarlo
	uv run python -m ppe_detection.tools.estado $(ARGS)

arch: ## Regenera el diagrama de arquitectura con Archify
	node "$(ARCHIFY_BIN)" finalize architecture docs/architecture/arquitectura.json docs/architecture/arquitectura.html --quality showcase

clean: ## Limpia cachés y artefactos
	rm -rf .pytest_cache .ruff_cache .mypy_cache dist build htmlcov .coverage
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
