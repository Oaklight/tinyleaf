// ══════════════════════════════════════════
// i18n
// ══════════════════════════════════════════
const I18N = {
  en: {
    compile: "Compile",
    compiling: "Compiling...",
    clean: "Clean",
    cleaned: "Cleaned {n} file(s)",
    save: "Save",
    commit: "Commit",
    push: "Push",
    theme: "Theme",
    theme_group_light: "Light",
    theme_group_dark: "Dark",
    theme_light: "Light",
    theme_paper: "Paper",
    theme_mint: "Mint",
    theme_indigo_dark: "Indigo Dark",
    theme_dracula: "Dracula",
    theme_nord: "Nord",
    language: "Language",
    docker_image: "Image",
    use_docker: "Docker",
    show_debian: "Show Debian",
    file_changed_externally: "File changed externally",
    reload: "Reload",
    dismiss: "Dismiss",
    js_modules: "JS Modules",
    update: "Update",
    downloading: "Downloading...",
    vendor_local: "Local",
    vendor_cdn: "CDN fallback",
    http_proxy: "HTTP Proxy",
    files: "Files",
    no_pdf: "No PDF",
    refresh: "Refresh",
    fit: "Fit",
    compile_to_preview: "Compile to see PDF preview",
    compile_log: "Compile Log",
    copy_log: "Copy log",
    log_copied: "Log copied to clipboard",
    copy: "Copy",
    ready: "Ready",
    projects: "Projects",
    new_project: "New Project",
    new_project_title: "New Project",
    project_name: "Project name",
    project_path: "Project path",
    open_folder: "Open Folder",
    open_folder_title: "Open Folder",
    select_this_folder: "Select This Folder",
    rename_project: "Rename",
    rename_project_title: "Rename Project",
    remove_project: "Remove Project",
    remove_project_title: "Remove Project",
    remove_project_confirm: "Remove \"{name}\" from the project list?",
    delete_files_too: "Also delete project files from disk",
    remove: "Remove",
    parent_dir: "Parent directory",
    create: "Create",
    cancel: "Cancel",
    new_file_title: "New File",
    new_folder_title: "New Folder",
    filename: "filename.tex",
    foldername: "folder-name",
    git_commit_title: "Git Commit",
    commit_message: "Commit message",
    saved: "Saved",
    committed: "Committed",
    no_changes: "No changes",
    no_diff: "No diff",
    diff_staged: "Staged changes",
    diff_unstaged: "Unstaged changes",
    diff_new_file: "New file",
    diff_no_changes: "No changes in this file",
    no_files_selected: "No files selected",
    files_selected: "file(s) selected",
    commit_selected: "Commit Selected",
    pushing: "Pushing...",
    pushed: "Pushed",
    compile_success: "Compilation successful",
    compile_failed: "Compilation failed",
    compile_cancelled: "Compilation cancelled",
    compile_error: "Compile error",
    connection_lost: "Compilation connection lost",
    loading_pdf: "Loading PDF...",
    loading: "Loading",
    pdf_error: "Failed to load PDF",
    pages: "page(s)",
    prev_page: "Previous page",
    next_page: "Next page",
    search_files: "Search files...",
    search_projects: "Search projects...",
    rename: "Rename",
    delete: "Delete",
    new_file_here: "New file here",
    new_folder_here: "New folder here",
    upload_here: "Upload here",
    download: "Download",
    rename_title: "Rename",
    new_name: "New name",
    confirm_delete: "Delete \"{name}\"?",
    deleted: "Deleted",
    renamed: "Renamed",
    uploaded: "Uploaded {n} file(s)",
    open: "Open",
    settings: "Settings",
    editor_font_size: "Font size",
    auto_save: "Auto save",
    off: "Off",
    collapse_all: "Collapse all",
    main_file: "Main file",
    auto_compile: "Auto",
    auto_compile_title: "Auto compile on save",
    engine: "Engine",
    clean_title: "Remove build artifacts",
    toggle_log: "Toggle log",
    grid_view: "Grid view",
    list_view: "List view",
    refresh: "Refresh",
    zoom_in: "Zoom in",
    zoom_out: "Zoom out",
    fit_width: "Fit width",
    toggle_hd: "Toggle HD/Fast",
    git_repo: "Git repository",
    keyboard_shortcuts: "Keyboard Shortcuts",
    shortcut_editing: "Editing",
    shortcut_compile: "Compile & Build",
    shortcut_git: "Git",
    shortcut_navigation: "Navigation",
    shortcut_general: "General",
    sc_save: "Save file",
    sc_find: "Find in file",
    sc_replace: "Find & Replace",
    sc_compile: "Compile",
    sc_files_tab: "Files tab",
    sc_git_tab: "Git tab",
    sc_commit: "Commit",
    sc_push: "Push",
    sc_close: "Close dialog / Escape",
    sc_shortcuts: "Show shortcuts",
    sc_synctex: "Jump to source (click on PDF)",
    pdf_canvas_title: "Ctrl+Click to jump to source",
    sc_forward_search: "Jump to PDF",
    shortcut_pdf: "PDF Preview",
    search_files_title: "Search files",
    upload_file_title: "Upload file",
    locate_in_tree: "Locate in tree",
    close_file: "Close file",
    toggle_sidebar: "Toggle sidebar",
    toggle_pdf: "Toggle PDF panel",
    image_error: "Failed to load image",
    binary_not_supported: "Binary file — cannot open in editor",
    registry_mirror: "Registry Mirror",
    pull: "Pull",
    pulling_image: "Pulling image...",
    pull_success: "Image pulled successfully",
    pull_failed: "Failed to pull image",
    pull_cancelled: "Image pull cancelled",
    image_removed: "Image removed",
    remove_failed: "Failed to remove image",
    confirm_rmi: "Remove local image \"{name}\"?",
    search: "Search",
    search_in_project: "Search in project",
    search_in_project_placeholder: "Search in project...",
    no_results: "No results",
    search_summary: "{n} result(s) in {f} file(s)",
    results_truncated: "Results truncated (max {n})",
    sc_search_tab: "Search tab",
    layout_editor: "Editor only",
    layout_split: "Split view",
    layout_pdf: "PDF only",
    sc_toggle_log: "Toggle compile log",
    sc_toggle_sidebar: "Toggle sidebar",
    sc_layout_editor: "Editor only layout",
    sc_layout_split: "Split layout",
    sc_layout_pdf: "PDF only layout",
    shortcut_layout: "Layout",
    outline: "Outline",
    outline_no_file: "Open a .tex file to see outline",
    outline_no_sections: "No sections found",
    sc_outline_tab: "Outline tab",
    close_tab: "Close tab",
    close_other_tabs: "Close other tabs",
    close_all_tabs: "Close all tabs",
    tab_unsaved_confirm: "\"{name}\" has unsaved changes. Close anyway?",
    sc_next_tab: "Next tab",
    sc_prev_tab: "Previous tab",
    sc_close_tab: "Close current tab",
    sc_quick_open: "Quick open file",
    quick_open_placeholder: "Type a file name…",
    quick_open_no_results: "No matching files",
    quick_open_hint_nav: "navigate",
    quick_open_hint_open: "open",
    quick_open_hint_close: "close",
    pdf_search_title: "Search in PDF",
    pdf_search_placeholder: "Search in PDF...",
    pdf_search_prev: "Previous match",
    pdf_search_next: "Next match",
    pdf_search_close: "Close search",
    pdf_search_no_results: "No results",
    pdf_search_count: "{current} of {total}",
    sc_pdf_search: "Search in PDF",
    word_count: "Word Count",
    wc_words_in_text: "Words in text",
    wc_words_in_headers: "Words in headers",
    wc_words_outside_text: "Words outside text",
    wc_words_in_captions: "Words in captions",
    wc_math_inline: "Math inlines",
    wc_math_display: "Math displayed",
    wc_total: "Total",
    wc_loading: "Counting words...",
    wc_error: "Word count failed",
    export_zip: "Export ZIP",
    export_zip_title: "Export project as ZIP",
  },
  zh: {
    compile: "编译",
    compiling: "编译中...",
    clean: "清理",
    cleaned: "已清理 {n} 个文件",
    save: "保存",
    commit: "提交",
    push: "推送",
    theme: "主题",
    theme_group_light: "明亮",
    theme_group_dark: "深色",
    theme_light: "明亮",
    theme_paper: "纸张",
    theme_mint: "薄荷",
    theme_indigo_dark: "靛蓝深色",
    theme_dracula: "德古拉",
    theme_nord: "北境",
    language: "语言",
    docker_image: "镜像",
    use_docker: "Docker",
    show_debian: "显示 Debian",
    file_changed_externally: "文件已被外部修改",
    reload: "重新加载",
    dismiss: "忽略",
    js_modules: "JS 模块",
    update: "更新",
    downloading: "下载中...",
    vendor_local: "本地",
    vendor_cdn: "CDN 回退",
    http_proxy: "HTTP 代理",
    files: "文件",
    no_pdf: "无 PDF",
    refresh: "刷新",
    fit: "适宽",
    compile_to_preview: "编译后预览 PDF",
    compile_log: "编译日志",
    copy_log: "复制日志",
    log_copied: "日志已复制到剪贴板",
    copy: "复制",
    ready: "就绪",
    projects: "项目",
    new_project: "新建项目",
    new_project_title: "新建项目",
    project_name: "项目名称",
    project_path: "项目路径",
    open_folder: "打开文件夹",
    open_folder_title: "打开文件夹",
    select_this_folder: "选择此文件夹",
    rename_project: "重命名",
    rename_project_title: "重命名项目",
    remove_project: "移除项目",
    remove_project_title: "移除项目",
    remove_project_confirm: "从项目列表中移除 \"{name}\"？",
    delete_files_too: "同时从磁盘删除项目文件",
    remove: "移除",
    parent_dir: "上级目录",
    create: "创建",
    cancel: "取消",
    new_file_title: "新建文件",
    new_folder_title: "新建文件夹",
    filename: "文件名.tex",
    foldername: "文件夹名称",
    git_commit_title: "Git 提交",
    commit_message: "提交信息",
    saved: "已保存",
    committed: "已提交",
    no_changes: "无更改",
    no_diff: "无差异",
    diff_staged: "暂存的更改",
    diff_unstaged: "未暂存的更改",
    diff_new_file: "新文件",
    diff_no_changes: "此文件无更改",
    no_files_selected: "未选择文件",
    files_selected: "个文件已选择",
    commit_selected: "提交所选",
    pushing: "推送中...",
    pushed: "已推送",
    compile_success: "编译成功",
    compile_failed: "编译失败",
    compile_cancelled: "编译已取消",
    compile_error: "编译错误",
    connection_lost: "编译连接断开",
    loading_pdf: "加载 PDF...",
    loading: "加载中",
    pdf_error: "PDF 加载失败",
    pages: "页",
    prev_page: "上一页",
    next_page: "下一页",
    search_files: "搜索文件...",
    search_projects: "搜索项目...",
    rename: "重命名",
    delete: "删除",
    new_file_here: "在此新建文件",
    new_folder_here: "在此新建文件夹",
    upload_here: "上传到此处",
    download: "下载",
    rename_title: "重命名",
    new_name: "新名称",
    confirm_delete: "删除 \"{name}\"？",
    deleted: "已删除",
    renamed: "已重命名",
    uploaded: "已上传 {n} 个文件",
    open: "打开",
    settings: "设置",
    editor_font_size: "字号",
    auto_save: "自动保存",
    off: "关闭",
    collapse_all: "全部折叠",
    main_file: "主文件",
    auto_compile: "自动",
    auto_compile_title: "保存后自动编译",
    engine: "引擎",
    clean_title: "清理构建产物",
    toggle_log: "切换日志",
    grid_view: "网格视图",
    list_view: "列表视图",
    refresh: "刷新",
    zoom_in: "放大",
    zoom_out: "缩小",
    fit_width: "适应宽度",
    toggle_hd: "高清/快速切换",
    git_repo: "Git 仓库",
    keyboard_shortcuts: "键盘快捷键",
    shortcut_editing: "编辑",
    shortcut_compile: "编译与构建",
    shortcut_git: "Git",
    shortcut_navigation: "导航",
    shortcut_general: "通用",
    sc_save: "保存文件",
    sc_find: "文件内查找",
    sc_replace: "查找与替换",
    sc_compile: "编译",
    sc_files_tab: "文件标签",
    sc_git_tab: "Git 标签",
    sc_commit: "提交",
    sc_push: "推送",
    sc_close: "关闭对话框 / 退出",
    sc_shortcuts: "显示快捷键",
    sc_synctex: "跳转到源码（点击 PDF）",
    pdf_canvas_title: "Ctrl+点击跳转到源码",
    sc_forward_search: "跳转到 PDF",
    shortcut_pdf: "PDF 预览",
    search_files_title: "搜索文件",
    upload_file_title: "上传文件",
    locate_in_tree: "在文件树中定位",
    close_file: "关闭文件",
    toggle_sidebar: "切换侧边栏",
    toggle_pdf: "切换 PDF 面板",
    image_error: "图片加载失败",
    binary_not_supported: "二进制文件 — 无法在编辑器中打开",
    registry_mirror: "镜像仓库",
    pull: "拉取",
    pulling_image: "正在拉取镜像...",
    pull_success: "镜像拉取成功",
    pull_failed: "镜像拉取失败",
    pull_cancelled: "镜像拉取已取消",
    image_removed: "镜像已删除",
    remove_failed: "删除镜像失败",
    confirm_rmi: "删除本地镜像 \"{name}\"？",
    search: "搜索",
    search_in_project: "在项目中搜索",
    search_in_project_placeholder: "在项目中搜索...",
    no_results: "无结果",
    search_summary: "{f} 个文件中找到 {n} 个结果",
    results_truncated: "结果已截断（上限 {n}）",
    sc_search_tab: "搜索标签",
    layout_editor: "仅编辑器",
    layout_split: "分屏视图",
    layout_pdf: "仅 PDF",
    sc_toggle_log: "切换编译日志",
    sc_toggle_sidebar: "切换侧边栏",
    sc_layout_editor: "仅编辑器布局",
    sc_layout_split: "分屏布局",
    sc_layout_pdf: "仅 PDF 布局",
    shortcut_layout: "布局",
    outline: "大纲",
    outline_no_file: "打开 .tex 文件以查看大纲",
    outline_no_sections: "未找到章节",
    sc_outline_tab: "大纲标签",
    close_tab: "关闭标签",
    close_other_tabs: "关闭其他标签",
    close_all_tabs: "关闭所有标签",
    tab_unsaved_confirm: "\"{name}\" 有未保存的更改。仍要关闭吗？",
    sc_next_tab: "下一个标签",
    sc_prev_tab: "上一个标签",
    sc_close_tab: "关闭当前标签",
    sc_quick_open: "快速打开文件",
    quick_open_placeholder: "输入文件名…",
    quick_open_no_results: "没有匹配的文件",
    quick_open_hint_nav: "导航",
    quick_open_hint_open: "打开",
    quick_open_hint_close: "关闭",
    pdf_search_title: "在 PDF 中搜索",
    pdf_search_placeholder: "在 PDF 中搜索...",
    pdf_search_prev: "上一个匹配",
    pdf_search_next: "下一个匹配",
    pdf_search_close: "关闭搜索",
    pdf_search_no_results: "无结果",
    pdf_search_count: "{current} / {total}",
    sc_pdf_search: "在 PDF 中搜索",
    word_count: "字数统计",
    wc_words_in_text: "正文字数",
    wc_words_in_headers: "标题字数",
    wc_words_outside_text: "正文外字数",
    wc_words_in_captions: "图表标题字数",
    wc_math_inline: "行内公式",
    wc_math_display: "行间公式",
    wc_total: "合计",
    wc_loading: "正在统计字数...",
    wc_error: "字数统计失败",
    export_zip: "导出 ZIP",
    export_zip_title: "导出项目为 ZIP",
  },
};

let currentLang = localStorage.getItem("tinyleaf-lang") || (navigator.language?.startsWith("zh") ? "zh" : "en");

function t(key) { return I18N[currentLang]?.[key] || I18N.en[key] || key; }

function applyI18n() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    const val = t(key);
    if (el.tagName === "INPUT") el.placeholder = val;
    else el.textContent = val;
  });
  document.querySelectorAll("[data-i18n-title]").forEach((el) => {
    el.title = t(el.getAttribute("data-i18n-title"));
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    el.placeholder = t(el.getAttribute("data-i18n-placeholder"));
  });
}

function setLang(lang) {
  currentLang = lang;
  localStorage.setItem("tinyleaf-lang", lang);
  document.getElementById("lang-select").value = lang;
  applyI18n();
  renderThemeOptions();
}

// ══════════════════════════════════════════
// Themes (from llm-rosetta)
// ══════════════════════════════════════════
const THEME_GROUPS = {
  light: ["light", "paper", "mint"],
  dark: ["indigo-dark", "dracula", "nord"],
};

const THEME_LABEL_KEYS = {
  light: "theme_light",
  paper: "theme_paper",
  mint: "theme_mint",
  "indigo-dark": "theme_indigo_dark",
  dracula: "theme_dracula",
  nord: "theme_nord",
};

const THEMES = {
  light: {
    "--bg": "#ffffff", "--bg-card": "#f6f8fa", "--bg-hover": "#eef1f5",
    "--border": "#d1d9e0", "--text": "#1f2328", "--text-dim": "#656d76",
    "--accent": "#059669", "--accent-hover": "#047857",
    "--green": "#1a7f37", "--red": "#cf222e", "--orange": "#bf8700", "--blue": "#0969da",
  },
  paper: {
    "--bg": "#fbf7ef", "--bg-card": "#f4eadc", "--bg-hover": "#eadfce",
    "--border": "#dccbb5", "--text": "#2f2418", "--text-dim": "#7c6b5a",
    "--accent": "#0f766e", "--accent-hover": "#0d5f59",
    "--green": "#1a7f37", "--red": "#b42318", "--orange": "#a15c07", "--blue": "#2563eb",
  },
  mint: {
    "--bg": "#f7fdf9", "--bg-card": "#eefaf3", "--bg-hover": "#dcfce7",
    "--border": "#bbf7d0", "--text": "#17211b", "--text-dim": "#5c7467",
    "--accent": "#059669", "--accent-hover": "#047857",
    "--green": "#16a34a", "--red": "#dc2626", "--orange": "#d97706", "--blue": "#0284c7",
  },
  "indigo-dark": {
    "--bg": "#0f1117", "--bg-card": "#1a1d27", "--bg-hover": "#242838",
    "--border": "#2d3148", "--text": "#e4e7ef", "--text-dim": "#8b90a5",
    "--accent": "#6366f1", "--accent-hover": "#818cf8",
    "--green": "#22c55e", "--red": "#ef4444", "--orange": "#f59e0b", "--blue": "#3b82f6",
  },
  dracula: {
    "--bg": "#282a36", "--bg-card": "#2d2f3d", "--bg-hover": "#383a4a",
    "--border": "#44475a", "--text": "#f8f8f2", "--text-dim": "#6272a4",
    "--accent": "#bd93f9", "--accent-hover": "#caa8fc",
    "--green": "#50fa7b", "--red": "#ff5555", "--orange": "#ffb86c", "--blue": "#8be9fd",
  },
  nord: {
    "--bg": "#2e3440", "--bg-card": "#3b4252", "--bg-hover": "#434c5e",
    "--border": "#4c566a", "--text": "#eceff4", "--text-dim": "#81a1c1",
    "--accent": "#88c0d0", "--accent-hover": "#8fbcbb",
    "--green": "#a3be8c", "--red": "#bf616a", "--orange": "#d08770", "--blue": "#5e81ac",
  },
};

