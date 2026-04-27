# tinyleaf

[English Version](./README.md)

基于 [TeX Live Docker 镜像](https://github.com/Oaklight/texlive) 的轻量 Web LaTeX 编辑器。

## 功能

* **CLI 优先** — `pip install tinyleaf && tinyleaf /path` 即可开始编辑
* **两种模式** — 单项目或多项目（类 Overleaf）
* **两种编译后端** — 本地 `latexmk`（默认）或 Docker
* **CodeMirror 6** 编辑器 + LaTeX 语法高亮
* **PDF.js** 预览，编译后自动刷新
* **SSE** 实时编译日志推送
* **Git 集成** — 自动发现 `.git`，支持 UI 内 commit/push
* **零 Python 依赖** — 仅使用标准库（`http.server` + `threading` + `subprocess`）
* **暗色/亮色主题** 切换

## 快速开始

```bash
pip install tinyleaf

# 单项目模式（本地编译）
tinyleaf /path/to/my-thesis

# 单项目模式（Docker 编译）
tinyleaf /path/to/my-thesis --docker

# 多项目模式
tinyleaf --projects-dir /path/to/projects
```

## 使用方法

```
用法: tinyleaf [-h] [--projects-dir DIR] [--docker] [--image IMAGE]
                  [--port PORT] [--host HOST] [--no-browser] [project_path]

位置参数:
  project_path          要打开的单项目目录

选项:
  --projects-dir DIR    多项目模式：包含项目文件夹的目录
  --docker              使用 Docker 编译（默认：本地 latexmk）
  --image IMAGE         Docker 镜像（默认：oaklight/texlive:latest）
  --port PORT           服务端口（默认：8080）
  --host HOST           服务地址（默认：127.0.0.1）
  --no-browser          启动时不自动打开浏览器
```

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

Web 编辑器将在 `http://localhost:8080` 启动，并使用持久化的 TeX Live 容器进行编译。

## 许可证

MIT
