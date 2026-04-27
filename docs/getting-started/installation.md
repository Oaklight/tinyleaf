# 安装

## 从 PyPI 安装

```bash
pip install tinyleaf
```

## 从源码安装

```bash
git clone https://github.com/Oaklight/tinyleaf.git
cd tinyleaf
pip install -e .
```

## 环境要求

- Python 3.10+
- 无额外 Python 依赖（仅标准库）

### 可选依赖

- **Docker** — 用于 Docker 编译模式（默认启用）
- **latexmk** — 用于本地编译（`--no-docker` 参数）
- 本地编译需要安装 TeX Live 发行版

### 开发依赖

```bash
pip install tinyleaf[dev]
```

包含 `ruff`、`ty`、`complexipy`、`build` 和 `twine`。