let currentTheme = localStorage.getItem("tinyleaf-theme") || "light";
if (!THEMES[currentTheme]) currentTheme = "light";

function setTheme(name) {
  const vars = THEMES[name];
  if (!vars) return;
  const root = document.documentElement;
  for (const [k, v] of Object.entries(vars)) root.style.setProperty(k, v);
  currentTheme = name;
  localStorage.setItem("tinyleaf-theme", name);
  document.getElementById("theme-select").value = name;
  const brandWordmark = THEME_GROUPS.light.includes(name)
    ? "/static/assets/brand-wordmark-light.svg"
    : "/static/assets/brand-wordmark-dark.svg";
  document.querySelectorAll(".brand-wordmark").forEach((img) => {
    img.src = brandWordmark;
  });
}

function renderThemeOptions() {
  const sel = document.getElementById("theme-select");
  sel.replaceChildren();
  const groups = [
    { label: t("theme_group_light"), names: THEME_GROUPS.light },
    { label: t("theme_group_dark"), names: THEME_GROUPS.dark },
  ];
  for (const group of groups) {
    const optgroup = document.createElement("optgroup");
    optgroup.label = group.label;
    for (const name of group.names) {
      const opt = document.createElement("option");
      opt.value = name;
      opt.textContent = t(THEME_LABEL_KEYS[name]);
      optgroup.appendChild(opt);
    }
    sel.appendChild(optgroup);
  }
  sel.value = currentTheme;
}

function initThemeSelect() {
  const sel = document.getElementById("theme-select");
  renderThemeOptions();
  sel.onchange = () => setTheme(sel.value);
}

// ══════════════════════════════════════════
// Module loader: local vendor first, CDN fallback
// ══════════════════════════════════════════
const VENDOR = "/vendor/";
const CDN = "https://esm.sh/";

async function loadMod(localFile, cdnPath) {
  try { return await import(VENDOR + localFile); }
  catch { return await import(CDN + cdnPath); }
}

// ── PDF.js ──
const pdfjsLib = await loadMod("pdfjs.js", "pdfjs-dist@4.9.155/build/pdf.min.mjs");
{
  let workerSrc = CDN + "pdfjs-dist@4.9.155/build/pdf.worker.min.mjs";
  try {
    const r = await fetch(VENDOR + "pdfjs-worker.js", { method: "HEAD" });
    if (r.ok) workerSrc = VENDOR + "pdfjs-worker.js";
  } catch {}
  pdfjsLib.GlobalWorkerOptions.workerSrc = workerSrc;
}

// ── CodeMirror 6 ──
const [
  { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter, drawSelection },
  { EditorState },
  { defaultKeymap, history, historyKeymap, indentWithTab },
  { syntaxHighlighting, defaultHighlightStyle, bracketMatching, foldGutter, foldKeymap },
  { closeBrackets, closeBracketsKeymap, autocompletion },
  { search, searchKeymap, highlightSelectionMatches, openSearchPanel },
] = await Promise.all([
  loadMod("cm-view.js", "@codemirror/view@6"),
  loadMod("cm-state.js", "@codemirror/state@6"),
  loadMod("cm-commands.js", "@codemirror/commands@6"),
  loadMod("cm-language.js", "@codemirror/language@6"),
  loadMod("cm-autocomplete.js", "@codemirror/autocomplete@6"),
  loadMod("cm-search.js", "@codemirror/search@6"),
]);

// ── Auto-pair \begin{env} → \end{env} on Enter ──
function latexAutoCloseEnv() {
  return keymap.of([{
    key: "Enter",
    run(view) {
      const { state } = view;
      const { head } = state.selection.main;
      const line = state.doc.lineAt(head);
      const before = state.doc.sliceString(line.from, head);
      const match = before.match(/\\begin\{([^}]+)\}$/);
      if (!match) return false;
      const env = match[1];
      // Determine indentation of the current line
      const lineIndent = before.match(/^(\s*)/)[1];
      const inner = lineIndent + "  ";
      const insert = "\n" + inner + "\n" + lineIndent + "\\end{" + env + "}";
      // Place cursor on the middle (indented) line
      const cursorPos = head + 1 + inner.length;
      view.dispatch({
        changes: { from: head, insert },
        selection: { anchor: cursorPos },
        scrollIntoView: true,
      });
      return true;
    },
  }]);
}

// ── Language extensions (loaded on demand) ──
// LaTeX build artifact extensions (grayed out in file tree)
const ARTIFACT_EXTS = new Set([
  ".aux", ".bbl", ".bcf", ".blg", ".fdb_latexmk", ".fls", ".log", ".out",
  ".run.xml", ".synctex.gz", ".toc", ".lof", ".lot", ".nav", ".snm", ".vrb",
  ".xdv", ".idx", ".ilg", ".ind", ".glo", ".gls", ".ist",
]);
function isArtifact(name) {
  if (name.endsWith(".synctex.gz")) return true;
  const dot = name.lastIndexOf(".");
  return dot >= 0 && ARTIFACT_EXTS.has(name.slice(dot));
}

const LANG_MAP = {
  ".tex": { mod: "cm-lang-latex.js", cdn: "codemirror-lang-latex", fn: "latexLanguage" },
  ".bib": { mod: "cm-lang-latex.js", cdn: "codemirror-lang-latex", fn: "latexLanguage" },
  ".sty": { mod: "cm-lang-latex.js", cdn: "codemirror-lang-latex", fn: "latexLanguage" },
  ".cls": { mod: "cm-lang-latex.js", cdn: "codemirror-lang-latex", fn: "latexLanguage" },
  ".dtx": { mod: "cm-lang-latex.js", cdn: "codemirror-lang-latex", fn: "latexLanguage" },
  ".md":  { mod: "cm-lang-markdown.js", cdn: "@codemirror/lang-markdown@6", fn: "markdown" },
  ".markdown": { mod: "cm-lang-markdown.js", cdn: "@codemirror/lang-markdown@6", fn: "markdown" },
  ".mmd": { mod: "cm-lang-markdown.js", cdn: "@codemirror/lang-markdown@6", fn: "markdown" },
  ".mermaid": { mod: "cm-lang-markdown.js", cdn: "@codemirror/lang-markdown@6", fn: "markdown" },
  ".py":  { mod: "cm-lang-python.js", cdn: "@codemirror/lang-python@6", fn: "python" },
  ".pyw": { mod: "cm-lang-python.js", cdn: "@codemirror/lang-python@6", fn: "python" },
  ".js":  { mod: "cm-lang-javascript.js", cdn: "@codemirror/lang-javascript@6", fn: "javascript" },
  ".mjs": { mod: "cm-lang-javascript.js", cdn: "@codemirror/lang-javascript@6", fn: "javascript" },
  ".jsx": { mod: "cm-lang-javascript.js", cdn: "@codemirror/lang-javascript@6", fn: "javascript" },
  ".ts":  { mod: "cm-lang-javascript.js", cdn: "@codemirror/lang-javascript@6", fn: "javascript" },
  ".tsx": { mod: "cm-lang-javascript.js", cdn: "@codemirror/lang-javascript@6", fn: "javascript" },
  ".json": { mod: "cm-lang-json.js", cdn: "@codemirror/lang-json@6", fn: "json" },
  ".jsonc": { mod: "cm-lang-json.js", cdn: "@codemirror/lang-json@6", fn: "json" },
  ".css": { mod: "cm-lang-css.js", cdn: "@codemirror/lang-css@6", fn: "css" },
  ".scss": { mod: "cm-lang-css.js", cdn: "@codemirror/lang-css@6", fn: "css" },
  ".less": { mod: "cm-lang-css.js", cdn: "@codemirror/lang-css@6", fn: "css" },
  ".html": { mod: "cm-lang-html.js", cdn: "@codemirror/lang-html@6", fn: "html" },
  ".htm": { mod: "cm-lang-html.js", cdn: "@codemirror/lang-html@6", fn: "html" },
  ".xml": { mod: "cm-lang-html.js", cdn: "@codemirror/lang-html@6", fn: "html" },
  ".svg": { mod: "cm-lang-html.js", cdn: "@codemirror/lang-html@6", fn: "html" },
  ".yaml": { mod: "cm-lang-yaml.js", cdn: "@codemirror/lang-yaml@6", fn: "yaml" },
  ".yml": { mod: "cm-lang-yaml.js", cdn: "@codemirror/lang-yaml@6", fn: "yaml" },
  ".toml": { mod: "cm-lang-json.js", cdn: "@codemirror/lang-json@6", fn: "json" },
  ".ini": { mod: "cm-lang-yaml.js", cdn: "@codemirror/lang-yaml@6", fn: "yaml" },
  ".cfg": { mod: "cm-lang-yaml.js", cdn: "@codemirror/lang-yaml@6", fn: "yaml" },
  ".conf": { mod: "cm-lang-yaml.js", cdn: "@codemirror/lang-yaml@6", fn: "yaml" },
};
// Filename-based language mappings (no extension)
const LANG_NAME_MAP = {
  "Makefile": { mod: "cm-lang-python.js", cdn: "@codemirror/lang-python@6", fn: "python" },
  "Dockerfile": { mod: "cm-lang-yaml.js", cdn: "@codemirror/lang-yaml@6", fn: "yaml" },
  ".gitignore": { mod: "cm-lang-yaml.js", cdn: "@codemirror/lang-yaml@6", fn: "yaml" },
  ".dockerignore": { mod: "cm-lang-yaml.js", cdn: "@codemirror/lang-yaml@6", fn: "yaml" },
};
const _langCache = {};
async function getLangExtension(filePath) {
  const fileName = filePath.split("/").pop();
  const ext = filePath.includes(".") ? "." + filePath.split(".").pop().toLowerCase() : "";
  const spec = LANG_MAP[ext] || LANG_NAME_MAP[fileName];
  if (!spec) return null;
  const key = spec.mod;
  if (!_langCache[key]) {
    try { _langCache[key] = await loadMod(spec.mod, spec.cdn); }
    catch { _langCache[key] = null; }
  }
  const mod = _langCache[key];
  const extension = mod?.[spec.fn];
  return typeof extension === "function" ? extension() : extension || null;
}

// ══════════════════════════════════════════
// Application State
// ══════════════════════════════════════════
const S = {
  mode: "single",
  projectName: null,
  files: [],
  fileTree: [],
  modified: new Set(),
  // Multi-tab state. `tabs` is the open-tab order; `activeTab` is the path
  // currently in the editor. `editors` maps path -> { view, mtime } so each
  // tab keeps its own CodeMirror instance (preserves undo + scroll on switch).
  tabs: [],
  activeTab: null,
  editors: new Map(),
  compiling: false,
  compileId: null,
  pulling: false,
  mainFile: "main.tex",
  autoCompile: true,
  autoCompileTimer: null,
  pdfDoc: null,
  pdfUrl: null,
  pdfZoom: 1.0,
  pdfRenderHD: true,
  pdfTextPages: null,
  pdfSearchMatches: [],
  pdfSearchIndex: -1,
  autoSaveTimer: null,
  autoSaveInterval: 2000,
  useDocker: true,
  dockerImage: "oaklight/texlive:alpine-science-cn",
  projectSymbols: { labels: [], citations: [] },
};

// Back-compat aliases so the older single-file call sites keep working
// without churn. `currentFile` and `editorView` now route through the
// per-tab state. `fileMtime` reads/writes the mtime on the active tab's
// editor record.
Object.defineProperty(S, "currentFile", {
  get() { return S.activeTab; },
  set(v) { S.activeTab = v; },
});
Object.defineProperty(S, "editorView", {
  get() {
    const entry = S.activeTab ? S.editors.get(S.activeTab) : null;
    return entry ? entry.view : null;
  },
  // Legacy setter: null clears the active tab's view; otherwise no-op
  // (new views are created via openFile's tab logic).
  set(v) {
    if (v === null && S.activeTab) {
      const entry = S.editors.get(S.activeTab);
      if (entry && entry.view) entry.view.destroy();
      S.editors.delete(S.activeTab);
    }
  },
});
Object.defineProperty(S, "fileMtime", {
  get() {
    const entry = S.activeTab ? S.editors.get(S.activeTab) : null;
    return entry ? entry.mtime : 0;
  },
  set(v) {
    if (!S.activeTab) return;
    const entry = S.editors.get(S.activeTab);
    if (entry) entry.mtime = v;
  },
});

// ── API ──
async function api(method, path, body = null) {
  const opts = { method, headers: {} };
  if (body !== null) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(body);
  }
  const resp = await fetch(path, opts);
  const ct = resp.headers.get("content-type") || "";
  if (ct.includes("application/json")) {
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || `HTTP ${resp.status}`);
    return data;
  }
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  return resp;
}

function enc(s) { return encodeURIComponent(s); }
function esc(s) { const d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
function setStatus(msg, level = "info") {
  const el = document.getElementById("status-left");
  el.textContent = msg;
  el.style.color = level === "error" ? "var(--red)" : level === "warning" ? "var(--orange)" : level === "success" ? "var(--green)" : "";
}

// ══════════════════════════════════════════
// Init
// ══════════════════════════════════════════
async function init() {
  initThemeSelect();
  setTheme(currentTheme);
  setLang(currentLang);

  const info = await api("GET", "/api/mode");
  S.mode = info.mode;
  S.useDocker = info.docker;
  S.dockerImage = info.image || "oaklight/texlive:alpine-science-cn";
  document.getElementById("about-version").textContent = `v${info.version || "0.0.0"}`;

  // Always load docker images list and sync toggle
  document.getElementById("docker-toggle").checked = S.useDocker;
  document.getElementById("docker-image-row").classList.toggle("collapsed", !S.useDocker);

  // Load global settings (show_debian, etc.)
  try {
    const globalSettings = await api("GET", "/api/settings");
    document.getElementById("show-debian-toggle").checked = !!globalSettings.show_debian;
    if (globalSettings.registry_mirror) {
      document.getElementById("registry-mirror-input").value = globalSettings.registry_mirror;
    } else {
      // Auto-detect China region and suggest registry mirror
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
      const isCN = tz.startsWith("Asia/Shanghai") || tz.startsWith("Asia/Chongqing")
        || tz.startsWith("Asia/Harbin") || tz.startsWith("Asia/Urumqi")
        || navigator.language?.startsWith("zh");
      if (isCN) {
        const mirror = "docker.1ms.run";
        document.getElementById("registry-mirror-input").value = mirror;
        api("PUT", "/api/settings", { registry_mirror: mirror });
      }
    }
  } catch {}
  await loadDockerImages();

  if (S.mode === "multi") {
    const lastProject = localStorage.getItem("tinyleaf-project");
    const projects = await api("GET", "/api/projects");
    const names = projects.map(p => p.name);
    if (lastProject && names.includes(lastProject)) {
      await openProject(lastProject);
    } else {
      showProjectList();
    }
  } else {
    const projects = await api("GET", "/api/projects");
    if (projects.length > 0) openProject(projects[0].name);
  }

  setupKeybindings();
  setupSettingsPopup();
  setupFileSearch();
  setupUpload();
  setupLogClickHandler();
  setupQuickOpen();
  startFileWatcher();
  setStatus(t("ready"));

  // Reveal UI
  document.getElementById("app").classList.add("ready");
  const overlay = document.getElementById("loading-overlay");
  overlay.classList.add("hidden");
  setTimeout(() => overlay.remove(), 300);
}

// ── Settings popup (centered modal) ──
function setupSettingsPopup() {
  const btn = document.getElementById("btn-settings");
  const popup = document.getElementById("settings-popup");

  btn.onclick = (e) => {
    e.stopPropagation();
    popup.classList.toggle("open");
    closeContextMenu();
  };

  document.getElementById("btn-shortcuts").onclick = (e) => {
    e.stopPropagation();
    showShortcutsPopup();
  };

  document.getElementById("btn-wordcount").onclick = (e) => {
    e.stopPropagation();
    showWordCount();
  };

  document.getElementById("lang-select").onchange = (e) => setLang(e.target.value);

  // Font size
  const savedFontSize = localStorage.getItem("tinyleaf-fontsize") || "14";
  document.getElementById("fontsize-select").value = savedFontSize;
  document.getElementById("fontsize-select").onchange = (e) => {
    const size = e.target.value;
    localStorage.setItem("tinyleaf-fontsize", size);
    document.querySelector("#editor-container").style.fontSize = size + "px";
  };
  document.querySelector("#editor-container").style.fontSize = savedFontSize + "px";

  // Auto save interval
  const savedAutoSave = localStorage.getItem("tinyleaf-autosave") || "2000";
  document.getElementById("autosave-select").value = savedAutoSave;
  S.autoSaveInterval = parseInt(savedAutoSave, 10);
  document.getElementById("autosave-select").onchange = (e) => {
    const val = e.target.value;
    localStorage.setItem("tinyleaf-autosave", val);
    S.autoSaveInterval = parseInt(val, 10);
  };

  document.getElementById("docker-toggle").onchange = (e) => {
    S.useDocker = e.target.checked;
    document.getElementById("docker-image-row").classList.toggle("collapsed", !S.useDocker);
    if (S.projectName) {
      api("PUT", `/api/projects/${enc(S.projectName)}/config`, { use_docker: S.useDocker });
    }
  };

  document.getElementById("docker-image-select").onchange = (e) => {
    S.dockerImage = e.target.value;
    if (S.projectName) {
      api("PUT", `/api/projects/${enc(S.projectName)}/config`, { docker_image: S.dockerImage });
    }
  };

  document.getElementById("show-debian-toggle").onchange = (e) => {
    api("PUT", "/api/settings", { show_debian: e.target.checked });
    loadDockerImages(true);
  };

  // Registry mirror — save on blur
  document.getElementById("registry-mirror-input").onblur = (e) => {
    api("PUT", "/api/settings", { registry_mirror: e.target.value.trim() });
  };

  // Docker pull
  document.getElementById("btn-docker-pull").onclick = async () => {
    const sel = document.getElementById("docker-image-select");
    const image = sel.value;
    if (!image) return;
    const btn = document.getElementById("btn-docker-pull");
    if (S.pulling) {
      // Cancel the running pull
      btn.disabled = true;
      try {
        await api("POST", "/api/docker/cancel-pull", { image: S.pullingImage });
      } catch {}
      btn.disabled = false;
      return;
    }
    S.pulling = true;
    S.pullingImage = image;
    btn.textContent = t("cancel");
    setStatus(t("pulling_image"));
    try {
      const res = await api("POST", "/api/docker/pull", { image });
      if (res.success) {
        setStatus(t("pull_success"), "success");
      } else if (res.message === "Cancelled") {
        setStatus(t("pull_cancelled"), "warning");
      } else {
        setStatus(t("pull_failed") + ": " + res.message, "error");
      }
      await loadDockerImages();
    } catch (e) {
      setStatus(t("pull_failed") + ": " + e.message, "error");
    } finally {
      S.pulling = false;
      S.pullingImage = null;
      btn.textContent = t("pull");
    }
  };

  // Docker remove
  document.getElementById("btn-docker-rmi").onclick = async () => {
    const sel = document.getElementById("docker-image-select");
    const image = sel.value;
    if (!image) return;
    const name = sel.options[sel.selectedIndex]?.textContent || image;
    if (!confirm(t("confirm_rmi").replace("{name}", image))) return;
    try {
      const res = await api("POST", "/api/docker/rmi", { image });
      if (res.success) {
        setStatus(t("image_removed"), "success");
      } else {
        setStatus(t("remove_failed") + ": " + res.message, "error");
      }
      await loadDockerImages();
    } catch (e) {
      setStatus(t("remove_failed") + ": " + e.message, "error");
    }
  };

  // Vendor JS modules status + update
  checkVendorStatus();
  document.getElementById("btn-update-vendor").onclick = async () => {
    const btn = document.getElementById("btn-update-vendor");
    const status = document.getElementById("vendor-status");
    const proxy = document.getElementById("proxy-input").value.trim();
    btn.disabled = true;
    status.textContent = t("downloading");
    try {
      await api("POST", "/api/vendor/update", { proxy });
      status.textContent = t("vendor_local") + " \u2713";
    } catch (e) {
      status.textContent = "Error: " + e.message;
    } finally {
      btn.disabled = false;
    }
  };
}

async function checkVendorStatus() {
  const el = document.getElementById("vendor-status");
  try {
    const data = await api("GET", "/api/vendor/status");
    // Load saved proxy
    if (data.proxy) document.getElementById("proxy-input").value = data.proxy;
    if (data.ready) {
      const d = data.manifest.updated_at?.slice(0, 10) || "";
      el.textContent = t("vendor_local") + (d ? ` (${d})` : "");
    } else {
      el.textContent = t("vendor_cdn");
    }
  } catch {
    el.textContent = "—";
  }
}

let _allDockerImages = [];

async function loadDockerImages(filterOnly) {
  const sel = document.getElementById("docker-image-select");
  sel.innerHTML = "";
  try {
    if (!filterOnly || !_allDockerImages.length) {
      _allDockerImages = await api("GET", "/api/docker/images");
    }
    const showDebian = document.getElementById("show-debian-toggle")?.checked;
    const images = _allDockerImages.filter(img =>
      showDebian || !img.name.startsWith("debian")
    );
    for (const img of images) {
      const opt = document.createElement("option");
      opt.value = img.tag;
      opt.textContent = img.local ? `${img.name} ✓` : img.name;
      sel.appendChild(opt);
    }
    const match = images.find(i => i.tag === S.dockerImage);
    if (match) {
      sel.value = match.tag;
    } else if (images.length > 0) {
      sel.value = images[0].tag;
      S.dockerImage = images[0].tag;
    }
  } catch {
    const opt = document.createElement("option");
    opt.value = S.dockerImage;
    opt.textContent = S.dockerImage;
    sel.appendChild(opt);
  }
}

// ══════════════════════════════════════════
// File Search
// ══════════════════════════════════════════
function setupFileSearch() {
  const input = document.getElementById("file-search-input");
  input.addEventListener("input", () => {
    renderFileTree(input.value.trim().toLowerCase());
  });
  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      input.value = "";
      document.getElementById("file-search-box").classList.remove("open");
      renderFileTree();
    }
  });
}

