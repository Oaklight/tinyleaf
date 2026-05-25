# 更新日志

本文件记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/spec/v2.0.0.html)。

## [0.4.0] - 2026-05-25

### 新增

- **\ref/\cite/\label 自动补全** — 输入 `\ref{`、`\cite{`、`\label{` 时自动提供来自 `.tex` 和 `.bib` 文件的符号补全
- **PDF 文字搜索**（PDF 区域 `Ctrl+F`）— 在渲染的 PDF 中搜索，高亮匹配并支持上下翻页
- **导出项目为 ZIP** — 将整个项目打包下载为 `.zip` 文件
- **字数/页数统计** — 基于 `texcount` 的字数和页数统计，显示在状态栏
- **PDF 页码导航** — PDF 工具栏中的页码输入框和上下翻页按钮
- **自动配对 `\begin{env}` → `\end{env}`** — 输入 `\begin{...}` 自动插入匹配的 `\end{...}`
- **快速打开**（`Ctrl+P`）— 模糊文件切换器
- **多标签编辑器** — 在标签页中打开多个文件，`Ctrl+W` 关闭，`Ctrl+Tab` 切换
- **Git 差异查看器** — 生产级的暂存/未暂存分栏差异视图
- **LaTeX 大纲**侧边栏标签页 — 从 `\section`、`\subsection` 等提取文档结构，支持 `\input`/`\include` 递归
- **可点击编译日志** — 日志中的 `文件名:行号` 引用可点击跳转到源码位置
- **SyncTeX 提示** — PDF 页面悬停显示"Ctrl+点击跳转到源码"
- **`--version` / `-V` 参数** — 显示当前版本并检查 PyPI 更新
- **翡翠绿主题** — 浅色主题的强调色从蓝色更改为翡翠绿（#059669）
- **SVG 叶子 logo** — 自定义 favicon 和工具栏品牌图标

### 变更

- 默认端口从 `8080` 更改为 `14159`（π）
- 工具栏中移除重复的 Commit/Push 按钮（保留在 Git 侧边栏中）
- PDF 搜索按钮使用 SVG 图标替代 emoji
- 复选框通过 `accent-color` 跟随主题色
- `Ctrl+H` 拦截为打开编辑器查找/替换面板而非浏览器历史

### 内部

- **前端拆分** — 单体 `index.html`（约 5700 行）拆分为 `index.html` + `css/app.css` + `js/app.js`
- 新增 `/static/` 路由的静态文件服务，支持 MIME 类型检测和路径遍历防护
- 内联 `onclick` 处理器迁移为 `addEventListener`，兼容 ES 模块

## [0.3.0] - 2026-05-18

### 新增

- **布局切换器**（Overleaf 风格）位于状态栏左下角——三种预设：
    - **Editor**：侧边栏 + 编辑器，隐藏 PDF
    - **Split**：三栏全显（默认）
    - **PDF**：仅显示 PDF，隐藏侧边栏和编辑器
- **侧边栏折叠按钮**——项目打开后显示于工具栏
- **编译日志开关**移至状态栏；新增 `Ctrl+\`` 快捷键开关日志面板
- 布局切换快捷键：`Ctrl+Shift+1` / `2` / `3`
- `Ctrl+B` 快捷键切换侧边栏（PDF 模式下禁用）
- 布局偏好持久化至 `localStorage`
- 快捷键弹窗新增布局相关条目（中英文）

### 变更

- 编译日志开关按钮从工具栏移至状态栏右侧
- 布局切换器置于状态栏最左侧，视觉上更突出

### 内部

- 新增 CI lint workflow（ruff + ty via pre-commit），在 push 和 PR 时自动运行
- 新增 release workflow（手动 `workflow_dispatch` 触发）
- 修复 `ty` 类型收窄：在 `compiler.py` 中添加 `assert proc.stdout is not None`
- 将 `_vendor/` 从 ruff 格式化范围中排除

## [0.2.0] - 2026-04-29

### 新增

- **项目级全文搜索**（`Ctrl+Shift+F`）——grep 风格的项目内文件搜索，结果按文件分组，关键词高亮，点击跳转到对应行
- **关闭文件按钮**（×）——面包屑栏中新增关闭按钮，可将编辑器恢复为空白状态
- 搜索支持大小写敏感切换

### 修复

- **CDN 回退**：从 jsdelivr 切换至 esm.sh，解决模块去重问题——修复单项目模式下无 vendor 文件时 CodeMirror 崩溃（"多个 @codemirror/state 实例"）
- 语言扩展冲突时自动降级（编辑器可用，仅无语法高亮）

### 变更

- 面包屑栏布局调整：定位按钮移至文件名左侧，关闭按钮在右侧

