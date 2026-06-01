---
title: Tinyleaf
hide:
  - navigation
  - title
---

<div class="tinyleaf-hero" markdown>

![Tinyleaf 横幅](assets/brand/tinyleaf-leafpen-readme-light.svg){ .tinyleaf-hero__banner .tinyleaf-hero__banner--light }
![Tinyleaf 横幅](assets/brand/tinyleaf-leafpen-readme-dark.svg){ .tinyleaf-hero__banner .tinyleaf-hero__banner--dark }

<p class="tinyleaf-hero__tagline">一个轻量、敏捷、专注写作体验的 LaTeX 编辑器。</p>

<p class="tinyleaf-hero__desc">打开项目，编辑 LaTeX，预览 PDF，把编译流程放在手边。Tinyleaf 让写作保持轻快、专注、少打断。</p>

<p class="tinyleaf-badges">
  <a href="https://pypi.org/project/tinyleaf/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/tinyleaf?color=059669"></a>
  <a href="https://github.com/Oaklight/tinyleaf/releases/latest"><img alt="GitHub release" src="https://img.shields.io/badge/release-v0.5.0-059669"></a>
  <a href="https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml"><img alt="CI" src="https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml/badge.svg"></a>
  <a href="https://www.gnu.org/licenses/agpl-3.0"><img alt="License: AGPL v3" src="https://img.shields.io/badge/License-AGPL_v3-047857.svg"></a>
</p>

<p class="tinyleaf-actions">
  <a class="tinyleaf-button tinyleaf-button--primary" href="getting-started/quickstart/">快速开始</a>
  <a class="tinyleaf-button tinyleaf-button--secondary" href="screenshots/">查看截图</a>
  <a class="tinyleaf-button tinyleaf-button--secondary" href="https://github.com/Oaklight/tinyleaf">GitHub</a>
</p>

</div>

![编辑器视图](assets/tinyleaf-editor.png)

## 特性

- **零依赖** — 仅使用标准库（`http.server` + `threading` + `subprocess`）
- **两种模式** — 单项目或基于注册表的多项目模式
- **两种编译后端** — 本地 `latexmk` 或 Docker 容器（默认）
- **CodeMirror 6** 编辑器 + 多语言语法高亮
- **PDF.js** 预览，支持缩放、高清渲染、文字搜索和页码导航
- **LaTeX 自动补全** — `\ref{}`、`\cite{}`、`\label{}` 符号扫描补全
- **Git 集成** — 状态、差异、提交、推送、拉取
- **多标签编辑器**，快速打开（`Ctrl+P`）和 `\begin`/`\end` 自动配对
- **7 套主题**，支持明暗切换（翡翠绿主色调）
- **国际化** — 中英双语
- **键盘快捷键** — 完整的快捷键帮助面板（`Ctrl+/`）

## 快速开始

```bash
pip install tinyleaf

# 单项目模式（默认启用 Docker 编译）
tinyleaf /path/to/my-thesis

# 多项目模式（注册表模式）
tinyleaf

# 本地编译（不使用 Docker）
tinyleaf /path/to/my-thesis --no-docker
```

查看[更多截图](screenshots.md)了解完整界面。

## 链接

- [GitHub 仓库](https://github.com/Oaklight/tinyleaf)
- [PyPI 包](https://pypi.org/project/tinyleaf/)
