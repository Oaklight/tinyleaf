# API 参考

Tinyleaf 暴露 RESTful HTTP API，由浏览器前端消费。所有响应使用 UTF-8 编码。错误统一返回 `{"error": "描述"}`。

!!! note "单项目 vs. 多项目模式"
    在**单项目模式**下，项目管理端点（`POST /api/projects`、`DELETE` 等）不可用。在**多项目模式**下，所有端点均可用。

---

## 模式与 Docker

### `GET /api/mode`

返回服务器模式和 Docker 配置。

**响应：**

```json
{
  "mode": "single",
  "docker": true,
  "image": "oaklight/texlive:alpine-science-cn",
  "version": "0.1.0"
}
```

### `GET /api/docker/images`

列出可用的 Docker 镜像标签及是否已本地拉取。

**响应：**

```json
[
  {"tag": "alpine-science-cn", "name": "oaklight/texlive:alpine-science-cn", "local": true},
  {"tag": "alpine-science", "name": "oaklight/texlive:alpine-science", "local": false}
]
```

### `POST /api/docker/pull`

拉取 Docker 镜像。拉取完成后返回。

**请求：** `{"image": "oaklight/texlive:alpine-science"}`

**响应：** `{"success": true, "message": "Pulled oaklight/texlive:alpine-science"}`

### `POST /api/docker/rmi`

删除本地 Docker 镜像。

**请求：** `{"image": "oaklight/texlive:alpine-science"}`

**响应：** `{"success": true, "message": "Removed oaklight/texlive:alpine-science"}`

---

## 项目

### `GET /api/projects`

列出所有已注册项目。

**响应：**