function toggleFileSearch() {
  const box = document.getElementById("file-search-box");
  const input = document.getElementById("file-search-input");
  box.classList.toggle("open");
  if (box.classList.contains("open")) {
    input.focus();
  } else {
    input.value = "";
    renderFileTree();
  }
}

// ══════════════════════════════════════════
// File Upload
// ══════════════════════════════════════════
let uploadTargetDir = "";

function setupUpload() {
  const input = document.getElementById("file-upload-input");
  input.addEventListener("change", async () => {
    if (!input.files.length || !S.projectName) return;
    const formData = new FormData();
    if (uploadTargetDir) formData.append("target_dir", uploadTargetDir);
    for (const file of input.files) formData.append("file", file);

    try {
      const resp = await fetch(`/api/projects/${enc(S.projectName)}/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await resp.json();
      if (!resp.ok) throw new Error(data.error || "Upload failed");
      setStatus(t("uploaded").replace("{n}", data.count), "success");
      await refreshFiles();
    } catch (err) {
      setStatus(`Upload error: ${err.message}`, "error");
    }
    input.value = "";
    uploadTargetDir = "";
  });
}

function triggerUpload(targetDir = "") {
  uploadTargetDir = targetDir;
  document.getElementById("file-upload-input").click();
}

// ══════════════════════════════════════════
// Context Menu
// ══════════════════════════════════════════
function closeContextMenu() {
  document.getElementById("context-menu").classList.remove("open");
}

function showContextMenu(e, items) {
  e.preventDefault();
  e.stopPropagation();

  const menu = document.getElementById("context-menu");
  menu.innerHTML = "";
  for (const item of items) {
    if (item === "sep") {
      const sep = document.createElement("div");
      sep.className = "context-menu-sep";
      menu.appendChild(sep);
      continue;
    }
    const div = document.createElement("div");
    div.className = "context-menu-item" + (item.danger ? " danger" : "");
    div.textContent = item.label;
    div.onclick = () => { closeContextMenu(); item.action(); };
    menu.appendChild(div);
  }

  // Position the menu
  menu.style.left = e.clientX + "px";
  menu.style.top = e.clientY + "px";
  menu.classList.add("open");

  // Adjust if overflows
  requestAnimationFrame(() => {
    const rect = menu.getBoundingClientRect();
    if (rect.right > window.innerWidth) menu.style.left = (window.innerWidth - rect.width - 4) + "px";
    if (rect.bottom > window.innerHeight) menu.style.top = (window.innerHeight - rect.height - 4) + "px";
  });
}

document.addEventListener("click", closeContextMenu);
document.addEventListener("contextmenu", (e) => {
  // Close any open context menu when right-clicking elsewhere
  const menu = document.getElementById("context-menu");
  if (menu.classList.contains("open") && !menu.contains(e.target)) {
    closeContextMenu();
  }
});

function fileContextMenu(e, node) {
  const items = [];
  if (node.type === "file") {
    items.push({ label: t("open"), action: () => openFile(node.path) });
    items.push("sep");
  }
  items.push({ label: t("rename"), action: () => showRenameModal(node) });

  if (node.type === "dir") {
    items.push("sep");
    items.push({ label: t("new_file_here"), action: () => showNewFileInDirModal(node.path) });
    items.push({ label: t("new_folder_here"), action: () => showNewFolderInDirModal(node.path) });
    items.push({ label: t("upload_here"), action: () => triggerUpload(node.path) });
  }

  if (node.type === "file") {
    items.push({ label: t("download"), action: () => downloadFile(node.path) });
  }

  items.push("sep");
  items.push({ label: t("delete"), danger: true, action: () => confirmDelete(node) });

  showContextMenu(e, items);
}

function showRenameModal(node) {
  const oldName = node.name;
  showModal(t("rename_title"), `<input id="inp-rename" value="${esc(oldName)}" autofocus>`, [
    { label: t("cancel"), action: closeModal },
    { label: t("rename"), primary: true, action: async () => {
      const newName = document.getElementById("inp-rename").value.trim();
      if (!newName || newName === oldName) { closeModal(); return; }
      const parentDir = node.path.includes("/") ? node.path.substring(0, node.path.lastIndexOf("/")) : "";
      const newPath = parentDir ? parentDir + "/" + newName : newName;
      try {
        await api("POST", `/api/projects/${enc(S.projectName)}/rename`, { old_path: node.path, new_path: newPath });
        closeModal();
        setStatus(`${t("renamed")}: ${newName}`, "success");
        await refreshFiles();
        // If the renamed file was open in a tab, retire the stale tab and
        // re-open under its new path so the editor reflects the new name.
        if (S.tabs.includes(node.path)) {
          const wasActive = S.activeTab === node.path;
          const entry = S.editors.get(node.path);
          if (entry && entry.view) { try { entry.view.destroy(); } catch {} }
          S.editors.delete(node.path);
          document.querySelectorAll(`.editor-tab-pane[data-path]`).forEach((p) => {
            if (p.dataset.path === node.path) p.remove();
          });
          const idx = S.tabs.indexOf(node.path);
          if (idx !== -1) S.tabs.splice(idx, 1);
          if (S.modified.has(node.path)) {
            S.modified.delete(node.path);
            S.modified.add(newPath);
          }
          if (wasActive) await openFile(newPath);
          else { renderTabs(); persistTabs(); }
        }
      } catch (err) {
        setStatus(`Rename error: ${err.message}`, "error");
      }
    }},
  ]);
  setTimeout(() => {
    const inp = document.getElementById("inp-rename");
    if (inp) { inp.focus(); inp.select(); }
  }, 50);
}

function confirmDelete(node) {
  const msg = t("confirm_delete").replace("{name}", node.name);
  showModal(t("delete"), `<p style="margin-bottom:14px">${esc(msg)}</p>`, [
    { label: t("cancel"), action: closeModal },
    { label: t("delete"), primary: true, action: async () => {
      try {
        await api("DELETE", `/api/projects/${enc(S.projectName)}/files/${enc(node.path)}`);
        closeModal();
        setStatus(`${t("deleted")}: ${node.name}`, "success");
        // Drop any open tab(s) for the deleted file
        if (S.tabs.includes(node.path)) {
          const entry = S.editors.get(node.path);
          if (entry && entry.view) { try { entry.view.destroy(); } catch {} }
          S.editors.delete(node.path);
          S.modified.delete(node.path);
          document.querySelectorAll(`.editor-tab-pane[data-path]`).forEach((p) => {
            if (p.dataset.path === node.path) p.remove();
          });
          const idx = S.tabs.indexOf(node.path);
          if (idx !== -1) S.tabs.splice(idx, 1);
          if (S.activeTab === node.path) {
            if (S.tabs.length) switchTab(S.tabs[Math.min(idx, S.tabs.length - 1)]);
            else {
              S.activeTab = null;
              const breadcrumb = document.getElementById("breadcrumb-path");
              if (breadcrumb) { breadcrumb.textContent = "—"; breadcrumb.title = ""; }
              document.getElementById("btn-close-file").style.display = "none";
              renderTabs();
            }
          } else {
            renderTabs();
          }
          persistTabs();
        }
        await refreshFiles();
      } catch (err) {
        setStatus(`Delete error: ${err.message}`, "error");
      }
    }},
  ]);
}

function downloadFile(filePath) {
  const url = `/api/projects/${enc(S.projectName)}/files/${enc(filePath)}`;
  // Read and download via blob
  fetch(url).then(r => r.json()).then(data => {
    const blob = new Blob([data.content], { type: "text/plain;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filePath.split("/").pop();
    a.click();
    URL.revokeObjectURL(a.href);
  });
}

function showNewFileInDirModal(dirPath) {
  showModal(t("new_file_title"), `<input id="inp-newfile" placeholder="${t("filename")}" autofocus>`, [
    { label: t("cancel"), action: closeModal },
    { label: t("create"), primary: true, action: async () => {
      const fname = document.getElementById("inp-newfile").value.trim();
      if (!fname) return;
      const fullPath = dirPath ? dirPath + "/" + fname : fname;
      await api("PUT", `/api/projects/${enc(S.projectName)}/files/${enc(fullPath)}`, { content: "" });
      closeModal();
      expandedDirs.add(dirPath);
      await refreshFiles();
      await openFile(fullPath);
    }},
  ]);
  setTimeout(() => document.getElementById("inp-newfile")?.focus(), 50);
}

function showNewFolderInDirModal(dirPath) {
  showModal(t("new_folder_title"), `<input id="inp-newfolder" placeholder="${t("foldername")}" autofocus>`, [
    { label: t("cancel"), action: closeModal },
    { label: t("create"), primary: true, action: async () => {
      const fname = document.getElementById("inp-newfolder").value.trim();
      if (!fname) return;
      const fullPath = dirPath ? dirPath + "/" + fname : fname;
      try {
        await api("POST", `/api/projects/${enc(S.projectName)}/mkdir`, { path: fullPath });
        closeModal();
        expandedDirs.add(dirPath);
        expandedDirs.add(fullPath);
        await refreshFiles();
      } catch (err) {
        setStatus(`Error: ${err.message}`, "error");
      }
    }},
  ]);
  setTimeout(() => document.getElementById("inp-newfolder")?.focus(), 50);
}

// ══════════════════════════════════════════
// Project List (multi-project)
// ══════════════════════════════════════════
async function showProjectList() {
  localStorage.removeItem("tinyleaf-project");
  document.getElementById("project-list-view").style.display = "block";
  document.getElementById("editor-view").style.display = "none";
  document.getElementById("toolbar-project").style.display = "none";
  document.getElementById("toolbar-project-name").style.display = "none";
  document.getElementById("btn-sidebar-toggle").style.display = "none";
  document.getElementById("layout-switcher").style.display = "none";

  const projects = await api("GET", "/api/projects");
  const grid = document.getElementById("project-grid");
  grid.innerHTML = "";

  for (const p of projects) {
    const card = document.createElement("div");
    card.className = "project-card" + (p.exists === false ? " stale" : "");
    const timeStr = p.added_at ? new Date(p.added_at).toLocaleString() : "";
    const gitBadge = p.git ? `<span class="git-badge" title="Git repository"><svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" fill="none" stroke-width="2"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg></span>` : "";
    card.innerHTML = `<h3>${esc(p.name)} ${gitBadge}</h3>`
      + `<div class="project-path">${esc(p.path || "")}</div>`
      + `<div class="project-time">${esc(timeStr)}</div>`
      + `<button class="rename-btn" title="${t("rename_project")}"><svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" fill="none" stroke-width="2"><path d="M17 3a2.83 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg></button>`
      + `<button class="remove-btn" title="${t("remove_project")}"><svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" fill="none" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>`;
    if (p.exists !== false) {
      card.onclick = (e) => { if (!e.target.closest(".remove-btn") && !e.target.closest(".rename-btn")) openProject(p.name); };
    }
    card.querySelector(".rename-btn").onclick = (e) => { e.stopPropagation(); showRenameProjectModal(p.name); };
    card.querySelector(".remove-btn").onclick = (e) => { e.stopPropagation(); showRemoveProjectModal(p.name); };
    grid.appendChild(card);
  }

  // Restore view mode
  applyViewMode(localStorage.getItem("tinyleaf-view-mode") || "grid");

  // Clear search
  const searchInput = document.getElementById("project-search");
  if (searchInput) searchInput.value = "";
}

function applyViewMode(mode) {
  const grid = document.getElementById("project-grid");
  if (mode === "list") {
    grid.classList.add("list-view");
  } else {
    grid.classList.remove("list-view");
  }
  document.getElementById("btn-view-grid").classList.toggle("active", mode !== "list");
  document.getElementById("btn-view-list").classList.toggle("active", mode === "list");
  localStorage.setItem("tinyleaf-view-mode", mode);
}

document.getElementById("btn-view-grid").onclick = () => applyViewMode("grid");
document.getElementById("btn-view-list").onclick = () => applyViewMode("list");
document.getElementById("btn-open-folder").onclick = showOpenFolderModal;
document.getElementById("btn-new-project").onclick = showCreateProjectModal;
document.getElementById("project-search").oninput = (e) => {
  const q = e.target.value.toLowerCase();
  document.querySelectorAll("#project-grid .project-card:not(.create-new)").forEach(card => {
    const name = card.querySelector("h3")?.textContent.toLowerCase() || "";
    const path = card.querySelector(".project-path")?.textContent.toLowerCase() || "";
    card.style.display = (name.includes(q) || path.includes(q)) ? "" : "none";
  });
};

function showCreateProjectModal() {
  showModal(t("new_project_title"),
    `<div class="dir-browser" id="create-dir-browser"></div>`
    + `<label style="font-size:12px;color:var(--text-dim);margin-bottom:4px;display:block">${t("project_name")}</label>`
    + `<input type="text" id="inp-project-name" placeholder="${t("project_name")}">`,
    [
      { label: t("cancel"), action: closeModal },
      { label: t("create"), primary: true, action: async () => {
        const name = document.getElementById("inp-project-name").value.trim();
        const parentPath = document.querySelector("#create-dir-browser .dir-path")?.textContent || "";
        if (!name || !parentPath) return;
        const fullPath = parentPath === "/" ? "/" + name : parentPath + "/" + name;
        await api("POST", "/api/projects", { name, path: fullPath });
        closeModal();
        showProjectList();
      }},
    ]);
  loadDirBrowser("create-dir-browser");
  setTimeout(() => document.getElementById("inp-project-name")?.focus(), 50);
}

function showOpenFolderModal() {
  showModal(t("open_folder_title"),
    `<div class="dir-browser" id="open-dir-browser"></div>`
    + `<label style="font-size:12px;color:var(--text-dim);margin-bottom:4px;display:block">${t("project_name")}</label>`
    + `<input type="text" id="inp-folder-name" style="margin-bottom:0" readonly>`,
    [
      { label: t("cancel"), action: closeModal },
      { label: t("select_this_folder"), primary: true, action: async () => {
        const path = document.querySelector("#open-dir-browser .dir-path")?.textContent || "";
        if (!path) return;
        const name = document.getElementById("inp-folder-name").value.trim();
        const body = { path };
        if (name) body.name = name;
        try {
          await api("POST", "/api/projects/register", body);
          closeModal();
          showProjectList();
        } catch (err) {
          setStatus(`Error: ${err.message}`, "error");
        }
      }},
    ]);
  loadDirBrowser("open-dir-browser");
}

function showRenameProjectModal(name) {
  showModal(t("rename_project_title"),
    `<input type="text" id="inp-rename-project" value="${esc(name)}" placeholder="${t("project_name")}" autofocus>`,
    [
      { label: t("cancel"), action: closeModal },
      { label: t("rename"), primary: true, action: async () => {
        const newName = document.getElementById("inp-rename-project").value.trim();
        if (!newName || newName === name) { closeModal(); return; }
        try {
          await api("POST", `/api/projects/${enc(name)}/rename-project`, { new_name: newName });
          closeModal();
          setStatus(`${t("renamed")}: ${newName}`, "success");
          showProjectList();
        } catch (e) {
          setStatus(e.message || "Rename failed", "error");
        }
      }},
    ]);
  setTimeout(() => {
    const inp = document.getElementById("inp-rename-project");
    if (inp) { inp.focus(); inp.select(); }
  }, 50);
}

function showRemoveProjectModal(name) {
  const msg = t("remove_project_confirm").replace("{name}", name);
  showModal(t("remove_project_title"),
    `<p style="margin-bottom:14px">${esc(msg)}</p>`
    + `<label style="display:flex;align-items:center;gap:8px;font-size:13px;cursor:pointer">`
    + `<input type="checkbox" id="chk-delete-files"> ${t("delete_files_too")}</label>`,
    [
      { label: t("cancel"), action: closeModal },
      { label: t("remove"), primary: true, action: async () => {
        const deleteFiles = document.getElementById("chk-delete-files").checked;
        await api("DELETE", `/api/projects/${enc(name)}`, { delete_files: deleteFiles });
        closeModal();
        showProjectList();
      }},
    ]);
}

// ── Directory Browser ──
async function loadDirBrowser(containerId, startPath) {
  const container = document.getElementById(containerId);
  const path = startPath || "~";
  const data = await api("GET", `/api/fs/browse?path=${encodeURIComponent(path)}`);
  renderDirBrowser(containerId, data.path, data.dirs);
}

function renderDirBrowser(containerId, currentPath, dirs) {
  const container = document.getElementById(containerId);
  container.innerHTML = `<div class="dir-path">${esc(currentPath)}</div><div class="dir-list"></div>`;
  const list = container.querySelector(".dir-list");

  // Auto-fill project name from path basename (Open Folder modal only)
  const nameInput = document.getElementById("inp-folder-name");
  if (nameInput) {
    const basename = currentPath.replace(/\/+$/, "").split("/").pop() || "";
    nameInput.value = basename;
  }

  // Parent directory entry
  const parentPath = currentPath.replace(/\/[^/]+\/?$/, "") || "/";
  if (currentPath !== "/") {
    const parentItem = document.createElement("div");
    parentItem.className = "dir-item parent-dir";
    parentItem.innerHTML = `<svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg> ..`;
    parentItem.onclick = () => navigateDir(containerId, parentPath);
    list.appendChild(parentItem);
  }

  for (const d of dirs) {
    const item = document.createElement("div");
    item.className = "dir-item";
    item.innerHTML = `<svg viewBox="0 0 24 24"><path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/></svg>${esc(d)}`;
    const fullPath = currentPath === "/" ? "/" + d : currentPath + "/" + d;
    item.onclick = () => navigateDir(containerId, fullPath);
    list.appendChild(item);
  }

  if (dirs.length === 0 && currentPath === "/") {
    const empty = document.createElement("div");
    empty.className = "dir-item";
    empty.style.color = "var(--text-dim)";
    empty.textContent = "(empty)";
    list.appendChild(empty);
  }
}

async function navigateDir(containerId, path) {
  try {
    const data = await api("GET", `/api/fs/browse?path=${encodeURIComponent(path)}`);
    renderDirBrowser(containerId, data.path, data.dirs);
  } catch (err) {
    setStatus(`Error: ${err.message}`, "error");
  }
}

// ══════════════════════════════════════════
// Open Project
// ══════════════════════════════════════════
async function openProject(name) {
  // Clear any tabs from a previous project before switching
  if (S.tabs.length) closeAllTabs();
  S.modified.clear();
  S.projectName = name;
  localStorage.setItem("tinyleaf-project", name);
  document.getElementById("project-name").textContent = name;
  document.getElementById("project-list-view").style.display = "none";
  document.getElementById("editor-view").style.display = "flex";
  document.getElementById("toolbar-project").style.display = "flex";
  document.getElementById("toolbar-project-name").style.display = "flex";
  document.getElementById("btn-sidebar-toggle").style.display = "";
  document.getElementById("layout-switcher").style.display = "";

  // Clear previous project state
  S.pdfDoc = null;
  S.pdfTextPages = null;
  S.pdfSearchMatches = [];
  S.pdfSearchIndex = -1;
  closePdfSearch();
  const pdfContainer = document.getElementById("pdf-container");
  pdfContainer.innerHTML = `<div class="pdf-placeholder" data-i18n="compile_to_preview">${t("compile_to_preview")}</div>`;
  setPdfStatus(t("no_pdf"));

  const config = await api("GET", `/api/projects/${enc(name)}/config`);
  document.getElementById("engine-select").value = config.engine || "latexmk";

  // Sync auto-compile toggle with project config
  S.autoCompile = config.auto_compile !== false; // default true
  document.getElementById("auto-compile-toggle").checked = S.autoCompile;

  // Sync docker toggle with project config
  if ("use_docker" in config) {
    S.useDocker = config.use_docker;
    document.getElementById("docker-toggle").checked = S.useDocker;
    document.getElementById("docker-image-row").classList.toggle("collapsed", !S.useDocker);
  }
  if (config.docker_image) {
    S.dockerImage = config.docker_image;
    document.getElementById("docker-image-select").value = S.dockerImage;
  }

  await refreshFiles();
  fetchProjectSymbols(); // non-blocking symbol fetch for autocomplete

  // Populate main file selector
  S.mainFile = config.main_file || _detectMainFile();
  _populateMainFileSelect();

  // Restore persisted tabs (drop paths that no longer exist).
  const persisted = loadPersistedTabs();
  const validTabs = persisted.tabs.filter((p) => S.files.includes(p));
  if (validTabs.length > 0) {
    for (const p of validTabs) {
      try { await openFile(p); } catch {}
    }
    const desiredActive = persisted.active && validTabs.includes(persisted.active)
      ? persisted.active : validTabs[validTabs.length - 1];
    if (desiredActive && S.tabs.includes(desiredActive)) switchTab(desiredActive);
  } else if (S.files.includes(S.mainFile)) {
    await openFile(S.mainFile);
  } else if (S.files.length > 0) {
    await openFile(S.files[0]);
  }

  await refreshGit();

  // Try loading existing PDF
  const pdfName = S.mainFile.replace(/\.tex$/, ".pdf");
  try {
    const r = await fetch(`/api/projects/${enc(name)}/output/${enc(pdfName)}`);
    if (r.ok) loadPDF(`/api/projects/${enc(name)}/output/${enc(pdfName)}`);
  } catch {}

  // Show shortcuts panel on first visit
  if (!localStorage.getItem("tinyleaf-shortcuts-seen")) {
    localStorage.setItem("tinyleaf-shortcuts-seen", "1");
    showShortcutsPopup();
  }
}

// ══════════════════════════════════════════
// File Tree
// ══════════════════════════════════════════
async function refreshFiles() {
  S.fileTree = await api("GET", `/api/projects/${enc(S.projectName)}/files`);
  // Flatten for quick lookups
  S.files = [];
  function collect(nodes) {
    for (const n of nodes) {
      if (n.type === "file") S.files.push(n.path);
      else if (n.children) collect(n.children);
    }
  }
  collect(S.fileTree);
  renderFileTree();
  _populateMainFileSelect();
}

function _detectMainFile() {
  const texFiles = S.files.filter((f) => f.endsWith(".tex"));
  if (texFiles.includes("main.tex")) return "main.tex";
  // Prefer root-level .tex files with \documentclass (server already detects this)
  const rootTex = texFiles.filter((f) => !f.includes("/"));
  if (rootTex.length > 0) return rootTex[0];
  return texFiles[0] || "main.tex";
}

function _populateMainFileSelect() {
  const sel = document.getElementById("main-file-select");
  const texFiles = S.files.filter((f) => f.endsWith(".tex"));
  sel.innerHTML = "";
  for (const f of texFiles) {
    const opt = document.createElement("option");
    opt.value = f;
    opt.textContent = f;
    sel.appendChild(opt);
  }
  if (texFiles.includes(S.mainFile)) {
    sel.value = S.mainFile;
  } else if (texFiles.length > 0) {
    S.mainFile = texFiles[0];
    sel.value = S.mainFile;
  }
}

// Track which dirs are expanded (persisted to localStorage)
const expandedDirs = new Set(
  JSON.parse(localStorage.getItem("tinyleaf-expanded-dirs") || "[]")
);
function saveExpandedDirs() {
  localStorage.setItem("tinyleaf-expanded-dirs", JSON.stringify([...expandedDirs]));
}

function renderFileTree(searchFilter = "") {
  const container = document.getElementById("file-tree");
  container.innerHTML = "";
  if (searchFilter) {
    renderFilteredFiles(searchFilter, container);
  } else {
    renderTreeNodes(S.fileTree || [], container, 0);
  }
}

function renderFilteredFiles(query, parent) {
  for (const filePath of S.files) {
    if (!filePath.toLowerCase().includes(query)) continue;
    const name = filePath.split("/").pop();
    const div = document.createElement("div");
    div.className = "file-item" + (filePath === S.currentFile ? " active" : "") +
      (isArtifact(name) ? " artifact" : "");
    div.textContent = filePath;
    div.title = filePath;
    div.onclick = () => openFile(filePath);
    parent.appendChild(div);
  }
}

function renderTreeNodes(nodes, parent, depth) {
  for (const node of nodes) {
    if (node.name === ".tinyleaf.json") continue;

    if (node.type === "dir") {
      const dirEl = document.createElement("div");
      dirEl.className = "tree-dir";

      const header = document.createElement("div");
      header.className = "tree-dir-header";
      header.style.paddingLeft = (14 + depth * 16) + "px";

      const isOpen = expandedDirs.has(node.path);
      header.innerHTML = `<span class="arrow ${isOpen ? "open" : ""}"><svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg></span> ${esc(node.name)}`;
      header.onclick = () => {
        if (expandedDirs.has(node.path)) expandedDirs.delete(node.path);
        else expandedDirs.add(node.path);
        saveExpandedDirs();
        renderFileTree();
      };
      header.oncontextmenu = (e) => fileContextMenu(e, node);
      dirEl.appendChild(header);

      const childrenEl = document.createElement("div");
      childrenEl.className = "tree-dir-children" + (isOpen ? " open" : "");
      renderTreeNodes(node.children || [], childrenEl, depth + 1);
      dirEl.appendChild(childrenEl);

      parent.appendChild(dirEl);
    } else {
      const div = document.createElement("div");
      div.className = "file-item" +
        (node.path === S.currentFile ? " active" : "") +
        (S.modified.has(node.path) ? " modified" : "") +
        (isArtifact(node.name) ? " artifact" : "");
      div.style.paddingLeft = (18 + depth * 16) + "px";
      div.textContent = node.name;
      div.title = node.path;
      div.onclick = () => openFile(node.path);
      div.oncontextmenu = (e) => fileContextMenu(e, node);
      parent.appendChild(div);
    }
  }
}

function locateInTree() {
  if (!S.currentFile) return;
  // Expand all parent directories of the current file
  const parts = S.currentFile.split("/");
  for (let i = 1; i < parts.length; i++) {
    expandedDirs.add(parts.slice(0, i).join("/"));
  }
  saveExpandedDirs();
  renderFileTree();
  // Scroll the active item into view after DOM update
  setTimeout(() => {
    const active = document.querySelector("#file-tree .file-item.active");
    if (active) {
      active.scrollIntoView({ block: "center", behavior: "smooth" });
      // Brief flash effect
      active.style.outline = "2px solid var(--accent)";
      setTimeout(() => { active.style.outline = ""; }, 1000);
    }
  }, 50);
}

// ══════════════════════════════════════════
// Editor + Tab Manager
// ══════════════════════════════════════════

// Render the tab bar from S.tabs / S.activeTab. Tabs are clickable;
// each has a dirty marker (•) when modified and a close X.
function renderTabs() {
  const bar = document.getElementById("editor-tabs");
  if (!bar) return;
  bar.innerHTML = "";
  for (const path of S.tabs) {
    const tab = document.createElement("div");
    const isActive = path === S.activeTab;
    const isDirty = S.modified.has(path);
    tab.className = "editor-tab" + (isActive ? " active" : "") + (isDirty ? " dirty" : "");
    tab.dataset.path = path;
    tab.title = path;
    tab.setAttribute("role", "tab");
    tab.setAttribute("aria-selected", isActive ? "true" : "false");

    const label = document.createElement("span");
    label.className = "editor-tab-label";
    label.textContent = path.split("/").pop();
    tab.appendChild(label);

    if (isDirty) {
      const dot = document.createElement("span");
      dot.className = "editor-tab-dirty";
      dot.textContent = "•";
      dot.setAttribute("aria-label", "unsaved");
      tab.appendChild(dot);
    }

    const close = document.createElement("span");
    close.className = "editor-tab-close";
    close.textContent = "×";
    close.title = t("close_tab");
    close.onclick = (e) => { e.stopPropagation(); closeTab(path); };
    tab.appendChild(close);

    tab.onclick = () => switchTab(path);
    tab.onmousedown = (e) => {
      // Middle-click closes
      if (e.button === 1) { e.preventDefault(); closeTab(path); }
    };
    bar.appendChild(tab);
  }
}

// Persist open tabs + active tab per project (drop on project close).
function persistTabs() {
  if (!S.projectName) return;
  const key = `tinyleaf-tabs-${S.projectName}`;
  try {
    localStorage.setItem(key, JSON.stringify({ tabs: S.tabs, active: S.activeTab }));
  } catch {}
}

// Read persisted tabs for a project; returns {tabs:[], active:null} on miss.
function loadPersistedTabs() {
  if (!S.projectName) return { tabs: [], active: null };
  const key = `tinyleaf-tabs-${S.projectName}`;
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return { tabs: [], active: null };
    const obj = JSON.parse(raw);
    return {
      tabs: Array.isArray(obj.tabs) ? obj.tabs : [],
      active: typeof obj.active === "string" ? obj.active : null,
    };
  } catch {
    return { tabs: [], active: null };
  }
}

// Switch the visible editor pane to `path`. No-op if path is not an open tab.
function switchTab(path) {
  if (!path || !S.tabs.includes(path)) return;
  S.activeTab = path;
  // Show only the matching pane
  document.querySelectorAll(".editor-tab-pane").forEach((p) => {
    p.classList.toggle("active", p.dataset.path === path);
  });
  // Breadcrumb + close button
  const breadcrumb = document.getElementById("breadcrumb-path");
  if (breadcrumb) {
    breadcrumb.textContent = path;
    breadcrumb.title = path;
  }
  const btnClose = document.getElementById("btn-close-file");
  if (btnClose) btnClose.style.display = "";
  document.getElementById("reload-bar")?.remove();
  // Focus the new view
  const entry = S.editors.get(path);
  if (entry && entry.view) {
    try { entry.view.focus(); entry.view.requestMeasure(); } catch {}
  }
  renderTabs();
  renderFileTree();
  // Refresh outline if visible (active file changed)
  const outlineEl = document.getElementById("sidebar-outline");
  if (outlineEl && outlineEl.style.display !== "none") renderOutline();
  persistTabs();
}

// Close a tab. If dirty, prompt to save; aborts on cancel.
async function closeTab(path) {
  if (!path || !S.tabs.includes(path)) return;
  if (S.modified.has(path)) {
    const msg = (t("tab_unsaved_confirm") || "\"{name}\" has unsaved changes. Close anyway?")
      .replace("{name}", path.split("/").pop());
    if (!confirm(msg)) return;
    // Persist before discarding the view so user's work isn't silently lost
    try {
      const entry = S.editors.get(path);
      if (entry && entry.view) {
        const content = entry.view.state.doc.toString();
        await api("PUT", `/api/projects/${enc(S.projectName)}/files/${enc(path)}`, { content });
      }
    } catch {}
    S.modified.delete(path);
  }
  // Destroy view + remove pane
  const entry = S.editors.get(path);
  if (entry && entry.view) { try { entry.view.destroy(); } catch {} }
  S.editors.delete(path);
  document.querySelectorAll(`.editor-tab-pane[data-path]`).forEach((p) => {
    if (p.dataset.path === path) p.remove();
  });
  // Update tab list
  const idx = S.tabs.indexOf(path);
  if (idx !== -1) S.tabs.splice(idx, 1);
  // Pick a new active tab
  if (S.activeTab === path) {
    if (S.tabs.length === 0) {
      S.activeTab = null;
      const breadcrumb = document.getElementById("breadcrumb-path");
      if (breadcrumb) { breadcrumb.textContent = "—"; breadcrumb.title = ""; }
      document.getElementById("btn-close-file").style.display = "none";
      document.getElementById("reload-bar")?.remove();
      renderTabs();
      renderFileTree();
      const outlineEl = document.getElementById("sidebar-outline");
      if (outlineEl && outlineEl.style.display !== "none") renderOutline();
    } else {
      const nextIdx = Math.min(idx, S.tabs.length - 1);
      switchTab(S.tabs[nextIdx]);
    }
  } else {
    renderTabs();
    renderFileTree();
  }
  persistTabs();
}

// Cycle through open tabs by `delta` (+1 next, -1 previous). Wraps around.
function cycleTabs(delta) {
  if (S.tabs.length < 2) return;
  const idx = S.tabs.indexOf(S.activeTab);
  if (idx === -1) { switchTab(S.tabs[0]); return; }
  const next = (idx + delta + S.tabs.length) % S.tabs.length;
  switchTab(S.tabs[next]);
}

// Destroy every tab + view. Used on project close / home navigation.
function closeAllTabs() {
  for (const [, entry] of S.editors) {
    if (entry && entry.view) { try { entry.view.destroy(); } catch {} }
  }
  S.editors.clear();
  S.tabs = [];
  S.activeTab = null;
  const container = document.getElementById("editor-container");
  if (container) container.innerHTML = "";
  const bar = document.getElementById("editor-tabs");
  if (bar) bar.innerHTML = "";
  const breadcrumb = document.getElementById("breadcrumb-path");
  if (breadcrumb) { breadcrumb.textContent = "—"; breadcrumb.title = ""; }
  document.getElementById("btn-close-file").style.display = "none";
  document.getElementById("reload-bar")?.remove();
}

// ── LaTeX symbol autocomplete ──

// Fetch \label{} and @cite{} symbols from the project
async function fetchProjectSymbols() {
  if (!S.projectName) return;
  try {
    S.projectSymbols = await api("GET", `/api/projects/${enc(S.projectName)}/symbols`);
  } catch { S.projectSymbols = { labels: [], citations: [] }; }
}

// Debounce wrapper so rapid saves don't spam the endpoint
let _symbolRefreshTimer = null;
function scheduleSymbolRefresh() {
  clearTimeout(_symbolRefreshTimer);
  _symbolRefreshTimer = setTimeout(fetchProjectSymbols, 800);
}

// CodeMirror completion source for \ref{}, \cite{}, etc.
function latexCompletionSource(context) {
  const refBefore = context.matchBefore(
    /\\(?:ref|eqref|autoref|pageref|nameref|cref|Cref)\{[^}]*/
  );
  const citeBefore = context.matchBefore(
    /\\(?:cite|citet|citep|citeauthor|citeyear|nocite|textcite|parencite)\{[^}]*/
  );
  if (!refBefore && !citeBefore) return null;

  const match = refBefore || citeBefore;
  const braceIdx = match.text.indexOf("{");
  const from = match.from + braceIdx + 1;

  if (refBefore) {
    const options = S.projectSymbols.labels.map((l) => ({
      label: l.key,
      detail: `${l.file}:${l.line}`,
      type: "variable",
    }));
    return { from, options };
  } else {
    const options = S.projectSymbols.citations.map((c) => ({
      label: c.key,
      detail: `${c.year ? c.year + " " : ""}${c.title}`.slice(0, 60),
      info: c.author || undefined,
      type: "text",
    }));
    return { from, options };
  }
}

// Open `filePath` as a tab. If already open, just focuses it (no re-fetch).
// PDFs / images / other binaries are routed to preview, not the editor.
async function openFile(filePath) {
  // PDF files: load in preview panel instead of editor
  if (filePath.endsWith(".pdf")) {
    const url = `/api/projects/${enc(S.projectName)}/output/${enc(filePath)}`;
    loadPDF(url);
    return;
  }

  // Image files: show in preview panel
  const imgExts = [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".ico"];
  if (imgExts.some(e => filePath.toLowerCase().endsWith(e))) {
    const url = `/api/projects/${enc(S.projectName)}/output/${enc(filePath)}`;
    showImagePreview(url, filePath);
    return;
  }

  // Binary / unsupported files: show notice instead of opening
  const binExts = [".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".exe", ".dll", ".so", ".dylib", ".o", ".a",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp3", ".mp4", ".avi", ".mov", ".wav", ".flac",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"];
  if (binExts.some(e => filePath.toLowerCase().endsWith(e))) {
    setStatus(t("binary_not_supported"), "warning");
    return;
  }

  // Already open → just focus it
  if (S.tabs.includes(filePath) && S.editors.has(filePath)) {
    switchTab(filePath);
    return;
  }

  // Fetch + create a new editor in its own pane
  const data = await api("GET", `/api/projects/${enc(S.projectName)}/files/${enc(filePath)}`);

  const pane = document.createElement("div");
  pane.className = "editor-tab-pane";
  pane.dataset.path = filePath;
  document.getElementById("editor-container").appendChild(pane);

  const extensions = [
    lineNumbers(),
    highlightActiveLine(),
    highlightActiveLineGutter(),
    drawSelection(),
    history(),
    bracketMatching(),
    closeBrackets(),
    latexAutoCloseEnv(),
    foldGutter(),
    autocompletion({ override: [latexCompletionSource] }),
    search(),
    highlightSelectionMatches(),
    syntaxHighlighting(defaultHighlightStyle),
    keymap.of([
      ...defaultKeymap, ...historyKeymap, ...closeBracketsKeymap,
      ...foldKeymap, ...searchKeymap, indentWithTab,
    ]),
    EditorView.updateListener.of((update) => {
      if (update.docChanged) {
        S.modified.add(filePath);
        renderTabs();
        renderFileTree();
        scheduleAutoSave();
        scheduleOutlineRefresh();
      }
    }),
    EditorView.lineWrapping,
  ];
  const langExt = await getLangExtension(filePath);
  if (langExt) extensions.push(langExt);

  let view;
  try {
    view = new EditorView({
      state: EditorState.create({ doc: data.content, extensions }),
      parent: pane,
    });
  } catch {
    // Language extension may conflict with CDN-loaded core modules; retry without it
    extensions.length = extensions.length - (langExt ? 1 : 0);
    view = new EditorView({
      state: EditorState.create({ doc: data.content, extensions }),
      parent: pane,
    });
  }

  S.editors.set(filePath, { view, mtime: data.mtime || 0 });
  if (!S.tabs.includes(filePath)) S.tabs.push(filePath);
  switchTab(filePath);
}

function scheduleAutoSave() {
  if (S.autoSaveInterval <= 0) return;
  if (S.autoSaveTimer) clearTimeout(S.autoSaveTimer);
  S.autoSaveTimer = setTimeout(() => saveCurrentFile(), S.autoSaveInterval);
}

async function saveCurrentFile() {
  if (!S.currentFile || !S.editorView) return;
  const content = S.editorView.state.doc.toString();
  await api("PUT", `/api/projects/${enc(S.projectName)}/files/${enc(S.currentFile)}`, { content });
  S.modified.delete(S.currentFile);
  renderFileTree();
  setStatus(`${t("saved")} ${S.currentFile}`, "success");
  // Refresh symbols for autocomplete when .tex or .bib files change
  if (S.currentFile.endsWith(".tex") || S.currentFile.endsWith(".bib")) {
    scheduleSymbolRefresh();
  }
  // Refresh outline if the outline tab is visible
  if (document.getElementById("sidebar-outline").style.display !== "none") {
    renderOutline();
  }
  // Auto-compile after save (guard against re-entry from compile's own save)
  if (S.autoCompile && !S.compiling && !S._autoCompiling) {
    clearTimeout(S.autoCompileTimer);
    S.autoCompileTimer = setTimeout(() => {
      S._autoCompiling = true;
      compile().finally(() => { S._autoCompiling = false; });
    }, 500);
  }
}

// Close the active tab (wired to the breadcrumb X button).
function closeFile() {
  if (!S.activeTab) return;
  closeTab(S.activeTab);
}

// ══════════════════════════════════════════
// File Change Detection
// ══════════════════════════════════════════
let _checkTimer = null;

async function checkFileChanges() {
  if (!S.projectName || !S.currentFile) return;
  // Check current file mtime
  try {
    const info = await api("GET",
      `/api/projects/${enc(S.projectName)}/check/${enc(S.currentFile)}`);
    if (info.exists === false) return;
    if (S.fileMtime && info.mtime > S.fileMtime) {
      if (S.modified.has(S.currentFile)) {
        showReloadPrompt();
      } else {
        await openFile(S.currentFile);
      }
    }
  } catch {}
  // Refresh file tree for new/deleted files
  try {
    await refreshFiles();
    renderFileTree();
  } catch {}
}

function showReloadPrompt() {
  if (document.getElementById("reload-bar")) return;
  const bar = document.createElement("div");
  bar.id = "reload-bar";
  bar.style.cssText = "background:var(--accent);color:#fff;padding:6px 16px;display:flex;align-items:center;justify-content:space-between;font-size:13px;border-radius:0";
  const btnStyle = "cursor:pointer;background:rgba(255,255,255,0.2);border:none;color:#fff;padding:3px 10px;border-radius:4px";
  bar.innerHTML = `<span>${t("file_changed_externally")}</span>
    <span style="display:flex;gap:8px">
      <button class="reload-btn" style="${btnStyle}">${t("reload")}</button>
      <button class="dismiss-btn" style="${btnStyle}">${t("dismiss")}</button>
    </span>`;
  bar.querySelector(".reload-btn").addEventListener("click", () => reloadCurrentFile());
  bar.querySelector(".dismiss-btn").addEventListener("click", () => bar.remove());
  const container = document.getElementById("editor-container");
  container.parentElement.insertBefore(bar, container);
}

async function reloadCurrentFile() {
  document.getElementById("reload-bar")?.remove();
  const path = S.activeTab;
  if (!path) return;
  S.modified.delete(path);
  // Drop cached view + pane so openFile re-fetches and rebuilds
  const entry = S.editors.get(path);
  if (entry && entry.view) { try { entry.view.destroy(); } catch {} }
  S.editors.delete(path);
  document.querySelectorAll(`.editor-tab-pane[data-path]`).forEach((p) => {
    if (p.dataset.path === path) p.remove();
  });
  const idx = S.tabs.indexOf(path);
  if (idx !== -1) S.tabs.splice(idx, 1);
  await openFile(path);
}
window.reloadCurrentFile = reloadCurrentFile;

function startFileWatcher() {
  if (_checkTimer) clearInterval(_checkTimer);
  _checkTimer = setInterval(checkFileChanges, 3000);
}

document.addEventListener("visibilitychange", () => {
  if (!document.hidden) checkFileChanges();
});

// ══════════════════════════════════════════
// Compile
// ══════════════════════════════════════════
async function compile() {
  if (S.compiling) {
    // Cancel the running compilation
    if (S.compileId) {
      try {
        await api("POST", `/api/projects/${enc(S.projectName)}/compile/${S.compileId}/cancel`);
      } catch {}
    }
    return;
  }
  S.compiling = true;

  if (S.modified.has(S.currentFile)) await saveCurrentFile();

  const engine = document.getElementById("engine-select").value;
  const btnCompile = document.getElementById("btn-compile");
  btnCompile.textContent = t("cancel");
  openLog();
  clearLog();
  setStatus(t("compiling"));

  try {
    const body = { engine, main_file: S.mainFile, use_docker: S.useDocker };
    if (S.useDocker) body.docker_image = S.dockerImage;

    const result = await api("POST", `/api/projects/${enc(S.projectName)}/compile`, body);
    S.compileId = result.compile_id;
    const evtSource = new EventSource(
      `/api/projects/${enc(S.projectName)}/compile/${result.compile_id}/stream`
    );

    evtSource.addEventListener("log", (e) => {
      const d = JSON.parse(e.data);
      appendLog(d.line, d.level);
    });

    evtSource.addEventListener("done", (e) => {
      const d = JSON.parse(e.data);
      evtSource.close();
      S.compiling = false;
      S.compileId = null;
      btnCompile.textContent = t("compile");

      if (d.status === "success") {
        setStatus(t("compile_success"), "success");
        document.getElementById("log-status").innerHTML = `<span class="badge success">OK</span>`;
      } else if (d.status === "cancelled") {
        setStatus(t("compile_cancelled"), "warning");
        document.getElementById("log-status").innerHTML = `<span class="badge warning">CANCELLED</span>`;
      } else {
        setStatus(t("compile_failed"), "error");
        document.getElementById("log-status").innerHTML = `<span class="badge error">FAILED</span>`;
      }
      if (d.pdf_url) loadPDF(d.pdf_url);
      refreshFiles();
      refreshGit();
    });

    evtSource.onerror = () => {
      evtSource.close();
      S.compiling = false;
      S.compileId = null;
      btnCompile.textContent = t("compile");
      setStatus(t("connection_lost"), "error");
    };
  } catch (err) {
    S.compiling = false;
    S.compileId = null;
    btnCompile.textContent = t("compile");
    setStatus(`${t("compile_error")}: ${err.message}`, "error");
  }
}

// ══════════════════════════════════════════
// Clean
// ══════════════════════════════════════════
async function doClean() {
  if (!S.projectName) return;
  try {
    const r = await api("POST", `/api/projects/${enc(S.projectName)}/clean`);
    setStatus(t("cleaned").replace("{n}", r.count), "success");
    await refreshFiles();
  } catch (err) {
    setStatus(`Clean error: ${err.message}`, "error");
  }
}

// ══════════════════════════════════════════
// PDF Viewer
// ══════════════════════════════════════════

async function loadPDF(url) {
  const container = document.getElementById("pdf-container");
  container.innerHTML = "";
  setPdfStatus(t("loading_pdf"));
  S.pdfUrl = url;

  try {
    const pdfUrl = url + (url.includes("?") ? "&" : "?") + "t=" + Date.now();
    const doc = await pdfjsLib.getDocument(pdfUrl).promise;
    S.pdfDoc = doc;
    S.pdfZoom = 1.0;
    S.pdfTextPages = null;
    S.pdfSearchMatches = [];
    S.pdfSearchIndex = -1;
    updateZoomLabel();
    await renderPDF();
    // Extract text in the background for PDF search
    extractPdfText().catch(() => {});
  } catch (err) {
    container.innerHTML = `<div class="pdf-placeholder">${t("pdf_error")}: ${esc(err.message)}</div>`;
    setPdfStatus(t("pdf_error"));
  }
}

// Set PDF status text and toggle page nav visibility.
// When showing a status message (loading, error, etc.), hide the page nav.
// When null, hide the status text (page nav is shown separately by renderPDF).
function setPdfStatus(text) {
  const statusEl = document.getElementById("pdf-status");
  const pageNav = document.getElementById("pdf-page-nav");
  if (text) {
    statusEl.textContent = text;
    statusEl.style.display = "";
    pageNav.classList.add("hidden");
  } else {
    statusEl.style.display = "none";
    pageNav.classList.remove("hidden");
  }
}

// Observer to track which page is currently visible in the PDF container
let pdfPageObserver = null;

function setupPdfPageObserver() {
  if (pdfPageObserver) pdfPageObserver.disconnect();
  const container = document.getElementById("pdf-container");
  pdfPageObserver = new IntersectionObserver((entries) => {
    // Find the most visible canvas
    let best = null;
    let bestRatio = 0;
    for (const entry of entries) {
      if (entry.isIntersecting && entry.intersectionRatio > bestRatio) {
        bestRatio = entry.intersectionRatio;
        best = entry.target;
      }
    }
    if (best) {
      const pageNum = parseInt(best.dataset.pageNum);
      const input = document.getElementById("pdf-page-input");
      if (input && document.activeElement !== input) {
        input.value = pageNum;
      }
    }
  }, { root: container, threshold: [0, 0.25, 0.5, 0.75, 1] });

  container.querySelectorAll("canvas[data-page-num]").forEach((c) => {
    pdfPageObserver.observe(c);
  });
}

function jumpToPdfPage(pageNum) {
  if (!S.pdfDoc) return;
  const n = Math.max(1, Math.min(pageNum, S.pdfDoc.numPages));
  const container = document.getElementById("pdf-container");
  const canvas = container.querySelector(`canvas[data-page-num="${n}"]`);
  if (canvas) canvas.scrollIntoView({ behavior: "smooth", block: "start" });
  document.getElementById("pdf-page-input").value = n;
}

async function renderPDF() {
  if (!S.pdfDoc) return;
  const container = document.getElementById("pdf-container");
  container.innerHTML = "";
  const doc = S.pdfDoc;

  // Show page nav, hide status text
  setPdfStatus(null);
  const pageInput = document.getElementById("pdf-page-input");
  pageInput.value = 1;
  pageInput.max = doc.numPages;
  document.getElementById("pdf-page-total").textContent = `/ ${doc.numPages}`;

  const dpr = S.pdfRenderHD ? (window.devicePixelRatio || 2) : 1;

  for (let i = 1; i <= doc.numPages; i++) {
    const page = await doc.getPage(i);
    const baseScale = (container.clientWidth - 40) / page.getViewport({ scale: 1 }).width;
    const scale = baseScale * S.pdfZoom;
    const viewport = page.getViewport({ scale });
    const canvas = document.createElement("canvas");
    canvas.width = viewport.width * dpr;
    canvas.height = viewport.height * dpr;
    canvas.style.width = viewport.width + "px";
    canvas.style.height = viewport.height + "px";
    canvas.dataset.pageNum = i;
    canvas.dataset.scale = scale;
    canvas.title = t("pdf_canvas_title");
    canvas.addEventListener("click", (e) => {
      if (!e.ctrlKey && !e.metaKey) return;
      e.preventDefault();
      const rect = canvas.getBoundingClientRect();
      const pdfX = (e.clientX - rect.left) / parseFloat(canvas.dataset.scale);
      const pdfY = (e.clientY - rect.top) / parseFloat(canvas.dataset.scale);
      syncTexInverseSearch(parseInt(canvas.dataset.pageNum), pdfX, pdfY);
    });
    // Wrap canvas in a positioned container for search highlight overlays
    const wrapper = document.createElement("div");
    wrapper.className = "pdf-page-wrapper";
    wrapper.dataset.pageNum = i;
    wrapper.appendChild(canvas);
    container.appendChild(wrapper);
    const ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);
    await page.render({ canvasContext: ctx, viewport }).promise;
  }
  setupPdfPageObserver();
  // Re-apply search highlights after re-render (e.g. zoom change)
  if (S.pdfSearchMatches.length > 0) {
    renderPdfSearchHighlights();
  }
}

function updateZoomLabel() {
  document.getElementById("pdf-zoom-level").textContent = Math.round(S.pdfZoom * 100) + "%";
}

async function syncTexInverseSearch(page, x, y) {
  try {
    const data = await api("GET",
      `/api/projects/${enc(S.projectName)}/synctex?page=${page}&x=${x}&y=${y}`);
    if (!data.file || !data.line) return;
    if (data.file !== S.currentFile) await openFile(data.file);
    if (S.editorView) {
      const line = S.editorView.state.doc.line(data.line);
      S.editorView.dispatch({
        selection: { anchor: line.from },
        effects: EditorView.scrollIntoView(line.from, { y: "center" })
      });
      S.editorView.focus();
    }
  } catch (err) {
    console.warn("SyncTeX:", err.message);
  }
}

async function syncTexForwardSearch() {
  if (!S.editorView || !S.currentFile || !S.projectName) return;
  const container = document.getElementById("pdf-container");
  if (!container.querySelector("canvas")) {
    setStatus("Compile first to enable forward search", "warn");
    return;
  }
  const lineNum = S.editorView.state.doc.lineAt(
    S.editorView.state.selection.main.head
  ).number;
  try {
    const data = await api("GET",
      `/api/projects/${enc(S.projectName)}/synctex/forward?file=${enc(S.currentFile)}&line=${lineNum}`);
    if (!data.page) return;
    const canvases = container.querySelectorAll("canvas");
    const canvas = canvases[data.page - 1];
    if (!canvas) return;
    const scale = parseFloat(canvas.dataset.scale);
    const cssY = data.y * scale;
    const wrapper = canvas.closest(".pdf-page-wrapper") || canvas;
    const wrapperTop = wrapper.offsetTop;
    container.scrollTop = wrapperTop + cssY - container.clientHeight / 2;
    // Flash highlight
    const marker = document.createElement("div");
    marker.className = "synctex-highlight";
    marker.style.top = `${wrapperTop + cssY - 10}px`;
    marker.style.left = `${wrapper.offsetLeft}px`;
    marker.style.width = `${canvas.width / (window.devicePixelRatio || 1)}px`;
    container.appendChild(marker);
    setTimeout(() => marker.remove(), 1500);
  } catch (err) {
    setStatus(`SyncTeX: ${err.message}`, "warn");
  }
}

function showImagePreview(url, filePath) {
  const container = document.getElementById("pdf-container");
  container.innerHTML = "";
  const name = filePath.split("/").pop();
  setPdfStatus(name);
  const img = document.createElement("img");
  img.src = url + (url.includes("?") ? "&" : "?") + "t=" + Date.now();
  img.alt = name;
  img.style.cssText = "max-width:100%;max-height:100%;object-fit:contain;display:block;margin:auto;padding:16px";
  img.onerror = () => {
    container.innerHTML = `<div class="pdf-placeholder">${t("image_error")}</div>`;
  };
  container.appendChild(img);
}

// ══════════════════════════════════════════
// PDF Search
// ══════════════════════════════════════════

// Extract text content from all pages of the current PDF document.
// Each page entry contains the page number and an array of text items
// with their position transforms. Called once after PDF loads.
async function extractPdfText() {
  if (!S.pdfDoc) return;
  const pages = [];
  for (let i = 1; i <= S.pdfDoc.numPages; i++) {
    const page = await S.pdfDoc.getPage(i);
    const content = await page.getTextContent();
    pages.push({ pageNum: i, items: content.items });
  }
  S.pdfTextPages = pages;
}

// Search extracted text for query string (case-insensitive).
// Returns an array of match objects with page, item index, and
// character offset within the item string.
function searchPdfText(query) {
  if (!S.pdfTextPages || !query) return [];
  const matches = [];
  const q = query.toLowerCase();
  const qLen = q.length;

  for (const page of S.pdfTextPages) {
    // Build a concatenated text for the page so we can find matches
    // that span across text items. Track item boundaries.
    const items = page.items.filter((it) => it.str.length > 0);
    let fullText = "";
    const itemBounds = []; // {start, end, itemIdx}
    for (let idx = 0; idx < items.length; idx++) {
      const start = fullText.length;
      fullText += items[idx].str;
      itemBounds.push({ start, end: fullText.length, itemIdx: idx });
    }

    const lowerText = fullText.toLowerCase();
    let pos = 0;
    while ((pos = lowerText.indexOf(q, pos)) !== -1) {
      // Find which items this match spans
      const matchEnd = pos + qLen;
      const spannedItems = [];
      for (const bound of itemBounds) {
        if (bound.end > pos && bound.start < matchEnd) {
          spannedItems.push({
            item: items[bound.itemIdx],
            itemIdx: bound.itemIdx,
            // Character range within this item that is part of the match
            charStart: Math.max(0, pos - bound.start),
            charEnd: Math.min(bound.end - bound.start, matchEnd - bound.start),
          });
        }
      }
      matches.push({ pageNum: page.pageNum, pos, spannedItems });
      pos++;
    }
  }
  return matches;
}

// Calculate CSS position and size for a text match highlight on a canvas.
// Uses pdf.js text item transforms to map PDF coordinates to canvas pixels.
function calcHighlightRect(item, charStart, charEnd, scale, viewportHeight) {
  // item.transform = [scaleX, skewY, skewX, scaleY, translateX, translateY]
  const tx = item.transform;
  const fontSize = Math.sqrt(tx[0] * tx[0] + tx[1] * tx[1]);
  const x = tx[4];
  const y = tx[5];

  // Approximate character width — use item.width / item.str.length
  const avgCharW = item.str.length > 0 ? (item.width || 0) / item.str.length : 0;
  const hlX = x + avgCharW * charStart;
  const hlW = avgCharW * (charEnd - charStart);

  // PDF coordinates have origin at bottom-left; canvas CSS has origin at top-left
  const cssX = hlX * scale;
  const cssY = (viewportHeight - y - fontSize) * scale;
  const cssW = hlW * scale;
  const cssH = fontSize * scale * 1.2; // slight padding

  return { left: cssX, top: cssY, width: cssW, height: cssH };
}

// Remove all search highlight elements from the PDF container.
function clearPdfSearchHighlights() {
  const container = document.getElementById("pdf-container");
  container.querySelectorAll(".pdf-search-highlight").forEach((el) => el.remove());
}

// Render highlight overlays for all current matches on the correct page wrappers.
function renderPdfSearchHighlights() {
  clearPdfSearchHighlights();
  const container = document.getElementById("pdf-container");

  for (let mi = 0; mi < S.pdfSearchMatches.length; mi++) {
    const match = S.pdfSearchMatches[mi];
    const wrapper = container.querySelector(`.pdf-page-wrapper[data-page-num="${match.pageNum}"]`);
    if (!wrapper) continue;
    const canvas = wrapper.querySelector("canvas");
    if (!canvas) continue;
    const scale = parseFloat(canvas.dataset.scale);
    // Get the viewport height for coordinate conversion
    const viewportHeight = parseFloat(canvas.style.height) / scale;

    for (const span of match.spannedItems) {
      const rect = calcHighlightRect(span.item, span.charStart, span.charEnd, scale, viewportHeight);
      if (rect.width <= 0) continue;
      const hl = document.createElement("div");
      hl.className = "pdf-search-highlight" + (mi === S.pdfSearchIndex ? " active" : "");
      hl.style.left = rect.left + "px";
      hl.style.top = rect.top + "px";
      hl.style.width = rect.width + "px";
      hl.style.height = rect.height + "px";
      hl.dataset.matchIndex = mi;
      wrapper.appendChild(hl);
    }
  }
}

// Update the match count display in the search bar.
function updatePdfSearchCount() {
  const countEl = document.getElementById("pdf-search-count");
  const total = S.pdfSearchMatches.length;
  if (total === 0) {
    const query = document.getElementById("pdf-search-input").value;
    countEl.textContent = query ? t("pdf_search_no_results") : "";
  } else {
    countEl.textContent = t("pdf_search_count")
      .replace("{current}", S.pdfSearchIndex + 1)
      .replace("{total}", total);
  }
}

// Scroll to the currently active match in the PDF container.
function scrollToPdfMatch(index) {
  if (index < 0 || index >= S.pdfSearchMatches.length) return;
  S.pdfSearchIndex = index;
  const match = S.pdfSearchMatches[index];
  const container = document.getElementById("pdf-container");
  const wrapper = container.querySelector(`.pdf-page-wrapper[data-page-num="${match.pageNum}"]`);
  if (wrapper) {
    // Scroll so the match is visible
    const activeHl = wrapper.querySelector(`.pdf-search-highlight[data-match-index="${index}"]`);
    if (activeHl) {
      activeHl.scrollIntoView({ behavior: "smooth", block: "center" });
    } else {
      wrapper.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }
  // Update page input
  document.getElementById("pdf-page-input").value = match.pageNum;
  // Re-render highlights to update active state
  renderPdfSearchHighlights();
  updatePdfSearchCount();
}

// Run a PDF search with the given query string.
function executePdfSearch(query) {
  S.pdfSearchMatches = searchPdfText(query);
  S.pdfSearchIndex = S.pdfSearchMatches.length > 0 ? 0 : -1;
  renderPdfSearchHighlights();
  updatePdfSearchCount();
  if (S.pdfSearchIndex >= 0) {
    scrollToPdfMatch(0);
  }
}

// Navigate to the next or previous match.
function pdfSearchNext() {
  if (S.pdfSearchMatches.length === 0) return;
  const next = (S.pdfSearchIndex + 1) % S.pdfSearchMatches.length;
  scrollToPdfMatch(next);
}

function pdfSearchPrev() {
  if (S.pdfSearchMatches.length === 0) return;
  const prev = (S.pdfSearchIndex - 1 + S.pdfSearchMatches.length) % S.pdfSearchMatches.length;
  scrollToPdfMatch(prev);
}

// Open the PDF search bar and focus the input.
function openPdfSearch() {
  const bar = document.getElementById("pdf-search-bar");
  bar.classList.remove("hidden");
  const input = document.getElementById("pdf-search-input");
  input.focus();
  input.select();
}

// Close the PDF search bar and clear highlights.
function closePdfSearch() {
  const bar = document.getElementById("pdf-search-bar");
  bar.classList.add("hidden");
  document.getElementById("pdf-search-input").value = "";
  document.getElementById("pdf-search-count").textContent = "";
  S.pdfSearchMatches = [];
  S.pdfSearchIndex = -1;
  clearPdfSearchHighlights();
}

// ══════════════════════════════════════════
// Compile Log
// ══════════════════════════════════════════
function openLog() { document.getElementById("log-panel").classList.add("open"); }
function toggleLog() { document.getElementById("log-panel").classList.toggle("open"); }

// ══════════════════════════════════════════
// Layout Switcher
// ══════════════════════════════════════════
function setLayout(mode) {
  const sidebar          = document.getElementById("sidebar");
  const editorPane       = document.getElementById("editor-pane");
  const pdfPane          = document.getElementById("pdf-pane");
  const resizeSidebar    = document.getElementById("resize-sidebar");
  const resizePdf        = document.getElementById("resize-pdf");
  const btnSidebarToggle = document.getElementById("btn-sidebar-toggle");

  if (mode === "editor") {
    sidebar.classList.remove("collapsed");
    editorPane.classList.remove("hidden");
    pdfPane.classList.add("collapsed");
    resizeSidebar.classList.remove("hidden");
    resizePdf.classList.add("hidden");
  } else if (mode === "split") {
    sidebar.classList.remove("collapsed");
    editorPane.classList.remove("hidden");
    pdfPane.classList.remove("collapsed");
    resizeSidebar.classList.remove("hidden");
    resizePdf.classList.remove("hidden");
  } else if (mode === "pdf") {
    sidebar.classList.add("collapsed");
    editorPane.classList.add("hidden");
    pdfPane.classList.remove("collapsed");
    resizeSidebar.classList.add("hidden");
    resizePdf.classList.add("hidden");
  }

  if (btnSidebarToggle) {
    btnSidebarToggle.disabled = (mode === "pdf");
    btnSidebarToggle.style.opacity = (mode === "pdf") ? "0.4" : "";
  }

  document.querySelectorAll(".layout-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.layout === mode);
  });

  localStorage.setItem("tinyleaf-layout", mode);
  S.layoutMode = mode;
}

function toggleSidebar() {
  if (S.layoutMode === "pdf") return;
  const sidebar = document.getElementById("sidebar");
  const isCollapsed = sidebar.classList.toggle("collapsed");
  localStorage.setItem("tinyleaf-sidebar-collapsed", isCollapsed ? "1" : "0");
}

function clearLog() {
  document.getElementById("log-content").innerHTML = "";
  document.getElementById("log-status").innerHTML = "";
}

/**
 * Normalize a path from the compile log to a project-relative path.
 * Strips leading `./` and `/workspace/` prefixes produced by Docker builds.
 * @param {string} rawPath - Path as it appears in the log.
 * @returns {string} Normalized relative path.
 */
function normalizeLogPath(rawPath) {
  if (rawPath.startsWith("/workspace/")) return rawPath.slice("/workspace/".length);
  if (rawPath.startsWith("./")) return rawPath.slice(2);
  return rawPath;
}

/**
 * Build an HTML string for a log line, turning recognized `filename:line:`
 * references into clickable `.log-link` spans. Non-matching text is HTML-escaped
 * so that characters like `<`, `>`, `&` render safely.
 *
 * Only references whose resolved path exists in `S.files` are linkified;
 * unrecognized paths fall through as plain escaped text.
 *
 * @param {string} line - Raw log line text.
 * @returns {string} HTML string safe to set as innerHTML.
 */
function buildLogLineHTML(line) {
  // Matches -file-line-error format: ./path/file.tex:42: or /workspace/path/file.tex:42:
  // Character set covers typical LaTeX file paths (alphanumeric, slashes, dots, hyphens, underscores).
  const re = /((?:\.\/|\/workspace\/)?[-\w./]+\.(?:tex|sty|bib|cls|bbl)):(\d+):/g;
  let result = "";
  let lastIndex = 0;
  let match;
  while ((match = re.exec(line)) !== null) {
    const [full, rawPath, lineStr] = match;
    const normalizedPath = normalizeLogPath(rawPath);
    // Only linkify if the file is known in the current project
    if (S.files && S.files.includes(normalizedPath)) {
      // Escape and append the text segment before this match
      result += escapeHtml(line.slice(lastIndex, match.index));
      // Build the clickable span; store normalized path and line number as data attrs
      const safeFile = escapeHtml(normalizedPath);
      result += `<span class="log-link" data-file="${safeFile}" data-line="${lineStr}">${escapeHtml(full)}</span>`;
      lastIndex = match.index + full.length;
    }
  }
  // Append any remaining text after the last match
  result += escapeHtml(line.slice(lastIndex));
  return result;
}

function appendLog(line, level = "info") {
  const el = document.getElementById("log-content");
  const div = document.createElement("div");
  div.className = "log-line " + level;
  // Use innerHTML so that log-link spans are rendered; textContent on the div
  // still returns the full plain text (used by copyLog).
  div.innerHTML = buildLogLineHTML(line);
  el.appendChild(div);
  el.scrollTop = el.scrollHeight;
}
function copyLog() {
  const el = document.getElementById("log-content");
  const text = [...el.querySelectorAll(".log-line")].map((l) => l.textContent).join("\n");
  navigator.clipboard.writeText(text).then(() => setStatus(t("log_copied"), "success"));
}

/**
 * Set up event delegation on the compile log panel for `.log-link` clicks.
 * Delegates to openFileAtLine so the referenced file is opened and scrolled to.
 */
function setupLogClickHandler() {
  document.getElementById("log-content").addEventListener("click", (e) => {
    const link = e.target.closest(".log-link");
    if (!link) return;
    const file = link.dataset.file;
    const line = parseInt(link.dataset.line, 10);
    if (file && line) openFileAtLine(file, line);
  });
}

// ══════════════════════════════════════════
// Sidebar Tab Switching
// ══════════════════════════════════════════
function switchSidebarTab(tabName) {
  document.querySelectorAll(".sidebar-tab").forEach((t) => t.classList.toggle("active", t.dataset.tab === tabName));
  document.getElementById("sidebar-files").style.display = tabName === "files" ? "flex" : "none";
  document.getElementById("sidebar-git").style.display = tabName === "git" ? "flex" : "none";
  document.getElementById("sidebar-search").style.display = tabName === "search" ? "flex" : "none";
  document.getElementById("sidebar-outline").style.display = tabName === "outline" ? "flex" : "none";
  if (tabName === "git") refreshGit();
  if (tabName === "search") document.getElementById("project-search-input").focus();
  if (tabName === "outline") renderOutline();
}

// ══════════════════════════════════════════
// Project Search
// ══════════════════════════════════════════
let _searchTimer = null;

function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

async function projectSearch(query) {
  const statusEl = document.getElementById("search-status");
  const resultsEl = document.getElementById("search-results");
  if (!query || !query.trim()) {
    statusEl.textContent = "";
    resultsEl.innerHTML = "";
    return;
  }
  const caseSensitive = document.getElementById("search-case-cb").checked;
  statusEl.textContent = "…";
  try {
    const data = await api("GET",
      `/api/projects/${enc(S.projectName)}/search?q=${encodeURIComponent(query)}&case=${caseSensitive ? 1 : 0}`);
    renderSearchResults(data, query, caseSensitive);
  } catch (err) {
    statusEl.textContent = err.message;
    resultsEl.innerHTML = "";
  }
}

function renderSearchResults(data, query, caseSensitive) {
  const statusEl = document.getElementById("search-status");
  const resultsEl = document.getElementById("search-results");
  const files = Object.keys(data.results);
  if (data.total === 0) {
    statusEl.textContent = t("no_results");
    resultsEl.innerHTML = "";
    return;
  }
  let summary = t("search_summary").replace("{n}", data.total).replace("{f}", files.length);
  if (data.truncated) summary += " — " + t("results_truncated").replace("{n}", 500);
  statusEl.textContent = summary;

  const flags = caseSensitive ? "g" : "gi";
  const highlightRe = new RegExp(query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), flags);

  let html = "";
  for (const file of files) {
    const matches = data.results[file];
    html += `<div class="search-file-group">`;
    html += `<div class="search-file-header" data-toggle>`;
    html += `<span>${escapeHtml(file)}</span><span class="match-count">${matches.length}</span></div>`;
    html += `<div>`;
    for (const m of matches) {
      const safe = escapeHtml(m.text).replace(highlightRe, s => `<mark>${s}</mark>`);
      html += `<div class="search-match" data-file="${escapeHtml(file)}" data-line="${m.line}">`;
      html += `<span class="line-num">${m.line}</span><span class="line-text">${safe}</span></div>`;
    }
    html += `</div></div>`;
  }
  resultsEl.innerHTML = html;
}

async function openFileAtLine(filePath, lineNum) {
  if (filePath !== S.currentFile) await openFile(filePath);
  if (S.editorView) {
    const line = S.editorView.state.doc.line(Math.min(lineNum, S.editorView.state.doc.lines));
    S.editorView.dispatch({
      selection: { anchor: line.from },
      effects: EditorView.scrollIntoView(line.from, { y: "center" })
    });
    S.editorView.focus();
  }
}

// ══════════════════════════════════════════
// LaTeX Outline
// ══════════════════════════════════════════

/**
 * Indent levels for LaTeX sectioning commands.
 * Lower number = higher in hierarchy.
 * @type {Object<string, number>}
 */
const OUTLINE_LEVELS = {
  part: 0,
  chapter: 1,
  section: 2,
  subsection: 3,
  subsubsection: 4,
  paragraph: 5,
  subparagraph: 6,
};

/**
 * Parse LaTeX content and extract sectioning commands and \input{}/\include{} directives.
 *
 * @param {string} content - Raw LaTeX source text.
 * @param {string} sourceFile - Project-relative path of the file being parsed.
 * @returns {Array<{kind: "section"|"input", level?: number, title?: string, line: number, file: string, path?: string}>}
 *   Ordered list of sectioning entries and include directives.
 */
function parseOutline(content, sourceFile) {
  const items = [];
  // Sectioning regex: optional star, command name, optional title argument.
  // Handles \section{title}, \section*{title}, \section[short]{title}
  const sectionRe = /^\s*\\(part|chapter|section|subsection|subsubsection|paragraph|subparagraph)\*?\s*(?:\[[^\]]*\])?\{([^}]*)\}/;
  // \input{path} / \include{path} / \subfile{path}
  const inputRe = /^\s*\\(input|include|subfile)\{([^}]+)\}/;
  const lines = content.split("\n");
  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    // Skip fully-commented lines (% not preceded by \)
    const stripped = raw.replace(/^(\s*)/, "");
    if (stripped.startsWith("%")) continue;
    // Remove inline comments before matching
    const noComment = raw.replace(/(?<!\\)%.*$/, "");
    const sm = noComment.match(sectionRe);
    if (sm) {
      const cmd = sm[1];
      const title = sm[2].trim();
      items.push({ kind: "section", level: OUTLINE_LEVELS[cmd], title, line: i + 1, file: sourceFile });
      continue;
    }
    const im = noComment.match(inputRe);
    if (im) {
      items.push({ kind: "input", path: im[2].trim(), line: i + 1, file: sourceFile });
    }
  }
  return items;
}

