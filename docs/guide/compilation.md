# Compilation

Tinyleaf supports two compilation backends: **local** and **Docker** (default).

## Docker Compilation (Default)

Uses a Docker container with a full TeX Live installation:

```bash
tinyleaf /path/to/project
```

The default Docker image is `oaklight/texlive:alpine-science-cn`. You can specify a different image:

```bash
tinyleaf /path/to/project --image oaklight/texlive:alpine-science
```

!!! note "Auto-pull"
    If the Docker image is not available locally, tinyleaf will automatically pull it on the first compile. A registry mirror can be configured in settings for faster downloads.

## Local Compilation

Uses `latexmk` installed on the host system:

```bash
tinyleaf /path/to/project --no-docker
```

!!! note "Prerequisite"
    A TeX Live distribution with `latexmk` must be installed locally.

## Per-Project Configuration

Each project can have a `.tinyleaf.json` file to configure:

```json
{
  "main_file": "thesis.tex",
  "engine": "lualatex",
  "docker_image": "oaklight/texlive:alpine-science-cn"
}
```

| Field | Default | Description |
|-------|---------|-------------|
| `main_file` | Auto-detected | The `.tex` file containing `\documentclass` |
| `engine` | `pdflatex` | LaTeX engine: `pdflatex`, `lualatex`, `xelatex` |
| `docker_image` | Server default | Override Docker image for this project |

## Auto-Detection

If `main_file` is not configured, tinyleaf scans for `.tex` files containing `\documentclass`. If exactly one is found, it is used. If multiple candidates exist, `main.tex` is preferred. You can also select the main file from the dropdown in the toolbar.

## Compilation Log

Compilation output is streamed in real-time via SSE (Server-Sent Events) to the browser log panel. The log panel includes a copy button for easy sharing of error messages.

## Cancellation

You can cancel a running compilation from the toolbar. This also works for Docker image pulls.
