# tinyleaf

<p align="center">
  <img src="assets/brand/tinyleaf-leafpen-readme-light.svg" alt="Tinyleaf" width="560">
</p>

[![PyPI version](https://img.shields.io/pypi/v/tinyleaf?color=green)](https://pypi.org/project/tinyleaf/)
[![GitHub release](https://img.shields.io/github/v/release/Oaklight/tinyleaf?color=green)](https://github.com/Oaklight/tinyleaf/releases/latest)
[![CI](https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml/badge.svg)](https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-blue)](https://tinyleaf.readthedocs.io)

[English Version](./README.md) | [文档](https://tinyleaf.readthedocs.io) | [品牌资产](./BRAND.md)

**Tinyleaf 是一个 tiny、local-first 的 TeX Web 编辑器。**

它面向想要 Overleaf 式浏览器编辑体验、但不想部署完整 Overleaf 服务栈的用户。安装一个 Python 包，指向一个 LaTeX 项目目录，就可以在浏览器里编辑、预览 PDF、查看编译日志、使用 Git、搜索、查看大纲和多标签编辑。

```bash
pip install tinyleaf

# 打开单个项目。默认使用 Docker 中的 TeX Live 编译。
tinyleaf /path/to/my-thesis

# 或者使用本机 TeX / latexmk。
tinyleaf /path/to/my-thesis --no-docker

# 启动项目注册表。
tinyleaf
```

## 为什么是 Tinyleaf？

Tinyleaf 位于本地编辑器和完整协作 LaTeX 平台之间：

- **Local-first** — 项目文件保留在你的文件系统中
- **可自托管** — 可运行在笔记本、工作站、实验室服务器或 VPS 上
- **运行时很小** — 无需数据库、Node.js 服务、Redis 或 MongoDB
- **浏览器界面** — CodeMirror 编辑器、PDF 预览、文件树、Git 面板和设置界面
- **编译方式灵活** — 默认使用 Docker 化 TeX Live，也可用 `--no-docker` 调用本机 `latexmk`
- **单用户优先** — 面向个人写作工作流，而不是完整多人 SaaS 克隆

## 功能

### 编辑

- CodeMirror 6 编辑器和 LaTeX 语法高亮
- 多标签编辑和快速打开（`Ctrl+P`）
- 自动配对 `\begin{...}` / `\end{...}`
- 项目级全文搜索
- LaTeX 大纲侧边栏，支持递归解析 `\input` / `\include`
- 从项目符号中补全 `\ref{}`、`\cite{}` 和 `\label{}`

### PDF 与编译

- PDF.js 预览，编译后自动刷新
- 页码导航、缩放控制和 PDF 文本搜索
- 基于 SSE 的实时编译日志
- 编译输出中的 `file.tex:line` 可点击跳转
- SyncTeX 正向/反向搜索
- 基于 `texcount` 的字数/页数统计
- 导出项目为 ZIP

### 项目与工作流

- 单项目模式：直接打开任意目录
- 多项目注册表：存储在 `~/.config/tinyleaf/projects.json`
- 文件树：新建、上传、重命名、删除和搜索
- Git 状态、差异、提交、推送、拉取和日志
- 7 套主题，支持明暗模式
- 中英文界面

## 安装

```bash
pip install tinyleaf
```

Tinyleaf **没有额外 Python 运行时依赖**，仅使用标准库。Web 编辑器资源随包一起分发。

编译后端可二选一：

| 后端 | 命令 | 要求 |
|---|---|---|
| Docker TeX Live | `tinyleaf /path/to/project` | 已安装 Docker |
| 本机 TeX Live | `tinyleaf /path/to/project --no-docker` | `PATH` 中可用 `latexmk` |

## 使用方法

```text
usage: tinyleaf [-h] [-V] [--projects-dir DIR] [--config-dir DIR]
                [--docker | --no-docker] [--image IMAGE] [--port PORT]
                [--host HOST] [--no-browser]
                [project_path]
```

常见示例：

```bash
# 打开项目并使用 Docker 编译。
tinyleaf ~/papers/my-paper

# 使用本机 latexmk，而不是 Docker。
tinyleaf ~/papers/my-paper --no-docker

# 在服务器上监听所有网卡。
tinyleaf ~/papers/my-paper --host 0.0.0.0 --port 14159

# 打开多项目注册表。
tinyleaf
```

## 多项目注册表

不传 `project_path` 时，Tinyleaf 会打开项目注册表。注册表将项目名称映射到文件系统任意位置的绝对路径。

在项目页面你可以：

- **打开文件夹** — 注册已有目录
- **新建项目** — 在指定位置创建新项目
- **移除** — 取消注册项目，可选择删除文件
- **切换视图** — 网格/列表布局，并持久化偏好

## 快捷键

| 快捷键 | 操作 |
|---|---|
| `Ctrl+S` | 保存当前文件 |
| `Ctrl+Enter` | 编译 |
| `Ctrl+P` | 快速打开 |
| `Ctrl+Shift+F` | 项目搜索 |
| `Ctrl+Shift+C` | Git 提交 |
| `Ctrl+Shift+P` | Git 推送 |
| `Ctrl+/` | 快捷键帮助 |

## Docker Compose

使用 Docker Compose 快速启动：

```bash
docker compose up
```

Tinyleaf 会运行在 `http://localhost:14159`。

## Tinyleaf vs. Overleaf CE

| | Tinyleaf | Overleaf CE |
|---|---|---|
| 主要场景 | 个人/本地 TeX 编辑 | 多用户协作平台 |
| 安装 | `pip install tinyleaf` | Docker Compose 服务栈 |
| 运行服务 | Python 标准库服务器 | MongoDB、Redis、Node.js、CLSI 等 |
| 项目存储 | 你的文件系统 | 应用托管的存储 |
| 编译方式 | Docker TeX Live 或本机 `latexmk` | CLSI 服务 |
| Git 工作流 | 内置轻量 UI | Git Bridge |
| 协作 | 单用户优先 | 多用户 |

Tinyleaf 不试图复刻完整的 Overleaf 协作模型。它服务于想要快速、自托管、浏览器化 TeX 编辑体验的个人写作者。

## 文档

- [文档](https://tinyleaf.readthedocs.io)
- [品牌资产](./BRAND.md)
- [商标与命名政策](./TRADEMARKS.md)

## 许可证

AGPL-3.0-or-later
