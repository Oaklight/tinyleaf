# 编译

Tinyleaf 支持两种编译后端：**本地编译**和 **Docker 编译**（默认）。

## Docker 编译（默认）

使用包含完整 TeX Live 的 Docker 容器：

```bash
tinyleaf /path/to/project
```

默认 Docker 镜像为 `oaklight/texlive:alpine-science-cn`。可以指定其他镜像：

```bash
tinyleaf /path/to/project --image oaklight/texlive:alpine-science
```

!!! note "自动拉取"
    如果 Docker 镜像本地不存在，tinyleaf 会在首次编译时自动拉取。可以在设置中配置镜像仓库加速下载。

## 本地编译

使用主机系统上安装的 `latexmk`：

```bash
tinyleaf /path/to/project --no-docker
```

!!! note "前提条件"
    需要本地安装包含 `latexmk` 的 TeX Live 发行版。

## 项目级配置

每个项目可以有一个 `.tinyleaf.json` 配置文件：

```json
{
  "main_file": "thesis.tex",
  "engine": "lualatex",
  "docker_image": "oaklight/texlive:alpine-science-cn"
}
```

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `main_file` | 自动检测 | 包含 `\documentclass` 的 `.tex` 文件 |
| `engine` | `pdflatex` | LaTeX 引擎：`pdflatex`、`lualatex`、`xelatex` |
| `docker_image` | 服务器默认值 | 为此项目覆盖 Docker 镜像 |

## 自动检测

如果未配置 `main_file`，tinyleaf 会扫描包含 `\documentclass` 的 `.tex` 文件。如果恰好找到一个，就使用它。如果有多个候选，优先选择 `main.tex`。也可以从工具栏的下拉菜单中手动选择主文件。

## 编译日志

编译输出通过 SSE（Server-Sent Events）实时推送到浏览器日志面板。日志面板包含复制按钮，方便分享错误信息。

## 取消编译

可以从工具栏取消正在运行的编译任务。Docker 镜像拉取操作同样支持取消。
