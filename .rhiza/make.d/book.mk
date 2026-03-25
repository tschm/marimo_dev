## book.mk - Book-building targets (MkDocs-based)
# This file is included by the main Makefile.
# It builds the companion book using MkDocs with mkdocstrings + mkdocs-jupyter.

.PHONY: marimushka mkdocs-build book test benchmark stress hypothesis-test

# Define default no-op targets for test-related book dependencies.
# These are used when test.mk is not available or tests are not installed,
# ensuring 'make book' succeeds even without a test environment.
test:: ; @:
benchmark:: ; @:
stress:: ; @:
hypothesis-test:: ; @:

# Default output directory for Marimushka (HTML exports of notebooks)
MARIMUSHKA_OUTPUT ?= _marimushka

# Keep marimushka for backwards compatibility (no longer a book dependency)
marimushka:: install-uv
	@if [ ! -d "book/marimo" ]; then \
	  printf "${BLUE}[INFO] No Marimo directory found, skipping marimushka${RESET}\n"; \
	fi

# Define a default no-op mkdocs-build target that will be used
# when .rhiza/make.d/docs.mk doesn't exist or doesn't define mkdocs-build
mkdocs-build:: install-uv
	@if [ ! -f "mkdocs.yml" ]; then \
	  printf "${BLUE}[INFO] No mkdocs.yml found, skipping MkDocs${RESET}\n"; \
	fi

# Default output directory for the book
BOOK_OUTPUT ?= _book

# MkDocs config file location
MKDOCS_CONFIG ?= mkdocs.yml

##@ Book

# The 'book' target assembles the final documentation book using MkDocs.
# 1. Runs test/benchmark/stress/hypothesis-test to generate HTML artefacts.
# 2. Copies generated HTML artefact directories into docs/reports/ (if they exist).
# 3. Copies Marimo notebooks into docs/notebooks/ for mkdocs-jupyter rendering.
# 4. Runs mkdocs build to produce the final site in _book/.
book:: test benchmark stress hypothesis-test ## compile the companion book via MkDocs
	@printf "${BLUE}[INFO] Copying test artefacts into docs/reports/...${RESET}\n"
	@mkdir -p docs/reports
	@for src_dir in \
	  "_tests/html-coverage:reports/coverage" \
	  "_tests/html-report:reports/test-report" \
	  "_tests/benchmarks:reports/benchmarks" \
	  "_tests/stress:reports/stress" \
	  "_tests/hypothesis:reports/hypothesis"; do \
	  src=$${src_dir%%:*}; dest=docs/$${src_dir#*:}; \
	  if [ -d "$$src" ]; then \
	    printf "${BLUE}[INFO] Copying $$src -> $$dest${RESET}\n"; \
	    mkdir -p "$$dest"; \
	    cp -r "$$src/." "$$dest/"; \
	  else \
	    printf "${YELLOW}[WARN] $$src not found, skipping${RESET}\n"; \
	  fi; \
	done
	@if [ -d "book/marimo" ]; then \
	  printf "${BLUE}[INFO] Copying Marimo notebooks into docs/notebooks/...${RESET}\n"; \
	  mkdir -p docs/notebooks; \
	  cp -r book/marimo/. docs/notebooks/; \
	fi
	@$(MAKE) mkdocs-build MKDOCS_OUTPUT=$(BOOK_OUTPUT)
	@touch "$(BOOK_OUTPUT)/.nojekyll"
	@printf "${GREEN}[SUCCESS] Book built at $(BOOK_OUTPUT)/${RESET}\n"
