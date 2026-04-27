# Installation

## From PyPI

```bash
pip install tinyleaf
```

## From Source

```bash
git clone https://github.com/Oaklight/tinyleaf.git
cd tinyleaf
pip install -e .
```

## Requirements

- Python 3.10+
- No additional Python dependencies (stdlib only)

### Optional

- **Docker** — for Docker-based compilation (enabled by default)
- **latexmk** — for local compilation (`--no-docker` flag)
- A TeX Live distribution if compiling locally

### Development Dependencies

```bash
pip install tinyleaf[dev]
```

Includes `ruff`, `ty`, `complexipy`, `build`, and `twine`.
