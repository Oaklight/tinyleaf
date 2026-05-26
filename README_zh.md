# tinyleaf

<p align="center">
  <img src="assets/brand/tinyleaf-leafpen-readme-light.svg" alt="Tinyleaf" width="560">
</p>

[![PyPI version](https://img.shields.io/pypi/v/tinyleaf?color=green)](https://pypi.org/project/tinyleaf/)
[![GitHub release](https://img.shields.io/github/v/release/Oaklight/tinyleaf?color=green)](https://github.com/Oaklight/tinyleaf/releases/latest)
[![CI](https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml/badge.svg)](https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-blue)](https://tinyleaf.readthedocs.io)

[English Version](./README.md) | [文档](https://tinyleaf.readthedocs.io)

轻量级、可自托管的 **Overleaf 替代方案**，只需一条 `pip install` 即可运行。无需数据库、无需 Node.js、无需 Docker——仅依赖 Python 标准库和 TeX Live。一条命令即可在浏览器中编辑 LaTeX。

```bash
pip install tinyleaf && tinyleaf /path/to/my-thesis
```

<!-- 截图 / 演示 GIF 占位 — 替换为实际素材 -->
<!-- ![tinyleaf 截图](docs/images/screenshot.png) -->

## 功能

* **CLI 优先** — `pip install tinyleaf && tinyleaf /path` 即可开始编辑
* **两种模式** — 单项目或基于注册表的多项目模式（`~/.config/tinyleaf/projects.json`）
* **两种编译后端** — 本地 `latexmk`（默认）或 Docker
* **CodeMirror 6** 编辑器 + LaTeX 语法高亮
* **PDF.js** 预览，编译后自动刷新
* **SSE** 实时编译日志推送
* **Git 集成** — 自动发现 `.git`，支持 UI 内 commit/push
* **零 Python 依赖** — 仅使用标准库（`http.server` + `threading` + `subprocess`）
* **7 套主题**，支持明暗切换
* **国际化** — 中英双语

## 快速开始

```bash
pip install tinyleaf

# 单项目模式（本地编译）
tinyleaf /path/to/my-thesis

# 单项目模式（Docker 编译）
tinyleaf /path/to/my-thesis --docker

# 多项目模式（注册表）
tinyleaf
```

## 使用方法

```
用法: tinyleaf [-h] [--projects-dir DIR] [--config-dir DIR] [--docker]
               [--image IMAGE] [--port PORT] [--host HOST] [--no-browser]
               [project_path]

位置参数:
  project_path          要打开的单项目目录

选项:
  --config-dir DIR      项目注册表的配置目录
                        （默认：~/.config/tinyleaf）
  --projects-dir DIR    旧版：将子目录迁移到注册表
  --docker              使用 Docker 编译（默认：本地 latexmk）
  --image IMAGE         Docker 镜像（默认：oaklight/texlive:latest）
  --port PORT           服务端口（默认：14159，环境变量：TINYLEAF_PORT）
  --host HOST           服务地址（默认：127.0.0.1）
  --no-browser          启动时不自动打开浏览器
```

## 多项目注册表

不带 `project_path` 参数启动时，tinyleaf 进入**多项目模式**。项目在 `~/.config/tinyleaf/projects.json` 中跟踪——每个条目将名称映射到文件系统上的绝对路径。

在项目页面你可以：

- **打开文件夹** — 浏览服务器文件系统，注册已有目录
- **新建项目** — 在指定位置创建新项目
- **移除** — 取消注册项目（可选择同时删除文件）

## 快捷键

| 快捷键 | 操作 |
|--------|------|
| `Ctrl+S` | 保存当前文件 |
| `Ctrl+Enter` | 编译 |
| `Ctrl+Shift+C` | Git 提交 |
| `Ctrl+Shift+P` | Git 推送 |

## Docker Compose

使用 Docker Compose 一键部署：

```bash
docker compose up
```

Web 编辑器将在 `http://localhost:14159` 启动，并使用持久化的 TeX Live 容器进行编译。

## 为什么选择 tinyleaf？

| | tinyleaf | Overleaf CE |
|---|---------|-------------|
| 安装 | `pip install tinyleaf` | Docker Compose（MongoDB + Redis + Node + CLSI + …） |
| 依赖 | **零**（仅 Python 标准库） | 6+ 个服务 |
| 内存占用 | ~30 MB | ~1 GB+ |
| 启动速度 | 即时 | 数分钟 |
| 编译方式 | 本地 `latexmk` 或 Docker | 内置 CLSI |
| Git 集成 | 内置 UI | 服务端 Git Bridge |
| 协作 | 单用户 | 多用户 |

tinyleaf 专为**个人用户**设计，提供浏览器内的 LaTeX 编辑体验，无需承担完整 Overleaf 部署的运维开销。

## 许可证

AGPL-3.0-or-later
