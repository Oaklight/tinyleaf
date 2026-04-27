IMAGE_NAME = oaklight/texlive-web
REGISTRY_MIRROR ?= docker.io

BUILD_ARGS = --build-arg REGISTRY_MIRROR=$(REGISTRY_MIRROR)

.PHONY: all install dev build-docker push-docker clean test help

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

help:
	@echo "Available targets:"
	@echo "  install       - Install package"
	@echo "  dev           - Install in development mode"
	@echo "  build-docker  - Build Docker image"
	@echo "  push-docker   - Push Docker image"
	@echo "  clean         - Remove build artifacts"
	@echo "  test          - Run tests"
	@echo ""
	@echo "Variables:"
	@echo "  REGISTRY_MIRROR=<host> - Docker registry mirror (default: docker.io)"