/**
 * Resolve a LaTeX \input{} path relative to the file that contains the directive.
 * Adds a `.tex` extension when missing and normalizes `./` and `../` segments.
 *
 * @param {string} rawPath - Argument of \input / \include / \subfile.
 * @param {string} sourceFile - Project-relative path of the file containing the directive.
 * @returns {string} Project-relative resolved path.
 */
function resolveInputPath(rawPath, sourceFile) {
  let p = rawPath.trim();
  if (!/\.[a-zA-Z]+$/.test(p)) p += ".tex";
  // Strip leading ./
  p = p.replace(/^\.\//, "");
  // If absolute-ish (starts with /), drop the leading slash and treat as project root
  if (p.startsWith("/")) return p.replace(/^\/+/, "");
  // Resolve relative to sourceFile's directory
  const dir = sourceFile.includes("/") ? sourceFile.slice(0, sourceFile.lastIndexOf("/")) : "";
  const parts = (dir ? dir.split("/") : []).concat(p.split("/"));
  const out = [];
  for (const seg of parts) {
    if (seg === "" || seg === ".") continue;
    if (seg === "..") { out.pop(); continue; }
    out.push(seg);
  }
  return out.join("/");
}

/**
 * Recursively expand an outline by following \input{} / \include{} directives.
 *
 * @param {string} rootFile - Project-relative path of the starting file.
 * @param {string} rootContent - Source of the starting file.
 * @param {Set<string>} seen - Files already visited (cycle guard, mutated).
 * @param {number} depth - Current recursion depth (capped at 6 to avoid runaway).
 * @returns {Promise<Array<{level: number, title: string, line: number, file: string}>>}
 */
async function expandOutline(rootFile, rootContent, seen, depth) {
  if (depth > 6) return [];
  if (seen.has(rootFile)) return [];
  seen.add(rootFile);
  const result = [];
  const items = parseOutline(rootContent, rootFile);
  for (const it of items) {
    if (it.kind === "section") {
      result.push({ level: it.level, title: it.title, line: it.line, file: it.file });
    } else if (it.kind === "input") {
      const resolved = resolveInputPath(it.path, rootFile);
      // Only follow inputs that exist in the project file list (avoid 404 noise).
      if (!S.files || !S.files.includes(resolved)) continue;
      try {
        const data = await api("GET", `/api/projects/${enc(S.projectName)}/files/${enc(resolved)}`);
        const sub = await expandOutline(resolved, data.content, seen, depth + 1);
        for (const s of sub) result.push(s);
      } catch {
        // Skip files that fail to load
      }
    }
  }
  return result;
}

/**
 * Render the outline tree for the currently open file.
 * Reads content from the live editor if available, otherwise fetches from API.
 */
async function renderOutline() {
  const statusEl = document.getElementById("outline-status");
  const treeEl = document.getElementById("outline-tree");

  if (!S.currentFile || !S.projectName) {
    statusEl.textContent = t("outline_no_file");
    treeEl.innerHTML = "";
    return;
  }
  if (!S.currentFile.endsWith(".tex")) {
    statusEl.textContent = t("outline_no_file");
    treeEl.innerHTML = "";
    return;
  }

  // Prefer the project's main file as the outline root so the full document
  // structure stays visible no matter which included file the user is editing
  // (matches Overleaf behaviour). Fall back to the current file otherwise.
  const rootFile = (S.mainFile && S.files && S.files.includes(S.mainFile))
    ? S.mainFile
    : S.currentFile;

  let rootContent;
  if (rootFile === S.currentFile && S.editorView) {
    // Live buffer for the file in the editor — reflects unsaved edits.
    rootContent = S.editorView.state.doc.toString();
  } else {
    try {
      const data = await api("GET", `/api/projects/${enc(S.projectName)}/files/${enc(rootFile)}`);
      rootContent = data.content;
    } catch (err) {
      statusEl.textContent = err.message;
      treeEl.innerHTML = "";
      return;
    }
  }

  // Expand \input{}/\include{} recursively so the outline reflects the
  // whole document, not just the file currently in the editor.
  const items = await expandOutline(rootFile, rootContent, new Set(), 0);
  if (items.length === 0) {
    statusEl.textContent = t("outline_no_sections");
    treeEl.innerHTML = "";
    return;
  }

  statusEl.textContent = "";

  // Compute indent relative to the minimum level present so shallow trees
  // (e.g., only \section and \subsection) still start at indent 0.
  const minLevel = items.reduce((m, it) => Math.min(m, it.level), Infinity);
  const INDENT_PX = 14;

  let html = "";
  for (const item of items) {
    const indent = (item.level - minLevel) * INDENT_PX;
    const fileAttr = escapeHtml(item.file);
    // Only show a file tag when the section comes from a different file than
    // the one currently being edited — keeps the outline visually clean.
    const fileTag = item.file === S.currentFile
      ? ""
      : `<span class="outline-filetag">${escapeHtml(item.file.split("/").pop())}</span>`;
    html += `<div class="outline-item" data-line="${item.line}" data-file="${fileAttr}" style="padding-left:${10 + indent}px" title="${escapeHtml(item.title)} (${escapeHtml(item.file)}:${item.line})">`;
    html += `<span class="outline-label">${escapeHtml(item.title)}</span>`;
    html += fileTag;
    html += `<span class="outline-linenum">${item.line}</span>`;
    html += `</div>`;
  }
  treeEl.innerHTML = html;

  // Attach click handlers — navigate cross-file when needed.
  treeEl.querySelectorAll(".outline-item").forEach((el) => {
    el.onclick = async () => {
      const lineNum = parseInt(el.dataset.line, 10);
      const filePath = el.dataset.file;
      if (filePath && filePath !== S.currentFile) {
        await openFile(filePath);
      }
      jumpToOutlineLine(lineNum);
    };
  });

  // Highlight the section containing the current cursor
  highlightOutlineActive();
}

/**
 * Jump the editor to the given 1-based line number in the current file.
 *
 * @param {number} lineNum - 1-based line number to scroll to.
 */
function jumpToOutlineLine(lineNum) {
  if (!S.editorView) return;
  const totalLines = S.editorView.state.doc.lines;
  const clampedLine = Math.min(Math.max(lineNum, 1), totalLines);
  const line = S.editorView.state.doc.line(clampedLine);
  S.editorView.dispatch({
    selection: { anchor: line.from },
    effects: EditorView.scrollIntoView(line.from, { y: "center" }),
  });
  S.editorView.focus();
  highlightOutlineActive();
}

/**
 * Mark the outline item whose section the editor cursor is currently inside.
 * The active item is the last one whose line number is ≤ the cursor line.
 */
function highlightOutlineActive() {
  if (!S.editorView) return;
  const cursorLine = S.editorView.state.doc.lineAt(
    S.editorView.state.selection.main.head
  ).number;
  const items = document.querySelectorAll("#outline-tree .outline-item");
  let activeEl = null;
  items.forEach((el) => {
    el.classList.remove("active");
    // Only items from the currently open file are candidates for cursor-based highlight.
    if (el.dataset.file && el.dataset.file !== S.currentFile) return;
    const ln = parseInt(el.dataset.line, 10);
    if (ln <= cursorLine) activeEl = el;
  });
  if (activeEl) activeEl.classList.add("active");
}

/** Debounce timer for outline refresh triggered by editor changes. */
let _outlineRefreshTimer = null;

/**
 * Schedule a deferred outline refresh (debounced at 500 ms).
 * Called on document edits so the outline stays in sync without live-parsing on every keystroke.
 */
function scheduleOutlineRefresh() {
  if (document.getElementById("sidebar-outline").style.display === "none") return;
  clearTimeout(_outlineRefreshTimer);
  _outlineRefreshTimer = setTimeout(() => renderOutline(), 500);
}

// ══════════════════════════════════════════
// Git
// ══════════════════════════════════════════
async function refreshGit() {
  try {
    const st = await api("GET", `/api/projects/${enc(S.projectName)}/git/status`);
    if (!st.git) { return; }
    document.getElementById("git-branch").textContent =
      `${st.branch || "???"}` +
      (st.ahead ? ` \u2191${st.ahead}` : "") +
      (st.behind ? ` \u2193${st.behind}` : "");

    S.gitFiles = st.files || [];
    const fd = document.getElementById("git-files");
    // Legacy diff view (sidebar widget) — keep hidden
    const legacyDiffView = document.getElementById("git-diff-view");
    fd.innerHTML = "";
    legacyDiffView.style.display = "none";
    legacyDiffView.innerHTML = "";

    if (S.gitFiles.length === 0) {
      fd.innerHTML = `<div style="padding:6px 14px;font-size:12px;color:var(--text-dim)">${t("no_changes")}</div>`;
      return;
    }

    for (const f of S.gitFiles) {
      const cls = f.status === "??" ? "U" : f.status.includes("D") ? "D" : f.status.includes("A") ? "A" : "M";
      const div = document.createElement("div");
      div.className = "git-file";
      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.checked = true;
      cb.dataset.path = f.path;
      div.appendChild(cb);
      const statusSpan = document.createElement("span");
      statusSpan.className = `git-status ${cls}`;
      statusSpan.textContent = cls;
      div.appendChild(statusSpan);
      const nameSpan = document.createElement("span");
      nameSpan.className = "git-file-name";
      nameSpan.textContent = f.path;
      nameSpan.title = f.path;
      div.appendChild(nameSpan);
      nameSpan.onclick = () => showGitDiff(f.path, div);
      fd.appendChild(div);
    }
  } catch { /* git not available */ }
}

// ── Diff pane helpers ──

/** Open the diff pane in the editor area, hiding the editor container. */
function _openDiffPane() {
  document.getElementById("editor-container").style.display = "none";
  document.getElementById("diff-pane").classList.add("open");
}

/** Close the diff pane and restore the editor container. */
function closeDiffPane() {
  document.getElementById("diff-pane").classList.remove("open");
  document.getElementById("editor-container").style.display = "";
  document.querySelectorAll("#git-files .git-file").forEach((el) => el.classList.remove("active"));
  S._diffFilePath = null;
  // Ask CodeMirror to re-measure layout after the container becomes visible.
  if (S.editorView) S.editorView.requestMeasure();
}

/**
 * Render a unified-diff string into a table with old/new line numbers.
 *
 * @param {string} diffText  Raw unified diff text.
 * @param {HTMLElement} container  Element to append rendered rows into.
 */
function _renderDiffText(diffText, container) {
  if (!diffText || !diffText.trim()) return false;

  const table = document.createElement("table");
  table.className = "diff-table";

  const colgroup = document.createElement("colgroup");
  colgroup.innerHTML = '<col class="ln-old"><col class="ln-new"><col class="code">';
  table.appendChild(colgroup);

  const tbody = document.createElement("tbody");
  table.appendChild(tbody);

  const hunkRe = /^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@/;
  let oldLine = 0, newLine = 0;
  let hasContent = false;

  for (const rawLine of diffText.split("\n")) {
    // Skip diff file headers (--- a/... +++ b/...)
    if (rawLine.startsWith("--- ") || rawLine.startsWith("+++ ")) continue;
    if (rawLine.startsWith("diff --git") || rawLine.startsWith("index ")) continue;
    if (rawLine.startsWith("new file mode") || rawLine.startsWith("deleted file mode")) continue;

    const tr = document.createElement("tr");
    const tdOld = document.createElement("td");
    tdOld.className = "diff-ln";
    const tdNew = document.createElement("td");
    tdNew.className = "diff-ln";
    const tdCode = document.createElement("td");
    tdCode.className = "diff-code";

    const hunkMatch = rawLine.match(hunkRe);
    if (hunkMatch) {
      oldLine = parseInt(hunkMatch[1], 10);
      newLine = parseInt(hunkMatch[2], 10);
      tr.className = "diff-row-hunk";
      tdOld.textContent = "";
      tdNew.textContent = "";
      tdCode.textContent = rawLine;
      hasContent = true;
    } else if (rawLine.startsWith("+")) {
      tr.className = "diff-row-add";
      tdOld.textContent = "";
      tdNew.textContent = newLine++;
      tdCode.textContent = rawLine;
      hasContent = true;
    } else if (rawLine.startsWith("-")) {
      tr.className = "diff-row-del";
      tdOld.textContent = oldLine++;
      tdNew.textContent = "";
      tdCode.textContent = rawLine;
      hasContent = true;
    } else {
      tr.className = "diff-row-ctx";
      tdOld.textContent = oldLine > 0 ? oldLine++ : "";
      tdNew.textContent = newLine > 0 ? newLine++ : "";
      tdCode.textContent = rawLine;
    }

    tr.appendChild(tdOld);
    tr.appendChild(tdNew);
    tr.appendChild(tdCode);
    tbody.appendChild(tr);
  }

  if (hasContent) container.appendChild(table);
  return hasContent;
}

async function showGitDiff(filePath, activeEl) {
  document.querySelectorAll("#git-files .git-file").forEach((el) => el.classList.remove("active"));
  if (activeEl) activeEl.classList.add("active");

  S._diffFilePath = filePath;
  document.getElementById("diff-title").textContent = filePath;

  const content = document.getElementById("diff-content");
  content.innerHTML = `<div class="diff-no-changes" style="color:var(--text-dim)">${t("loading")}…</div>`;
  _openDiffPane();

  try {
    const resp = await fetch(
      `/api/projects/${enc(S.projectName)}/git/diff/${enc(filePath)}?format=json`
    );
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();

    content.innerHTML = "";

    const hasBoth = data.staged && data.unstaged;
    const hasAny = (data.staged && data.staged.trim()) || (data.unstaged && data.unstaged.trim());

    if (!hasAny) {
      content.innerHTML = `<div class="diff-no-changes">${t("diff_no_changes")}</div>`;
      return;
    }

    // Render unstaged section.
    if (data.unstaged && data.unstaged.trim()) {
      if (hasBoth) {
        const hdr = document.createElement("div");
        hdr.className = "diff-section-header";
        hdr.textContent = t("diff_unstaged");
        content.appendChild(hdr);
      }
      _renderDiffText(data.unstaged, content);
    }

    // Render staged section.
    if (data.staged && data.staged.trim()) {
      if (hasBoth) {
        const hdr = document.createElement("div");
        hdr.className = "diff-section-header";
        hdr.textContent = t("diff_staged");
        content.appendChild(hdr);
      }
      _renderDiffText(data.staged, content);
    }

    // Handle pseudo-diff for untracked files: only the unstaged section.
    // If nothing rendered at all (e.g. truly empty), show friendly message.
    if (!content.querySelector("table, .diff-no-changes")) {
      content.innerHTML = `<div class="diff-no-changes">${t("diff_no_changes")}</div>`;
    }
  } catch {
    content.innerHTML = `<div class="diff-no-changes" style="color:var(--red)">Failed to load diff</div>`;
  }
}

async function doCommit() {
  const checkboxes = document.querySelectorAll("#git-files input[type=checkbox]");
  const selectedFiles = [...checkboxes].filter((cb) => cb.checked).map((cb) => cb.dataset.path);

  if (S.gitFiles && S.gitFiles.length > 0 && selectedFiles.length === 0) {
    setStatus(t("no_files_selected"), "warning");
    return;
  }

  const msgEl = document.getElementById("git-commit-msg");
  const msg = msgEl ? msgEl.value.trim() : "";
  if (!msg) {
    // Switch to git tab and focus the textarea
    switchSidebarTab("git");
    setTimeout(() => { msgEl?.focus(); }, 50);
    setStatus(t("commit_message"), "warning");
    return;
  }

  if (S.modified.has(S.currentFile)) await saveCurrentFile();
  const r = await api("POST", `/api/projects/${enc(S.projectName)}/git/commit`, {
    message: msg,
    files: selectedFiles.length ? selectedFiles : null,
  });
  setStatus(r.success ? t("committed") : r.message, r.success ? "success" : "error");
  if (r.success && msgEl) msgEl.value = "";
  refreshGit();
}

async function doPush() {
  setStatus(t("pushing"));
  const r = await api("POST", `/api/projects/${enc(S.projectName)}/git/push`);
  setStatus(r.success ? t("pushed") : r.message, r.success ? "success" : "error");
  refreshGit();
}

// ══════════════════════════════════════════
// New File / Folder (root level)
// ══════════════════════════════════════════
function showNewFileModal() {
  showNewFileInDirModal("");
}

function showNewFolderModal() {
  showNewFolderInDirModal("");
}

// ══════════════════════════════════════════
// Modal
// ══════════════════════════════════════════
function showModal(title, bodyHtml, buttons) {
  document.getElementById("modal-title").textContent = title;
  document.getElementById("modal-body").innerHTML = bodyHtml;
  const actions = document.getElementById("modal-actions");
  actions.innerHTML = "";
  for (const b of buttons) {
    const btn = document.createElement("button");
    btn.textContent = b.label;
    if (b.primary) btn.className = "primary";
    btn.onclick = b.action;
    actions.appendChild(btn);
  }
  const overlay = document.getElementById("modal-overlay");
  overlay.style.display = "flex";
  overlay.onclick = (e) => { if (e.target === overlay) closeModal(); };
}

function closeModal() { document.getElementById("modal-overlay").style.display = "none"; }

// ══════════════════════════════════════════
// Keyboard Shortcuts
// ══════════════════════════════════════════

const isMac = /Mac|iPhone|iPad|iPod/.test(navigator.platform);
const MOD = isMac ? "⌘" : "Ctrl";

function showShortcutsPopup() {
  const groups = [
    { title: t("shortcut_editing"), shortcuts: [
      { keys: [MOD, "S"], desc: t("sc_save") },
      { keys: [MOD, "F"], desc: t("sc_find") },
      { keys: [MOD, "H"], desc: t("sc_replace") },
    ]},
    { title: t("shortcut_compile"), shortcuts: [
      { keys: [MOD, "Enter"], desc: t("sc_compile") },
      { keys: [MOD, "`"],     desc: t("sc_toggle_log") },
    ]},
    { title: t("shortcut_navigation"), shortcuts: [
      { keys: [MOD, "P"],          desc: t("sc_quick_open") },
      { keys: [MOD, "B"],          desc: t("sc_toggle_sidebar") },
      { keys: [MOD, "Shift", "E"], desc: t("sc_files_tab") },
      { keys: [MOD, "Shift", "G"], desc: t("sc_git_tab") },
      { keys: [MOD, "Shift", "F"], desc: t("sc_search_tab") },
      { keys: [MOD, "Shift", "O"], desc: t("sc_outline_tab") },
      { keys: [MOD, "Tab"],          desc: t("sc_next_tab") },
      { keys: [MOD, "Shift", "Tab"], desc: t("sc_prev_tab") },
      { keys: [MOD, "W"],            desc: t("sc_close_tab") },
    ]},
    { title: t("shortcut_git"), shortcuts: [
      { keys: [MOD, "Shift", "Alt", "C"], desc: t("sc_commit") },
      { keys: [MOD, "Shift", "Alt", "P"], desc: t("sc_push") },
    ]},
    { title: t("shortcut_pdf"), shortcuts: [
      { keys: [MOD, "Click"], desc: t("sc_synctex") },
      { keys: [MOD, "Shift", "Enter"], desc: t("sc_forward_search") },
      { keys: [MOD, "F"], desc: t("sc_pdf_search") },
    ]},
    { title: t("shortcut_layout"), shortcuts: [
      { keys: [MOD, "Shift", "1"], desc: t("sc_layout_editor") },
      { keys: [MOD, "Shift", "2"], desc: t("sc_layout_split") },
      { keys: [MOD, "Shift", "3"], desc: t("sc_layout_pdf") },
    ]},
    { title: t("shortcut_general"), shortcuts: [
      { keys: [MOD, "/"], desc: t("sc_shortcuts") },
      { keys: ["Esc"], desc: t("sc_close") },
    ]},
  ];

  const container = document.getElementById("shortcuts-content");
  container.innerHTML = groups.map(g => `
    <div class="shortcut-group">
      <div class="shortcut-group-title">${g.title}</div>
      ${g.shortcuts.map(s => `
        <div class="shortcut-row">
          <span class="shortcut-desc">${s.desc}</span>
          <span class="shortcut-keys">${s.keys.map(k => `<kbd>${k}</kbd>`).join('<span>+</span>')}</span>
        </div>
      `).join("")}
    </div>
  `).join("");

  document.getElementById("shortcuts-popup").classList.add("open");
}

// ══════════════════════════════════════════
// Word Count
// ══════════════════════════════════════════
async function showWordCount() {
  if (!S.projectName) return;

  const container = document.getElementById("wordcount-content");
  container.innerHTML = `<div style="text-align:center;padding:16px;color:var(--text-dim)">${t("wc_loading")}</div>`;
  document.getElementById("wordcount-popup").classList.add("open");

  try {
    const stats = await api("GET", `/api/projects/${enc(S.projectName)}/wordcount`);
    const rows = [
      { label: t("wc_words_in_text"), value: stats.words_in_text },
      { label: t("wc_words_in_headers"), value: stats.words_in_headers },
      { label: t("wc_words_outside_text"), value: stats.words_outside_text },
      { label: t("wc_words_in_captions"), value: stats.words_in_captions },
      { label: t("wc_math_inline"), value: stats.math_inline },
      { label: t("wc_math_display"), value: stats.math_display },
    ];
    container.innerHTML = rows.map(r => `
      <div class="wordcount-row">
        <span class="wc-label">${r.label}</span>
        <span class="wc-value">${r.value.toLocaleString()}</span>
      </div>
    `).join("") + `
      <div class="wordcount-row wc-total">
        <span class="wc-label">${t("wc_total")}</span>
        <span class="wc-value">${stats.total.toLocaleString()}</span>
      </div>
    `;
  } catch (err) {
    container.innerHTML = `<div style="text-align:center;padding:16px;color:var(--red)">${t("wc_error")}: ${esc(err.message)}</div>`;
  }
}

// ══════════════════════════════════════════
// Quick Open (Ctrl+P fuzzy file switcher)
// ══════════════════════════════════════════
const QO = {
  matches: [],     // [{path, indices, score}]
  active: 0,       // active row index
  maxResults: 50,
};

/**
 * Score a path against a query using subsequence fuzzy match.
 *
 * Returns null when the query is not a subsequence of the path; otherwise
 * an object {indices, score}. Higher scores rank earlier.
 */
function quickOpenScore(query, path) {
  if (!query) return { indices: [], score: 0 };
  const q = query.toLowerCase();
  const p = path.toLowerCase();
  const indices = [];
  let qi = 0;
  let score = 0;
  let lastMatchPos = -2;
  let consecutive = 0;
  const basenameStart = path.lastIndexOf("/") + 1;
  for (let i = 0; i < p.length && qi < q.length; i++) {
    if (p[i] === q[qi]) {
      indices.push(i);
      let bonus = 1;
      const prevCh = i > 0 ? p[i - 1] : "/";
      if (prevCh === "/") bonus += 25;
      else if (prevCh === "_" || prevCh === "-" || prevCh === "." || prevCh === " ") bonus += 10;
      if (i >= basenameStart) bonus += 6;
      if (lastMatchPos === i - 1) {
        consecutive++;
        bonus += 15 * consecutive;
      } else {
        consecutive = 0;
      }
      score += bonus;
      lastMatchPos = i;
      qi++;
    }
  }
  if (qi < q.length) return null;
  // Shorter paths win on ties
  score -= path.length * 0.1;
  return { indices, score };
}

function quickOpenFilter(query) {
  const files = S.files || [];
  const trimmed = query.trim();
  if (!trimmed) {
    // Empty query: tabs first (recent), then all files alphabetically
    const tabSet = new Set(S.tabs || []);
    const head = (S.tabs || []).slice();
    const tail = files.filter((f) => !tabSet.has(f)).sort();
    return [...head, ...tail].slice(0, QO.maxResults).map((path) => ({
      path,
      indices: [],
      score: 0,
    }));
  }
  const scored = [];
  for (const path of files) {
    const r = quickOpenScore(trimmed, path);
    if (r) scored.push({ path, indices: r.indices, score: r.score });
  }
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, QO.maxResults);
}

