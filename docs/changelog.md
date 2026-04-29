# 更新日志

本文件记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/spec/v2.0.0.html)。

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

[0.1.0]: https://github.com/Oaklight/tinyleaf/releases/tag/v0.1.0
