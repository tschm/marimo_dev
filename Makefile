# Colors for pretty output
BLUE := \033[36m
BOLD := \033[1m
RESET := \033[0m

.DEFAULT_GOAL := help

.PHONY: help fmt marimo clean test

##@ Development Setup

uv:
	@printf "$(BLUE)Install uv...$(RESET)\n"
	@curl -LsSf https://astral.sh/uv/install.sh | sh

##@ Code Quality

fmt: uv ## Run code formatting and linting
	@printf "$(BLUE)Running formatters and linters...$(RESET)\n"
	@uvx pre-commit run --all-files

##@ Cleanup

clean: ## Clean generated files and directories
	@printf "$(BLUE)Cleaning project...$(RESET)\n"
	@git clean -d -X -f

##@ Marimo

marimo: uv ## Start a Marimo server
	@printf "$(BLUE)Start Marimo server...$(RESET)\n"
	@uvx marimo edit --host=localhost --port=8080 --headless --no-token --sandbox notebooks/minimal_enclosing_circle.py

##@ Help

help: ## Display this help message
	@printf "$(BOLD)Usage:$(RESET)\n"
	@printf "  make $(BLUE)<target>$(RESET)\n\n"
	@printf "$(BOLD)Targets:$(RESET)\n"
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  $(BLUE)%-15s$(RESET) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BOLD)%s$(RESET)\n", substr($$0, 5) }' $(MAKEFILE_LIST)
