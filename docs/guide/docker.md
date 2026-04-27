# Docker

Tinyleaf 可以部署为 Docker 容器，也可以使用 Docker 进行 LaTeX 编译（默认）。

## Docker 编译（默认）

Docker 编译默认启用。Tinyleaf 使用包含完整 TeX Live 的 Docker 容器：

```bash
# 默认使用 Docker
tinyleaf /path/to/project

# 指定其他镜像
tinyleaf /path/to/project --image oaklight/texlive:alpine-science
```

### 可用镜像

[oaklight/texlive](https://github.com/Oaklight/texlive) 镜像提供多种 TeX Live 配置：

| 镜像 | 说明 |
|------|------|
| `oaklight/texlive:alpine-science-cn` | 科学论文包 + 中文字体（默认）|
| `oaklight/texlive:alpine-science` | 科学论文包 |
| `oaklight/texlive:alpine-science-jp` | 科学论文包 + 日文字体 |
| `oaklight/texlive:alpine-science-kr` | 科学论文包 + 韩文字体 |
| `oaklight/texlive:debian-science-cn` | Debian 版，科学论文包 + 中文字体 |
| `oaklight/texlive:debian-science` | Debian 版，科学论文包 |

### 镜像管理

在设置面板中你可以：

- **拉取**新的 Docker 镜像
- **删除**未使用的本地镜像
- 配置**镜像仓库**加速下载
- 切换 **Show Debian** 显示 Debian 版镜像

![设置面板](../assets/tinyleaf-settings.png)

### 自动拉取

如果配置的 Docker 镜像本地不存在，tinyleaf 会在首次编译时自动拉取。

### 字体缓存

为加速后续编译，建议使用 Docker volume 缓存字体目录：

- `/root/.texlive2023/texmf-var`
- `/var/lib/texmf/luatex-cache`

## Docker Compose 部署

将编辑器本身运行在容器中：

```bash
docker compose up
```

Web 编辑器将在 `http://localhost:8080` 启动，并使用持久化的 TeX Live 容器进行编译。

## 禁用 Docker

使用本地 `latexmk` 代替 Docker：

```bash
tinyleaf /path/to/project --no-docker
```