function _qoEscape(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function _qoHighlight(text, indices, offset = 0) {
  if (!indices.length) return _qoEscape(text);
  const set = new Set(indices.map((i) => i - offset));
  let out = "";
  for (let i = 0; i < text.length; i++) {
    const ch = _qoEscape(text[i]);
    out += set.has(i) ? `<span class="qo-match">${ch}</span>` : ch;
  }
  return out;
}

function renderQuickOpenResults() {
  const container = document.getElementById("quick-open-results");
  if (!QO.matches.length) {
    container.innerHTML = `<div class="qo-empty">${t("quick_open_no_results")}</div>`;
    return;
  }
  if (QO.active >= QO.matches.length) QO.active = QO.matches.length - 1;
  if (QO.active < 0) QO.active = 0;
  const html = QO.matches.map((m, idx) => {
    const slash = m.path.lastIndexOf("/");
    const name = slash >= 0 ? m.path.slice(slash + 1) : m.path;
    const dir = slash >= 0 ? m.path.slice(0, slash + 1) : "";
    const nameHtml = _qoHighlight(name, m.indices, slash + 1);
    const dirHtml = dir ? _qoHighlight(dir, m.indices, 0) : "";
    return `<div class="qo-row${idx === QO.active ? " active" : ""}" data-idx="${idx}" data-path="${_qoEscape(m.path)}">
      <span class="qo-name">${nameHtml}</span>
      <span class="qo-dir">${dirHtml}</span>
    </div>`;
  }).join("");
  container.innerHTML = html;
  const activeEl = container.querySelector(".qo-row.active");
  if (activeEl) activeEl.scrollIntoView({ block: "nearest" });
}

function quickOpenUpdate(query) {
  QO.matches = quickOpenFilter(query);
  QO.active = 0;
  renderQuickOpenResults();
}

function openQuickOpen() {
  if (!S.projectName) return;
  const overlay = document.getElementById("quick-open-overlay");
  const input = document.getElementById("quick-open-input");
  input.placeholder = t("quick_open_placeholder");
  input.value = "";
  overlay.classList.add("open");
  quickOpenUpdate("");
  // Focus after the overlay becomes visible
  setTimeout(() => input.focus(), 0);
}

function closeQuickOpen() {
  const overlay = document.getElementById("quick-open-overlay");
  if (!overlay.classList.contains("open")) return;
  overlay.classList.remove("open");
  document.getElementById("quick-open-input").blur();
}

function quickOpenPick(idx) {
  if (idx < 0 || idx >= QO.matches.length) return;
  const path = QO.matches[idx].path;
  closeQuickOpen();
  openFile(path);
}

function setupQuickOpen() {
  const overlay = document.getElementById("quick-open-overlay");
  const input = document.getElementById("quick-open-input");
  const results = document.getElementById("quick-open-results");

  input.addEventListener("input", () => quickOpenUpdate(input.value));

  input.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      QO.active = Math.min(QO.active + 1, QO.matches.length - 1);
      renderQuickOpenResults();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      QO.active = Math.max(QO.active - 1, 0);
      renderQuickOpenResults();
    } else if (e.key === "Enter") {
      e.preventDefault();
      quickOpenPick(QO.active);
    } else if (e.key === "Escape") {
      e.preventDefault();
      closeQuickOpen();
    }
  });

  results.addEventListener("click", (e) => {
    const row = e.target.closest(".qo-row");
    if (!row) return;
    quickOpenPick(parseInt(row.dataset.idx, 10));
  });

  results.addEventListener("mousemove", (e) => {
    const row = e.target.closest(".qo-row");
    if (!row) return;
    const idx = parseInt(row.dataset.idx, 10);
    if (idx !== QO.active) {
      QO.active = idx;
      renderQuickOpenResults();
    }
  });

  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) closeQuickOpen();
  });
}

