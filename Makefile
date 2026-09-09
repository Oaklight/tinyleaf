IMAGE_NAME = oaklight/tinyleaf
REGISTRY_MIRROR ?= docker.io
VERSION := $(shell grep -oP '__version__\s*=\s*"\K[^"]+' src/tinyleaf/__init__.py)

BUILD_ARGS = --build-arg REGISTRY_MIRROR=$(REGISTRY_MIRROR)

.PHONY: all install dev build-docker push-docker clean test help \
	build-binary build-binary-musl clean-binary clean-binary-all

all: install

install:
	pip install .

dev:
	pip install -e .

build-docker:
	docker build $(BUILD_ARGS) -t $(IMAGE_NAME):latest .

push-docker:
	docker push $(IMAGE_NAME):latest

clean:
	rm -rf build/ dist/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

test:
	python -m pytest tests/ -v

# ──────────────────────────────────────────────
# Nuitka binary builds
# ──────────────────────────────────────────────

# Detect platform
UNAME_S := $(shell uname -s 2>/dev/null || echo Windows)
UNAME_M := $(shell uname -m 2>/dev/null || echo x86_64)
ifeq ($(UNAME_S),Linux)
  BINARY_OS := linux
else ifeq ($(UNAME_S),Darwin)
  BINARY_OS := macos
else
  BINARY_OS := windows
endif
ifeq ($(UNAME_M),aarch64)
  BINARY_ARCH := arm64
else ifeq ($(UNAME_M),arm64)
  BINARY_ARCH := arm64
else
  BINARY_ARCH := x86_64
endif

BINARY_NAME = tinyleaf-$(VERSION)-$(BINARY_OS)-$(BINARY_ARCH)
BINARY_NAME_MUSL = tinyleaf-$(VERSION)-linux-$(BINARY_ARCH)-musl
BINARY_DIR := build
NUITKA_ENTRY := _nuitka_entry.py
NUITKA_JOBS := $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 2)
NUITKA_EXTRA_FLAGS ?=

# Modules excluded from binary — standard bloat that tinyleaf never imports.
# Do NOT add concurrent (asyncio imports it) or multiprocessing (Nuitka
# plugin conflict).
NUITKA_NOFOLLOW := \
	pytest setuptools pip _pytest \
	tkinter unittest pydoc doctest test \
	distutils ensurepip idlelib lib2to3 \
	turtle turtledemo xmlrpc curses

NUITKA_NOFOLLOW_FLAGS := $(foreach m,$(NUITKA_NOFOLLOW),--nofollow-import-to=$m)

NUITKA_FLAGS = \
	--standalone \
	--onefile \
	--jobs=$(NUITKA_JOBS) \
	--output-dir=$(BINARY_DIR) \
	--lto=yes \
	--python-flag=no_docstrings \
	--python-flag=-O \
	--python-flag=no_warnings \
	--include-package=tinyleaf \
	--include-data-files=src/tinyleaf/static/index.html=tinyleaf/static/index.html \
	--include-data-dir=src/tinyleaf/static/css=tinyleaf/static/css \
	--include-data-dir=src/tinyleaf/static/js=tinyleaf/static/js \
	--include-data-dir=src/tinyleaf/static/assets=tinyleaf/static/assets \
	$(NUITKA_NOFOLLOW_FLAGS) \
	--assume-yes-for-downloads \
	$(NUITKA_EXTRA_FLAGS)

# Build native binary (glibc on Linux, system libc on macOS)
build-binary:
	@echo "Building native binary: $(BINARY_NAME)..."
	@printf 'from tinyleaf.cli import main\nmain()\n' > $(NUITKA_ENTRY)
	python -m nuitka $(NUITKA_FLAGS) \
		--output-filename=$(BINARY_NAME)$(if $(filter windows,$(BINARY_OS)),.exe,) \
		$(NUITKA_ENTRY); \
	ret=$$?; rm -f $(NUITKA_ENTRY); exit $$ret
	@ls -lh $(BINARY_DIR)/$(BINARY_NAME)*
	@echo "Binary build complete."

# Build musl-linked binary via Alpine Docker container (Linux only)
build-binary-musl:
	@echo "Building musl binary: $(BINARY_NAME_MUSL)..."
	@mkdir -p $(BINARY_DIR)
	docker run --rm \
		-v $(CURDIR):/workspace:ro \
		-v $(CURDIR)/$(BINARY_DIR):/output \
		$(REGISTRY_MIRROR:%=%/)python:3.12-alpine \
		/bin/sh -c '\
			mkdir -p /tmp/build && tar -cf - -C /workspace --exclude=.git --exclude=__pycache__ . | tar -xf - -C /tmp/build && cd /tmp/build && \
			apk add --no-cache gcc musl-dev python3-dev git >/dev/null && \
			pip install --break-system-packages patchelf -q && \
			pip install --break-system-packages -e "." -q && \
			pip install --break-system-packages "nuitka[onefile]" ordered-set -q && \
			printf "from tinyleaf.cli import main\nmain()\n" > /tmp/_entry.py && \
			python -m nuitka \
				--standalone --onefile \
				--jobs=$$(nproc) \
				--output-dir=/output \
				--output-filename=$(BINARY_NAME_MUSL) \
				--lto=yes \
				--python-flag=no_docstrings \
				--python-flag=-O \
				--python-flag=no_warnings \
				--include-package=tinyleaf \
				--include-data-files=src/tinyleaf/static/index.html=tinyleaf/static/index.html \
				--include-data-dir=src/tinyleaf/static/css=tinyleaf/static/css \
				--include-data-dir=src/tinyleaf/static/js=tinyleaf/static/js \
				--include-data-dir=src/tinyleaf/static/assets=tinyleaf/static/assets \
				$(NUITKA_NOFOLLOW_FLAGS) \
				--assume-yes-for-downloads \
				$(NUITKA_EXTRA_FLAGS) \
				/tmp/_entry.py && \
			rm -rf /output/_entry.* '
	@ls -lh $(BINARY_DIR)/$(BINARY_NAME_MUSL)
	@echo "Musl binary build complete."

clean-binary:
	@echo "Cleaning binary build artifacts..."
	rm -rf $(BINARY_DIR)/_nuitka_entry.* $(BINARY_DIR)/_entry.* $(NUITKA_ENTRY)
	@echo "Clean complete. Binaries in $(BINARY_DIR)/ preserved."

clean-binary-all:
	@echo "Cleaning all binary artifacts..."
	rm -rf $(BINARY_DIR)
	rm -f $(NUITKA_ENTRY)
	@echo "Clean complete."

help:
	@echo "Available targets:"
	@echo "  install          - Install package"
	@echo "  dev              - Install in development mode"
	@echo "  build-docker     - Build Docker image"
	@echo "  push-docker      - Push Docker image"
	@echo "  clean            - Remove build artifacts"
	@echo "  test             - Run tests"
	@echo ""
	@echo "Binary:"
	@echo "  build-binary     - Build native Nuitka binary"
	@echo "  build-binary-musl- Build musl-linked binary (Docker)"
	@echo "  clean-binary     - Clean build artifacts (keep binaries)"
	@echo "  clean-binary-all - Clean all binary artifacts"
	@echo ""
	@echo "Variables:"
	@echo "  REGISTRY_MIRROR=<host>  - Docker registry mirror (default: docker.io)"
	@echo "  NUITKA_EXTRA_FLAGS=...  - Extra Nuitka flags for experimentation"
