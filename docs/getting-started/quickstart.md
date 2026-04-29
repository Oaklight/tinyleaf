# 快速开始

## 单项目模式

直接打开一个 LaTeX 项目目录：

```bash
tinyleaf /path/to/my-thesis
```

编辑器将在 `http://localhost:8080` 启动并自动打开浏览器。默认启用 Docker 编译。

### 禁用 Docker（本地编译）

```bash
tinyleaf /path/to/my-thesis --no-docker
```

### 自定义端口和地址

```bash
tinyleaf /path/to/my-thesis --port 3000 --host 0.0.0.0
```

### 自定义 Docker 镜像

```bash
tinyleaf /path/to/my-thesis --image oaklight/texlive:alpine-science
```

## 多项目模式

不带参数启动即进入注册表模式：

```bash
tinyleaf
```

在项目页面你可以：

- **打开文件夹** — 浏览文件系统，注册已有目录
- **新建项目** — 在指定路径创建新的 LaTeX 项目
- **重命名** — 修改项目显示名称
- **移除** — 取消注册项目（可选择同时从磁盘删除文件）
- **搜索** — 按名称或路径过滤项目
- **视图切换** — 在网格和列表视图之间切换

![项目列表](../assets/tinyleaf-project-list-grid.png)

项目信息保存在 `~/.config/tinyleaf/projects.json`。

## 快捷键

| 快捷键 | 操作 |
|--------|------|
| `Ctrl+S` | 保存当前文件 |
| `Ctrl+Enter` | 编译 |
| `Ctrl+Shift+Enter` | 跳转到 PDF（正向搜索） |
| `Ctrl+点击`（PDF） | 跳转到源码（反向搜索） |
| `Ctrl+Shift+E` | 切换到文件标签页 |
| `Ctrl+Shift+F` | 切换到搜索标签页 |
| `Ctrl+Shift+G` | 切换到 Git 标签页 |
| `Ctrl+Shift+Alt+C` | Git 提交 |
| `Ctrl+Shift+Alt+P` | Git 推送 |
| `Ctrl+/` | 显示键盘快捷键 |
| `Esc` | 关闭对话框 |

!!! tip "提示"
    随时按 `Ctrl+/` 可查看完整的快捷键面板。