function setupKeybindings() {
  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "s") { e.preventDefault(); saveCurrentFile(); }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "Enter") { e.preventDefault(); syncTexForwardSearch(); }
    if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key === "Enter") { e.preventDefault(); compile(); }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "E") { e.preventDefault(); switchSidebarTab("files"); }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "G") { e.preventDefault(); switchSidebarTab("git"); }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "F") { e.preventDefault(); switchSidebarTab("search"); }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "O") { e.preventDefault(); switchSidebarTab("outline"); }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.altKey && e.key === "C") { e.preventDefault(); doCommit(); }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.altKey && e.key === "P") { e.preventDefault(); doPush(); }
    if ((e.ctrlKey || e.metaKey) && e.key === "/") { e.preventDefault(); showShortcutsPopup(); }
    if ((e.ctrlKey || e.metaKey) && e.key === "`") { e.preventDefault(); toggleLog(); }
    if ((e.ctrlKey || e.metaKey) && !e.shiftKey && !e.altKey && e.key === "b") { e.preventDefault(); toggleSidebar(); }
    // Ctrl+H: prevent browser history and open CM search/replace panel
    if ((e.ctrlKey || e.metaKey) && !e.shiftKey && !e.altKey && e.key === "h") {
      e.preventDefault();
      if (S.editorView) openSearchPanel(S.editorView);
    }
    if ((e.ctrlKey || e.metaKey) && !e.shiftKey && !e.altKey && e.key === "p") { e.preventDefault(); openQuickOpen(); }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "1") { e.preventDefault(); setLayout("editor"); }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "2") { e.preventDefault(); setLayout("split"); }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "3") { e.preventDefault(); setLayout("pdf"); }
    if ((e.ctrlKey || e.metaKey) && !e.shiftKey && !e.altKey && e.key === "w") {
      if (S.activeTab) { e.preventDefault(); closeTab(S.activeTab); }
    }
    if (e.ctrlKey && !e.altKey && e.key === "Tab") {
      e.preventDefault();
      cycleTabs(e.shiftKey ? -1 : 1);
    }
    // Ctrl+F: open PDF search when focus is in PDF pane or PDF-only layout
    if ((e.ctrlKey || e.metaKey) && !e.shiftKey && !e.altKey && e.key === "f") {
      const pdfPane = document.getElementById("pdf-pane");
      const editorPane = document.getElementById("editor-pane");
      const inPdfPane = pdfPane && pdfPane.contains(document.activeElement);
      const pdfOnly = editorPane && editorPane.classList.contains("hidden");
      if (inPdfPane || pdfOnly) {
        e.preventDefault();
        e.stopPropagation();
        openPdfSearch();
        return;
      }
    }
    if (e.key === "Escape") { closePdfSearch(); closeModal(); closeContextMenu(); closeQuickOpen(); document.getElementById("settings-popup").classList.remove("open"); document.getElementById("shortcuts-popup").classList.remove("open"); document.getElementById("wordcount-popup").classList.remove("open"); if (document.getElementById("diff-pane").classList.contains("open")) closeDiffPane(); }
  });
}