```json
[
  {
    "name": "my-thesis",
    "path": "/home/user/documents/thesis",
    "added_at": "2025-01-15T10:30:00",
    "exists": true,
    "git": true
  }
]
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 项目显示名称 |
| `path` | string | 绝对文件系统路径 |
| `exists` | bool | 目录是否存在于磁盘上 |
| `git` | bool | 目录是否为 Git 仓库 |

### `POST /api/projects`

创建包含默认 `main.tex` 的新项目。

**请求：**

```json
{"name": "new-paper", "path": "/home/user/documents"}
```

**响应（201）：**

```json
{"name": "new-paper", "path": "/home/user/documents/new-paper"}
```

**错误：** `409` 目录已存在，`400` 名称无效。

### `POST /api/projects/register`

注册已有目录为项目。

**请求：**

```json
{"path": "/home/user/documents/thesis", "name": "my-thesis"}
```

`name` 字段可选 — 默认使用目录名。

**响应（201）：**

```json
{"name": "my-thesis", "path": "/home/user/documents/thesis", "added_at": "2025-01-15T10:30:00"}
```

### `DELETE /api/projects/{name}`

取消注册项目。可选择同时从磁盘删除文件。

**请求：**

```json
{"delete_files": false}
```

**响应：**

```json
{"deleted": "my-thesis", "files_deleted": false}
```

### `POST /api/projects/{name}/rename-project`

重命名项目的显示名称。

**请求：** `{"new_name": "thesis-v2"}`

**响应：** `{"old_name": "my-thesis", "new_name": "thesis-v2"}`

---

## 文件系统浏览

### `GET /api/fs/browse?path={dir_path}`

列出指定路径下的子目录。供"打开文件夹"对话框使用。

**响应：**

```json
{"path": "/home/user", "dirs": ["documents", "projects", "Desktop"]}
```

---

## 文件

### `GET /api/projects/{name}/files`

返回完整文件树（嵌套结构）。

**响应：**

```json
[
  {
    "name": "main.tex",
    "path": "main.tex",
    "type": "file",
    "mtime": 1706000000
  },
  {
    "name": "sections",
    "path": "sections",
    "type": "dir",
    "children": [
      {"name": "intro.tex", "path": "sections/intro.tex", "type": "file", "mtime": 1706000000}
    ]
  }
]
```

### `GET /api/projects/{name}/files/{file_path}`

读取文件内容（仅 UTF-8 文本文件）。

**响应：**

```json
{"path": "main.tex", "content": "\\documentclass{article}\n...", "mtime": 1706000000}
```

**错误：** `400` 二进制文件，`404` 文件不存在。

### `GET /api/projects/{name}/check/{file_path}`

检查文件是否存在并获取修改时间。用于检测外部更改。

**响应：**

```json
{"path": "main.tex", "mtime": 1706000000}
```

文件不存在时返回 `{"exists": false}`。

### `PUT /api/projects/{name}/files/{file_path}`

写入文件内容。自动创建父目录。

**请求：**

```json
{"content": "\\documentclass{article}\n..."}
```

**响应：** `{"path": "main.tex", "saved": true}`

### `DELETE /api/projects/{name}/files/{file_path}`

删除文件或目录（递归删除）。

**响应：** `{"path": "old-file.tex", "deleted": true}`

### `POST /api/projects/{name}/mkdir`

创建新目录。

**请求：** `{"path": "figures/plots"}`

**响应：** `{"path": "figures/plots", "created": true}`

**错误：** `409` 路径已存在。

### `POST /api/projects/{name}/rename`

重命名或移动文件/目录。

**请求：**

```json
{"old_path": "intro.tex", "new_path": "sections/intro.tex"}
```

**响应：** `{"old_path": "intro.tex", "new_path": "sections/intro.tex", "renamed": true}`

### `POST /api/projects/{name}/upload`

通过 multipart 表单上传文件。

**请求：** `Content-Type: multipart/form-data`

| 字段 | 类型 | 说明 |
|------|------|------|
| `files` | file(s) | 一个或多个文件 |
| `target_dir` | string | 可选目标子目录路径 |

**响应：**

```json
{"uploaded": ["figures/plot1.png", "figures/plot2.png"], "count": 2}
```

---

## 配置

### `GET /api/projects/{name}/config`

读取项目配置。若无 `.tinyleaf.json` 则返回自动检测值。

**响应：**

```json
{
  "main_file": "main.tex",
  "engine": "pdflatex",
  "use_docker": true,
  "docker_image": "oaklight/texlive:alpine-science-cn"
}
```

### `PUT /api/projects/{name}/config`

更新项目配置。字段与现有值合并。

**请求：**

```json
{"engine": "lualatex", "main_file": "thesis.tex"}
```

**响应：** 合并后的完整配置对象。

### `GET /api/settings`

读取全局设置（仅多项目模式）。

### `PUT /api/settings`

更新全局设置。与现有值合并。

**请求：**

```json
{"registry_mirror": "docker.1ms.run"}
```

---

## 编译

### `POST /api/projects/{name}/compile`

启动异步编译任务。

**请求（所有字段可选）：**

```json
{
  "main_file": "main.tex",
  "engine": "pdflatex",
  "use_docker": true,
  "docker_image": "oaklight/texlive:alpine-science-cn"
}
```

**响应：**

```json
{"compile_id": "a1b2c3d4", "main_file": "main.tex", "engine": "pdflatex"}
```

### `GET /api/projects/{name}/compile/{compile_id}/stream`

编译日志的 Server-Sent Events (SSE) 流。

**事件类型：**

| 事件 | 数据 | 说明 |
|------|------|------|
| `log` | `{"line": "...", "level": "info"}` | 一行编译输出 |
| `done` | `{"status": "success", "pdf_url": "/api/projects/.../output/main.pdf"}` | 编译完成 |

`level` 字段为 `info`、`warning` 或 `error`。`status` 字段为 `success`、`error` 或 `cancelled`。

### `POST /api/projects/{name}/compile/{compile_id}/cancel`

取消正在运行的编译。

**响应：** `{"cancelled": true}`

### `GET /api/projects/{name}/output/{file_path}`

下载编译产物（PDF、图片等）。返回二进制文件并设置相应的 `Content-Type`。

### `POST /api/projects/{name}/clean`

清除 LaTeX 构建产物（`.aux`、`.log`、`.synctex.gz` 等）。

**响应：**

```json
{"removed": ["main.aux", "main.log", "main.synctex.gz"], "count": 3}
```

---

## Git

所有 Git 端点在项目非 Git 仓库时返回 `{"git": false}`。

### `GET /api/projects/{name}/git/status`

**响应：**

```json
{
  "git": true,
  "branch": "main",
  "files": [
    {"path": "main.tex", "status": "M"},
    {"path": "new-file.tex", "status": "??"}
  ],
  "ahead": 1,
  "behind": 0
}
```

状态码遵循 git porcelain 格式：`M`（已修改）、`A`（已添加）、`D`（已删除）、`??`（未跟踪）等。

### `GET /api/projects/{name}/git/diff`

返回完整项目差异（纯文本）。

### `GET /api/projects/{name}/git/diff/{file_path}`

返回单个文件的差异（纯文本）。

### `GET /api/projects/{name}/git/log`

返回最近 20 条提交。

**响应：**

```json
[
  {
    "hash": "a1b2c3d",
    "message": "Add introduction section",
    "author": "Alice",
    "date": "2025-01-15T10:30:00"
  }
]
```

### `POST /api/projects/{name}/git/commit`

暂存文件并创建提交。

**请求：**

```json
{"message": "Update thesis draft", "files": ["main.tex", "sections/intro.tex"]}
```

省略 `files` 时暂存所有已更改文件。

**响应：** `{"success": true, "message": "Committed a1b2c3d"}`

### `POST /api/projects/{name}/git/push`

推送到远程仓库。

**响应：** `{"success": true, "message": "Pushed to origin/main"}`

### `POST /api/projects/{name}/git/pull`

从远程仓库拉取。

**响应：** `{"success": true, "message": "Already up to date"}`

---

## SyncTeX

SyncTeX 提供源文件与编译 PDF 之间的双向导航。需要编译时生成的 `.synctex.gz` 文件（tinyleaf 默认使用 `-synctex=1` 编译）。

### `GET /api/projects/{name}/synctex?page={N}&x={X}&y={Y}`

反向搜索：根据 PDF 页面上的位置查找对应源码位置。

**查询参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `page` | int | 从 1 开始的页码 |
| `x` | float | 水平位置，PDF 点（72 DPI） |
| `y` | float | 垂直位置，PDF 点（72 DPI） |

**响应：**

```json
{"file": "main.tex", "line": 42}
```

**错误：** `404` 无 SyncTeX 文件或无匹配结果。

### `GET /api/projects/{name}/synctex/forward?file={path}&line={N}`

正向搜索：根据源文件和行号查找 PDF 对应位置。

**查询参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `file` | string | 源文件路径（相对于项目根目录） |
| `line` | int | 从 1 开始的行号 |

**响应：**

```json
{"page": 1, "x": 150.0, "y": 300.0}
```

坐标单位为 PDF 点（72 DPI）。

**错误：** `400` 缺少参数，`404` 无 SyncTeX 文件或无匹配结果。