## [0.1.0] - 2026-04-28

tinyleaf 首次发布（前身为 texlive-web）。

### 新增

#### 核心

- **CLI 优先设计**：通过 `pip install tinyleaf && tinyleaf /path` 即可启动编辑器
- **单项目模式**：直接打开指定的 LaTeX 项目目录
- **多项目模式**：基于 JSON 的项目注册表（`~/.config/tinyleaf/projects.json`）
    - 打开文件夹：浏览并注册已有目录
    - 新建项目：在指定位置创建新项目
    - 重命名和移除项目
    - 网格与列表视图切换，偏好持久化
    - 按名称和路径搜索过滤项目
- **双编译后端**：本地 `latexmk` 和 Docker（默认启用）
- **零 Python 依赖**——仅使用标准库（`http.server`、`threading`、`subprocess`）

#### 编辑器

- **CodeMirror 6** 编辑器，支持 LaTeX 语法高亮
- 多语言语法高亮（LaTeX、Markdown、JavaScript、Python、JSON、CSS、HTML、YAML）
- 自动保存，支持自定义间隔
- 主文件选择器，自动检测 `\documentclass`
- 文件路径面包屑导航，支持在文件树中定位
- 通过 mtime 轮询检测外部文件变更
- 二进制文件拦截（图片在 PDF 面板中预览）

#### PDF 预览

- **PDF.js** 查看器，编译后自动刷新
- 缩放控制（+、-、适应、百分比）和高清/快速渲染切换
- **SyncTeX** 双向搜索，基于纯 Python 解析器
    - **反向搜索**：在 PDF 上 `Ctrl+点击` 跳转到对应源码行
    - **正向搜索**：在编辑器中 `Ctrl+Shift+Enter` 跳转到 PDF 对应位置并高亮闪烁
- 彩色状态栏消息（错误/警告/成功）
- 编译取消支持

#### 侧边栏与文件树

- 可调整大小和折叠的侧边栏和 PDF 面板
- 文件和 Git 标签页
- 文件树展开/折叠状态持久化
- 全部折叠按钮、搜索、上传、新建文件/文件夹、删除、重命名
- **项目级全文搜索**（`Ctrl+Shift+F`）——grep 风格的项目内文件搜索，结果按文件分组，关键词高亮，点击跳转到对应行
- LaTeX 构建产物在文件树中灰显

#### Git 集成

- Git 状态、差异（包括逐文件差异视图）、提交、推送、拉取和日志
- 选择性文件暂存提交
- 项目卡片上的 Git 标识，显示仓库状态

#### 设置与界面

- 7 款主题，支持明暗模式切换（Light、Indigo Dark、Dracula 等）
- Docker 开关，镜像管理（拉取、删除、镜像仓库）
- 首次编译自动拉取 Docker 镜像
- 关于弹窗，显示版本、GitHub 和 PyPI 链接
- 键盘快捷键帮助面板（`Ctrl+/`）
- 国际化支持（英文和中文）
- 本地 JS 模块，CDN 回退和代理支持

#### 编译

- SSE（Server-Sent Events）实时编译日志推送
- 日志面板，支持复制按钮
- 清理构建产物按钮
- Docker Compose 部署支持

#### 快捷键

| 快捷键 | 操作 |
|--------|------|
| `Ctrl+S` | 保存文件 |
| `Ctrl+Enter` | 编译 |
| `Ctrl+Shift+Enter` | 跳转到 PDF（正向搜索） |
| `Ctrl+点击`（PDF） | 跳转到源码（反向搜索） |
| `Ctrl+Shift+E` | 文件标签页 |
| `Ctrl+Shift+F` | 搜索标签页 |
| `Ctrl+Shift+G` | Git 标签页 |
| `Ctrl+Shift+Alt+C` | Git 提交 |
| `Ctrl+Shift+Alt+P` | Git 推送 |
| `Ctrl+/` | 显示快捷键 |

### 变更

- 项目从 `texlive-web` 重命名为 `tinyleaf`
- Python 包从 `texlive_web` 重命名为 `tinyleaf`
- 更新了 CLI 入口、配置目录和程序名称
- 默认编译后端改为 Docker（使用 `--no-docker` 切换为本地编译）

[0.4.0]: https://github.com/Oaklight/tinyleaf/releases/tag/v0.4.0
[0.3.0]: https://github.com/Oaklight/tinyleaf/releases/tag/v0.3.0
[0.2.0]: https://github.com/Oaklight/tinyleaf/releases/tag/v0.2.0
[0.1.0]: https://github.com/Oaklight/tinyleaf/releases/tag/v0.1.0