// ══════════════════════════════════════════
// Wire up buttons
// ══════════════════════════════════════════
document.getElementById("btn-home").onclick = () => {
  if (S.mode === "multi") {
    // Flush any dirty tabs synchronously (best effort)
    for (const path of S.tabs) {
      if (S.modified.has(path)) {
        const entry = S.editors.get(path);
        if (entry && entry.view) {
          const content = entry.view.state.doc.toString();
          api("PUT", `/api/projects/${enc(S.projectName)}/files/${enc(path)}`, { content }).catch(() => {});
        }
      }
    }
    closeAllTabs();
    S.modified.clear();
    S.projectName = null;
    document.getElementById("project-name").textContent = "\u2014";
    showProjectList();
  }
};
document.getElementById("btn-compile").onclick = compile;
document.getElementById("btn-clean").onclick = doClean;
document.getElementById("btn-export-zip").onclick = () => {
  if (!S.projectName) return;
  const a = document.createElement("a");
  a.href = `/api/projects/${enc(S.projectName)}/export`;
  a.download = "";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
};
document.getElementById("btn-save").onclick = saveCurrentFile;
document.getElementById("main-file-select").onchange = (e) => {
  S.mainFile = e.target.value;
  api("PUT", `/api/projects/${enc(S.projectName)}/config`, { main_file: S.mainFile });
};
document.getElementById("auto-compile-toggle").onchange = (e) => {
  S.autoCompile = e.target.checked;
  api("PUT", `/api/projects/${enc(S.projectName)}/config`, { auto_compile: S.autoCompile });
};
document.getElementById("btn-git-commit-selected").onclick = doCommit;
document.getElementById("btn-git-push").onclick = doPush;
document.getElementById("btn-git-refresh").onclick = refreshGit;
document.getElementById("btn-diff-close").onclick = closeDiffPane;
document.getElementById("btn-diff-refresh").onclick = () => {
  if (S._diffFilePath) {
    const active = document.querySelector("#git-files .git-file.active");
    showGitDiff(S._diffFilePath, active);
  }
};
document.getElementById("tab-files").onclick = () => switchSidebarTab("files");
document.getElementById("tab-git").onclick = () => switchSidebarTab("git");
document.getElementById("tab-search").onclick = () => switchSidebarTab("search");
document.getElementById("tab-outline").onclick = () => switchSidebarTab("outline");

// Search input wiring
document.getElementById("project-search-input").addEventListener("input", (e) => {
  clearTimeout(_searchTimer);
  _searchTimer = setTimeout(() => projectSearch(e.target.value), 300);
});
document.getElementById("project-search-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") { clearTimeout(_searchTimer); projectSearch(e.target.value); }
  if (e.key === "Escape") { e.target.value = ""; document.getElementById("search-status").textContent = ""; document.getElementById("search-results").innerHTML = ""; }
});
document.getElementById("search-case-cb").addEventListener("change", () => {
  const q = document.getElementById("project-search-input").value;
  if (q) projectSearch(q);
});
document.getElementById("search-results").addEventListener("click", (e) => {
  const header = e.target.closest(".search-file-header[data-toggle]");
  if (header) { const body = header.nextElementSibling; body.style.display = body.style.display === "none" ? "" : "none"; return; }
  const match = e.target.closest(".search-match[data-file]");
  if (match) openFileAtLine(match.dataset.file, parseInt(match.dataset.line, 10));
});
document.getElementById("btn-log-toggle").onclick = toggleLog;
document.getElementById("btn-log-copy").addEventListener("click", (e) => { e.stopPropagation(); copyLog(); });
document.getElementById("btn-new-file").onclick = showNewFileModal;
document.getElementById("btn-new-folder").onclick = showNewFolderModal;
document.getElementById("btn-search-file").onclick = toggleFileSearch;
document.getElementById("btn-upload-file").onclick = () => triggerUpload("");
document.getElementById("btn-locate-file").onclick = locateInTree;
document.getElementById("btn-close-file").onclick = closeFile;
document.getElementById("btn-collapse-all").onclick = () => {
  expandedDirs.clear();
  saveExpandedDirs();
  renderFileTree();
};
document.getElementById("log-header").onclick = toggleLog;
// Layout switcher
document.querySelectorAll(".layout-btn").forEach(btn => {
  btn.addEventListener("click", () => setLayout(btn.dataset.layout));
});
document.getElementById("btn-sidebar-toggle").addEventListener("click", toggleSidebar);
document.getElementById("btn-pdf-refresh").onclick = () => {
  if (S.projectName) {
    const base = (S.currentFile || "main.tex").replace(/\.tex$/, ".pdf");
    loadPDF(`/api/projects/${enc(S.projectName)}/output/${enc(base)}`);
  }
};
document.getElementById("btn-pdf-zoom-in").onclick = () => { S.pdfZoom = Math.min(S.pdfZoom + 0.25, 5); updateZoomLabel(); renderPDF(); };
document.getElementById("btn-pdf-zoom-out").onclick = () => { S.pdfZoom = Math.max(S.pdfZoom - 0.25, 0.25); updateZoomLabel(); renderPDF(); };
document.getElementById("btn-pdf-zoom-fit").onclick = () => { S.pdfZoom = 1.0; updateZoomLabel(); renderPDF(); };
document.getElementById("btn-pdf-hd").onclick = () => {
  S.pdfRenderHD = !S.pdfRenderHD;
  document.getElementById("btn-pdf-hd").classList.toggle("active", S.pdfRenderHD);
  localStorage.setItem("tinyleaf-pdf-hd", S.pdfRenderHD ? "1" : "0");
  renderPDF();
};
// Init HD button state
S.pdfRenderHD = localStorage.getItem("tinyleaf-pdf-hd") !== "0";
document.getElementById("btn-pdf-hd").classList.toggle("active", S.pdfRenderHD);

// ── PDF page navigation ──
document.getElementById("btn-pdf-prev").onclick = () => {
  const input = document.getElementById("pdf-page-input");
  jumpToPdfPage(parseInt(input.value) - 1);
};
document.getElementById("btn-pdf-next").onclick = () => {
  const input = document.getElementById("pdf-page-input");
  jumpToPdfPage(parseInt(input.value) + 1);
};
document.getElementById("pdf-page-input").addEventListener("click", (e) => {
  e.target.select();
});
document.getElementById("pdf-page-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    jumpToPdfPage(parseInt(e.target.value) || 1);
    e.target.blur();
  }
});
document.getElementById("pdf-page-input").addEventListener("blur", (e) => {
  if (S.pdfDoc) {
    jumpToPdfPage(parseInt(e.target.value) || 1);
  }
});

// ── PDF search bar ──
document.getElementById("btn-pdf-search").onclick = openPdfSearch;
document.getElementById("btn-pdf-search-close").onclick = closePdfSearch;
document.getElementById("btn-pdf-search-prev").onclick = pdfSearchPrev;
document.getElementById("btn-pdf-search-next").onclick = pdfSearchNext;
{
  let pdfSearchTimer = null;
  document.getElementById("pdf-search-input").addEventListener("input", (e) => {
    clearTimeout(pdfSearchTimer);
    const query = e.target.value.trim();
    // Debounce search to avoid lag on fast typing
    pdfSearchTimer = setTimeout(() => executePdfSearch(query), 200);
  });
}
document.getElementById("pdf-search-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    if (e.shiftKey) pdfSearchPrev();
    else pdfSearchNext();
  }
  if (e.key === "Escape") {
    e.preventDefault();
    closePdfSearch();
  }
});

// ── SyncTeX: Ctrl/Cmd cursor hint + status bar ──
{
  const pdfEl = document.getElementById("pdf-container");
  const statusLeft = document.getElementById("status-left");
  let savedStatus = "";
  let ctrlHeld = false;
  let hoveringPdf = false;

  function updateSynctexHint() {
    if (ctrlHeld && hoveringPdf) {
      pdfEl?.classList.add("synctex-ready");
      savedStatus = statusLeft.textContent;
      statusLeft.textContent = t("sc_synctex");
    } else {
      pdfEl?.classList.remove("synctex-ready");
      if (statusLeft.textContent === t("sc_synctex")) statusLeft.textContent = savedStatus;
    }
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Control" || e.key === "Meta") { ctrlHeld = true; updateSynctexHint(); }
  });
  document.addEventListener("keyup", (e) => {
    if (e.key === "Control" || e.key === "Meta") { ctrlHeld = false; updateSynctexHint(); }
  });
  pdfEl?.addEventListener("mouseenter", () => { hoveringPdf = true; updateSynctexHint(); });
  pdfEl?.addEventListener("mouseleave", () => { hoveringPdf = false; updateSynctexHint(); });
  window.addEventListener("blur", () => { ctrlHeld = false; hoveringPdf = false; updateSynctexHint(); });
}

// ── Auto-refresh on window focus ──
window.addEventListener("focus", () => {
  if (S.projectName) {
    refreshFiles();
    refreshGit();
  }
});

// ── Panel resize & collapse ──
(function initPanels() {
  const sidebar = document.getElementById("sidebar");
  const pdfPane = document.getElementById("pdf-pane");
  const resizeSidebar = document.getElementById("resize-sidebar");
  const resizePdf = document.getElementById("resize-pdf");

  // Restore saved widths
  const savedSidebarW = localStorage.getItem("tinyleaf-sidebar-width");
  if (savedSidebarW) sidebar.style.width = savedSidebarW + "px";

  const savedPdfW = localStorage.getItem("tinyleaf-pdf-width");
  if (savedPdfW) pdfPane.style.flex = "0 0 " + savedPdfW + "px";

  // Restore layout preset first, then honor individual sidebar toggle
  const savedLayout = localStorage.getItem("tinyleaf-layout") || "split";
  setLayout(savedLayout);
  if (savedLayout !== "pdf" && localStorage.getItem("tinyleaf-sidebar-collapsed") === "1") {
    sidebar.classList.add("collapsed");
  }

  function setupResize(handle, target, applySizeFn, storageKey, min, max, invert) {
    handle.addEventListener("mousedown", function (e) {
      e.preventDefault();
      const startX = e.clientX;
      const startSize = target.getBoundingClientRect().width;
      handle.classList.add("active");
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";
      function onMove(e2) {
        const delta = invert ? (startX - e2.clientX) : (e2.clientX - startX);
        let newSize = Math.max(min, Math.min(max, startSize + delta));
        applySizeFn(newSize);
        target.classList.remove("collapsed");
        localStorage.setItem(storageKey.replace("-width", "-collapsed"), "0");
        localStorage.setItem(storageKey, Math.round(newSize));
      }
      function onUp() {
        handle.classList.remove("active");
        document.body.style.cursor = "";
        document.body.style.userSelect = "";
        document.removeEventListener("mousemove", onMove);
        document.removeEventListener("mouseup", onUp);
      }
      document.addEventListener("mousemove", onMove);
      document.addEventListener("mouseup", onUp);
    });
    // Double-click to toggle collapse
    handle.addEventListener("dblclick", () => {
      target.classList.toggle("collapsed");
      const key = storageKey.replace("-width", "-collapsed");
      localStorage.setItem(key, target.classList.contains("collapsed") ? "1" : "0");
    });
  }

  setupResize(
    resizeSidebar, sidebar,
    (w) => { sidebar.style.width = w + "px"; },
    "tinyleaf-sidebar-width", 150, 500, false
  );

  setupResize(
    resizePdf, pdfPane,
    (w) => { pdfPane.style.flex = "0 0 " + w + "px"; },
    "tinyleaf-pdf-width", 200, window.innerWidth * 0.7, true
  );
})();

// ── Start ──
init();
