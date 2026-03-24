#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".php",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".json",
    ".jsonc",
    ".yml",
    ".yaml",
    ".dart",
    ".py",
    ".ps1",
    ".psm1",
    ".psd1",
    ".sh",
    ".css",
    ".scss",
    ".less",
    ".html",
    ".htm",
    ".xml",
    ".sql",
    ".env",
    ".ini",
    ".conf",
    ".properties",
    ".java",
    ".kt",
    ".gradle",
    ".rb",
    ".go",
    ".rs",
    ".vue",
}

TEXT_FILENAMES = {
    "Dockerfile",
    ".gitignore",
    ".editorconfig",
    ".gitattributes",
    ".npmrc",
    ".prettierrc",
    ".eslintrc",
    "README",
    "LICENSE",
}

IGNORED_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    "vendor",
    "build",
    "dist",
    "target",
    "coverage",
    ".dart_tool",
    ".next",
    ".nuxt",
}

SUSPICIOUS_SNIPPETS = {
    "\u951f\u65a4\u62f7": "检测到常见的乱码片段 U+951F U+65A4 U+62F7",
    "\u70eb\u70eb\u70eb": "检测到常见的乱码片段 U+70EB U+70EB U+70EB",
    "\u00ef\u00bb\u00bf": "检测到 BOM 被错误写入文本内容",
    "\u00c3": "检测到疑似 UTF-8/ANSI 双重解码乱码片段 U+00C3",
    "\u00c2": "检测到疑似 UTF-8/ANSI 双重解码乱码片段 U+00C2",
}

LIKELY_CN_MOJIBAKE_SNIPPETS = {
    "濂戠害": "契约",
    "鐗堟湰": "版本",
    "鎺ュ彛": "接口",
    "璇存槑": "说明",
    "鍙傛暟": "参数",
    "鍝嶅簲": "响应",
    "寮哄埗": "强制",
    "鏇存柊": "更新",
    "鍏ュ彛": "入口",
    "楠屾敹": "验收",
    "浠诲姟": "任务",
    "璺敱": "路由",
    "鏉冮檺": "权限",
    "鍚庣": "后端",
    "鍓嶇": "前端",
    "涓夌": "三端",
    "鐧诲綍": "登录",
    "瀛楁": "字段",
}

MOJIBAKE_CONTEXT_IGNORE_SNIPPETS = {
    "LIKELY_CN_MOJIBAKE_SNIPPETS",
    "suspicious_cn_mojibake",
    "典型命中片段",
    "错码片段",
    "用于识别",
    "专门识别",
    "命中片段包括",
    "检测到疑似 GBK/ANSI 误解码后的中文错码片段",
}

PROTECTED_MARKDOWN_PATTERNS = {
    ".github/*.md",
    ".github/**/*.md",
    "docs/*.md",
    "docs/**/*.md",
    "指南.md",
}


@dataclass
class Issue:
    path: str
    code: str
    severity: str
    message: str


@dataclass
class CheckResult:
    name: str
    scope: str
    status: str
    command: str
    message: str


def run_git(root: Path, args: list[str]) -> list[str]:
    command = ["git", "-C", str(root), *args]
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if completed.returncode != 0:
        return []
    return [line.rstrip("\r") for line in completed.stdout.splitlines() if line.strip()]


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    if path.name in TEXT_FILENAMES:
        return True
    return False


def normalize_path(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def detect_likely_cn_mojibake(text: str) -> list[str]:
    matches: set[str] = set()
    for line in text.splitlines():
        if any(marker in line for marker in MOJIBAKE_CONTEXT_IGNORE_SNIPPETS):
            continue
        if re.match(r'\s*"[^\"]+":\s*"[^\"]+",?\s*$', line):
            continue
        for snippet in LIKELY_CN_MOJIBAKE_SNIPPETS:
            if snippet in line:
                matches.add(snippet)
    return sorted(matches, key=len, reverse=True)


def validate_file(root: Path, path: Path) -> list[Issue]:
    issues: list[Issue] = []
    rel_path = normalize_path(root, path)

    try:
        raw = path.read_bytes()
    except OSError as exc:
        return [Issue(rel_path, "read_error", "error", f"文件读取失败: {exc}")]

    if b"\x00" in raw:
        issues.append(Issue(rel_path, "null_byte", "error", "文件包含 NUL 字节，疑似写入损坏或二进制内容混入"))

    if raw.startswith(b"\xef\xbb\xbf"):
        issues.append(Issue(rel_path, "utf8_bom", "warning", "文件是 UTF-8 BOM，建议统一改为 UTF-8 无 BOM"))

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        issues.append(Issue(rel_path, "non_utf8", "error", f"文件不是有效 UTF-8: {exc}"))
        return issues

    if "\ufffd" in text:
        issues.append(Issue(rel_path, "replacement_char", "error", "文件中存在替换字符 U+FFFD，疑似乱码或写入截断"))

    for snippet, message in SUSPICIOUS_SNIPPETS.items():
        if snippet in text:
            issues.append(Issue(rel_path, "suspicious_mojibake", "warning", message))

    cn_mojibake_matches = detect_likely_cn_mojibake(text)
    if cn_mojibake_matches:
        display_matches = ", ".join(cn_mojibake_matches[:5])
        if len(cn_mojibake_matches) > 5:
            display_matches = f"{display_matches} 等 {len(cn_mojibake_matches)} 个片段"
        issues.append(
            Issue(
                rel_path,
                "suspicious_cn_mojibake",
                "warning",
                f"检测到疑似 GBK/ANSI 误解码后的中文错码片段: {display_matches}；建议优先用 Git 历史或原始 UTF-8 文本恢复",
            )
        )

    if path.suffix.lower() == ".json":
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            issues.append(Issue(rel_path, "invalid_json", "error", f"JSON 结构无效: {exc.msg} (line {exc.lineno}, column {exc.colno})"))

    if path.suffix.lower() == ".md":
        fence_count = text.count("```")
        if fence_count % 2 != 0:
            issues.append(Issue(rel_path, "markdown_fence", "warning", "Markdown 代码块围栏数量为奇数，可能存在截断或未闭合代码块"))

    if not text.endswith(("\n", "\r\n")):
        issues.append(Issue(rel_path, "missing_final_newline", "warning", "文件末尾缺少换行，可能是异常截断或非标准写入"))

    return issues


def collect_changed_files(root: Path) -> list[Path]:
    changed: list[Path] = []
    command = [
        "git",
        "-C",
        str(root),
        "status",
        "--porcelain",
        "--untracked-files=all",
        "-z",
    ]
    completed = subprocess.run(command, capture_output=True)
    if completed.returncode != 0:
        return []

    entries = [entry for entry in completed.stdout.split(b"\x00") if entry]
    index = 0
    while index < len(entries):
        raw_entry = entries[index]
        index += 1
        if len(raw_entry) < 4:
            continue

        status = raw_entry[:2].decode("ascii", errors="replace")
        candidate = raw_entry[3:].decode("utf-8", errors="replace")

        # In -z mode, renames/copies emit an extra path entry. Prefer the destination path.
        if any(flag in status for flag in {"R", "C"}) and index < len(entries):
            candidate = entries[index].decode("utf-8", errors="replace")
            index += 1

        path = (root / candidate).resolve()
        if path.exists() and path.is_file() and is_text_file(path):
            changed.append(path)
    return sorted({item for item in changed}, key=lambda item: str(item).lower())


def collect_changed_files_by_suffix(root: Path, suffixes: set[str]) -> list[Path]:
    files = []
    for path in collect_changed_files(root):
        if path.suffix.lower() in suffixes:
            files.append(path)
    return files


def classify_markdown_kind(text: str) -> str:
    stripped = text.lstrip()
    if stripped.startswith("{") and '"cells"' in text and '"cell_type"' in text:
        return "notebook-json"
    if "<VSCode.Cell" in text:
        return "vscode-cell"
    return "plain"


def is_protected_markdown(rel_path: str) -> bool:
    return any(fnmatch.fnmatch(rel_path, pattern) for pattern in PROTECTED_MARKDOWN_PATTERNS)


def get_markdown_write_policy(rel_path: str, kind: str) -> dict:
    if kind in {"notebook-json", "vscode-cell"} or is_protected_markdown(rel_path):
        return {
            "protected": True,
            "writeMode": "notebook-cell",
            "recommendedTool": "edit_notebook_file",
            "allowWholeFileOverwrite": False,
            "retryRequiredOnError": True,
        }
    return {
        "protected": False,
        "writeMode": "incremental-patch",
        "recommendedTool": "apply_patch",
        "allowWholeFileOverwrite": False,
        "retryRequiredOnError": True,
    }


def build_markdown_retry_hint(policy: dict) -> str:
    return f"请改用 {policy['recommendedTool']} 重新写入，并在重写后再次执行 validate-markdown；禁止整文件覆盖原文"


def count_lines(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def validate_markdown_file(root: Path, path: Path, require_changed: bool, changed_paths: set[str]) -> tuple[dict, list[Issue]]:
    rel_path = normalize_path(root, path)
    issues = validate_file(root, path)

    try:
        raw = path.read_bytes()
    except OSError as exc:
        issues.append(Issue(rel_path, "read_error", "error", f"文件读取失败: {exc}"))
        return {
            "path": rel_path,
            "kind": "unknown",
            "changed": rel_path in changed_paths,
            "sizeBytes": 0,
            "lineCount": 0,
        }, issues

    text = raw.decode("utf-8", errors="replace")
    kind = classify_markdown_kind(text)
    policy = get_markdown_write_policy(rel_path, kind)

    if len(raw) == 0:
        issues.append(Issue(rel_path, "empty_file", "error", f"Markdown 文件为空，疑似写入失败或被覆盖为空文件；{build_markdown_retry_hint(policy)}"))

    if not text.strip():
        issues.append(Issue(rel_path, "blank_markdown", "error", f"Markdown 文件只包含空白内容，疑似写入失败或被错误清空；{build_markdown_retry_hint(policy)}"))

    changed = rel_path in changed_paths
    if require_changed and not changed:
        issues.append(Issue(rel_path, "markdown_not_changed", "error", f"Markdown 文件未出现在 Git 变更中，无法确认本次写入已真正落盘；{build_markdown_retry_hint(policy)}"))

    if kind == "notebook-json":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            issues.append(Issue(rel_path, "invalid_notebook_json", "error", f"Notebook Markdown JSON 结构无效: {exc.msg} (line {exc.lineno}, column {exc.colno})；{build_markdown_retry_hint(policy)}"))
        else:
            cells = payload.get("cells")
            if not isinstance(cells, list) or not cells:
                issues.append(Issue(rel_path, "notebook_cells_missing", "error", f"Notebook-backed Markdown 未检测到有效 cells，疑似写入失败或结构损坏；{build_markdown_retry_hint(policy)}"))
    elif kind == "vscode-cell":
        open_count = text.count("<VSCode.Cell")
        close_count = text.count("</VSCode.Cell>")
        if open_count == 0:
            issues.append(Issue(rel_path, "notebook_cells_missing", "error", f"VSCode.Cell Markdown 未检测到单元起始标记，疑似写入失败；{build_markdown_retry_hint(policy)}"))
        if open_count != close_count:
            issues.append(Issue(rel_path, "vscode_cell_mismatch", "error", f"VSCode.Cell 起止标记数量不一致，疑似写入截断；{build_markdown_retry_hint(policy)}"))

    return {
        "path": rel_path,
        "kind": kind,
        "changed": changed,
        "protected": policy["protected"],
        "writeMode": policy["writeMode"],
        "recommendedTool": policy["recommendedTool"],
        "allowWholeFileOverwrite": policy["allowWholeFileOverwrite"],
        "retryRequiredOnError": policy["retryRequiredOnError"],
        "sizeBytes": len(raw),
        "lineCount": count_lines(text),
    }, issues


def report_markdown_validation(root: Path, files: list[Path], require_changed: bool) -> dict:
    changed_paths = {normalize_path(root, path) for path in collect_changed_files_by_suffix(root, {".md"})}
    issues: list[Issue] = []
    markdown_files: list[dict] = []

    for path in files:
        markdown_file, file_issues = validate_markdown_file(root, path, require_changed, changed_paths)
        markdown_files.append(markdown_file)
        issues.extend(file_issues)

    severity_rank = {"error": 2, "warning": 1, "info": 0}
    highest = max((severity_rank.get(issue.severity, 0) for issue in issues), default=0)
    status = "error" if highest == 2 else "warning" if highest == 1 else "ok"

    return {
        "root": root.as_posix(),
        "checkedFiles": [item["path"] for item in markdown_files],
        "markdownFiles": markdown_files,
        "summary": {
            "checked": len(markdown_files),
            "issues": len(issues),
            "status": status,
            "requireChanged": require_changed,
        },
        "issues": [asdict(issue) for issue in issues],
    }


def build_workspace_map(root: Path, max_depth: int, focus: str | None = None) -> dict:
    target_root = root
    if focus:
        focus_path = Path(focus)
        target_root = (focus_path.resolve() if focus_path.is_absolute() else (root / focus_path).resolve())
        if not target_root.exists():
            raise FileNotFoundError(f"focus path does not exist: {focus}")
        if target_root.is_file():
            return {
                "root": root.as_posix(),
                "focus": normalize_path(root, target_root),
                "maxDepth": max_depth,
                "ignoredDirs": sorted(IGNORED_DIRS),
                "entries": [{"name": target_root.name, "path": normalize_path(root, target_root), "type": "file"}],
            }

    def walk(directory: Path, depth: int) -> dict:
        node = {
            "name": directory.name or directory.as_posix(),
            "path": normalize_path(root, directory),
            "type": "directory",
            "children": [],
        }
        if depth >= max_depth:
            return node

        try:
            entries = sorted(directory.iterdir(), key=lambda item: (item.is_file(), item.name.lower()))
        except OSError:
            return node

        for entry in entries:
            if entry.name in IGNORED_DIRS:
                continue
            if entry.is_dir():
                node["children"].append(walk(entry, depth + 1))
            else:
                node["children"].append({
                    "name": entry.name,
                    "path": normalize_path(root, entry),
                    "type": "file",
                })
        return node

    entries = []
    for entry in sorted(target_root.iterdir(), key=lambda item: (item.is_file(), item.name.lower())):
        if entry.name in IGNORED_DIRS:
            continue
        if entry.is_dir():
            entries.append(walk(entry, 1))
        else:
            entries.append({
                "name": entry.name,
                "path": normalize_path(root, entry),
                "type": "file",
            })

    return {
        "root": root.as_posix(),
        "focus": normalize_path(root, target_root),
        "maxDepth": max_depth,
        "ignoredDirs": sorted(IGNORED_DIRS),
        "entries": entries,
    }


def render_tree(entries: Iterable[dict], prefix: str = "") -> list[str]:
    lines: list[str] = []
    items = list(entries)
    for index, item in enumerate(items):
        connector = "└── " if index == len(items) - 1 else "├── "
        lines.append(f"{prefix}{connector}{item['name']}")
        children = item.get("children") or []
        if children:
            child_prefix = "    " if index == len(items) - 1 else "│   "
            lines.extend(render_tree(children, prefix + child_prefix))
    return lines


def report_validate(root: Path, files: list[Path]) -> dict:
    issues: list[Issue] = []
    checked_files: list[str] = []
    for path in files:
        checked_files.append(normalize_path(root, path))
        issues.extend(validate_file(root, path))

    severity_rank = {"error": 2, "warning": 1, "info": 0}
    highest = max((severity_rank.get(issue.severity, 0) for issue in issues), default=0)
    status = "error" if highest == 2 else "warning" if highest == 1 else "ok"

    return {
        "root": root.as_posix(),
        "checkedFiles": checked_files,
        "summary": {
            "checked": len(checked_files),
            "issues": len(issues),
            "status": status,
        },
        "issues": [asdict(issue) for issue in issues],
    }


def run_command(command: list[str], cwd: Path) -> tuple[int, str]:
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = completed.stdout.strip() or completed.stderr.strip()
    return completed.returncode, output


def summarize_tool_output(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return ""
    for line in reversed(lines):
        if " - " in line:
            return line
    return lines[-1]


def classify_flutter_analyze_output(code: int, output: str) -> tuple[str, str]:
    error_count = len(re.findall(r"(^|\s)error\s+-\s+", output, flags=re.MULTILINE))
    warning_count = len(re.findall(r"(^|\s)warning\s+-\s+", output, flags=re.MULTILINE))
    info_count = len(re.findall(r"(^|\s)info\s+-\s+", output, flags=re.MULTILINE))

    if error_count > 0:
        summary = f"flutter analyze found {error_count} errors, {warning_count} warnings, {info_count} infos"
        detail = summarize_tool_output(output)
        return "error", f"{summary}; {detail}" if detail else summary

    if warning_count > 0 or info_count > 0:
        summary = f"flutter analyze found {warning_count} warnings, {info_count} infos"
        detail = summarize_tool_output(output)
        return "warning", f"{summary}; {detail}" if detail else summary

    if code == 0:
        return "ok", "flutter analyze passed"

    detail = summarize_tool_output(output)
    return "error", detail or "flutter analyze failed"


def validate_backend_project(root: Path) -> list[CheckResult]:
    php = shutil.which("php")
    if not php:
        return [CheckResult("php-syntax", "backend", "skipped", "php -l <changed-files>", "php is not available")]

    changed_php = collect_changed_files_by_suffix(root, {".php"})
    if not changed_php:
        return [CheckResult("php-syntax", "backend", "skipped", "php -l <changed-files>", "no changed PHP files detected")]

    results: list[CheckResult] = []
    for path in changed_php:
        code, output = run_command([php, "-l", str(path)], root)
        status = "ok" if code == 0 else "error"
        message = output or "syntax check passed"
        results.append(CheckResult(f"php-lint:{normalize_path(root, path)}", "backend", status, f"php -l {normalize_path(root, path)}", message))
    return results


def validate_app_project(root: Path, scope_name: str = "app") -> list[CheckResult]:
    flutter = shutil.which("flutter")
    app_root = root / "livehome_app"
    if not flutter:
        return [CheckResult("flutter-analyze", scope_name, "skipped", "flutter analyze", "flutter is not available")]
    if not app_root.exists():
        return [CheckResult("flutter-analyze", scope_name, "skipped", "flutter analyze", "livehome_app directory does not exist")]

    command = [flutter, "analyze", "--no-fatal-infos", "--no-fatal-warnings"]
    code, output = run_command(command, app_root)
    status, message = classify_flutter_analyze_output(code, output)
    return [CheckResult("flutter-analyze", scope_name, status, "flutter analyze --no-fatal-infos --no-fatal-warnings", message)]


def validate_web_project(root: Path, scope_name: str = "web") -> list[CheckResult]:
    npx = shutil.which("npx")
    web_root = root / "livehome_ng"
    if not npx:
        return [CheckResult("tsc-noemit", scope_name, "skipped", "npx tsc --noEmit -p tsconfig.app.json", "npx is not available")]
    if not web_root.exists():
        return [CheckResult("tsc-noemit", scope_name, "skipped", "npx tsc --noEmit -p tsconfig.app.json", "livehome_ng directory does not exist")]

    code, output = run_command([npx, "tsc", "--noEmit", "-p", "tsconfig.app.json"], web_root)
    status = "ok" if code == 0 else "error"
    message = summarize_tool_output(output) or ("TypeScript compile check passed" if code == 0 else "TypeScript compile check failed")
    return [CheckResult("tsc-noemit", scope_name, status, "npx tsc --noEmit -p tsconfig.app.json", message)]


def normalize_project_scopes(scopes: list[str]) -> tuple[list[str], set[str]]:
    requested = list(dict.fromkeys(scopes or ["backend", "flutter", "angular"]))
    normalized: set[str] = set()
    for scope in requested:
        if scope == "flutter":
            normalized.add("app")
        elif scope == "angular":
            normalized.add("web")
        else:
            normalized.add(scope)
    return requested, normalized


def report_project_validation(root: Path, scopes: list[str]) -> dict:
    requested_scopes, normalized_scopes = normalize_project_scopes(scopes)
    file_report = report_validate(root, collect_changed_files(root))

    checks: list[CheckResult] = []
    if "backend" in normalized_scopes:
        checks.extend(validate_backend_project(root))
    if "app" in normalized_scopes:
        checks.extend(validate_app_project(root, "flutter" if "flutter" in requested_scopes else "app"))
    if "web" in normalized_scopes:
        checks.extend(validate_web_project(root, "angular" if "angular" in requested_scopes else "web"))

    status_rank = {"error": 2, "warning": 1, "ok": 0, "skipped": 0}
    highest = max(
        [status_rank.get(file_report["summary"]["status"], 0)] + [status_rank.get(check.status, 0) for check in checks],
        default=0,
    )
    status = "error" if highest == 2 else "warning" if highest == 1 else "ok"

    return {
        "root": root.as_posix(),
        "scopes": requested_scopes,
        "fileSafety": file_report,
        "checks": [asdict(check) for check in checks],
        "summary": {
            "status": status,
            "fileIssues": len(file_report["issues"]),
            "checks": len(checks),
            "failedChecks": len([check for check in checks if check.status == "error"]),
            "skippedChecks": len([check for check in checks if check.status == "skipped"]),
        },
    }


def print_json(payload: dict) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    status = payload.get("summary", {}).get("status")
    if status == "error":
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="LiveHome AI 文件安全与结构扫描工具")
    parser.add_argument("--root", default=os.getcwd(), help="工作区根目录")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_files_parser = subparsers.add_parser("validate-files", help="校验指定文件是否为有效 UTF-8、中文错码以及常见结构问题")
    validate_files_parser.add_argument("--root", dest="command_root", help="工作区根目录")
    validate_files_parser.add_argument("paths", nargs="+", help="要校验的文件路径")
    validate_files_parser.add_argument("--json", action="store_true", help="以 JSON 输出")

    validate_changed_parser = subparsers.add_parser("validate-changed", help="校验 Git 变更中的文本文件，包含 UTF-8、中文错码和基础结构检查")
    validate_changed_parser.add_argument("--root", dest="command_root", help="工作区根目录")
    validate_changed_parser.add_argument("--json", action="store_true", help="以 JSON 输出")

    validate_project_parser = subparsers.add_parser("validate-project", help="执行文件安全校验与项目级检查")
    validate_project_parser.add_argument("--root", dest="command_root", help="工作区根目录")
    validate_project_parser.add_argument("--scope", action="append", choices=["backend", "app", "web", "flutter", "angular"], help="要执行的项目范围，可重复传入")
    validate_project_parser.add_argument("--json", action="store_true", help="以 JSON 输出")

    validate_markdown_parser = subparsers.add_parser("validate-markdown", help="执行 Markdown 专项写入校验")
    validate_markdown_parser.add_argument("--root", dest="command_root", help="工作区根目录")
    validate_markdown_parser.add_argument("paths", nargs="*", help="要校验的 Markdown 文件路径；不传时默认校验 Git 变更中的 Markdown")
    validate_markdown_parser.add_argument("--require-changed", action="store_true", help="要求目标 Markdown 必须出现在 Git 变更中")
    validate_markdown_parser.add_argument("--json", action="store_true", help="以 JSON 输出")

    workspace_map_parser = subparsers.add_parser("workspace-map", help="输出项目结构地图")
    workspace_map_parser.add_argument("--root", dest="command_root", help="工作区根目录")
    workspace_map_parser.add_argument("--focus", help="只展开某个子目录或模块路径")
    workspace_map_parser.add_argument("--max-depth", type=int, default=3, help="目录扫描深度，默认 3")
    workspace_map_parser.add_argument("--json", action="store_true", help="以 JSON 输出")

    args = parser.parse_args()
    root = Path(getattr(args, "command_root", None) or args.root).resolve()

    if args.command == "validate-files":
        files = []
        for raw_path in args.paths:
            path = Path(raw_path)
            resolved = path.resolve() if path.is_absolute() else (root / path).resolve()
            if resolved.exists() and resolved.is_file() and is_text_file(resolved):
                files.append(resolved)
        report = report_validate(root, files)
        if args.json:
            return print_json(report)

        if not report["issues"]:
            print("OK: 所有目标文件都通过了 UTF-8、中文错码与基础结构校验")
            return 0
        for issue in report["issues"]:
            print(f"[{issue['severity']}] {issue['path']} :: {issue['code']} :: {issue['message']}")
        return 1

    if args.command == "validate-changed":
        report = report_validate(root, collect_changed_files(root))
        if args.json:
            return print_json(report)

        if not report["checkedFiles"]:
            print("OK: 当前没有需要校验的 Git 变更文本文件")
            return 0
        if not report["issues"]:
            print("OK: 所有 Git 变更文本文件都通过了 UTF-8、中文错码与基础结构校验")
            return 0
        for issue in report["issues"]:
            print(f"[{issue['severity']}] {issue['path']} :: {issue['code']} :: {issue['message']}")
        return 1

    if args.command == "validate-project":
        report = report_project_validation(root, args.scope or ["backend", "flutter", "angular"])
        if args.json:
            return print_json(report)

        for issue in report["fileSafety"]["issues"]:
            print(f"[file-{issue['severity']}] {issue['path']} :: {issue['code']} :: {issue['message']}")
        for check in report["checks"]:
            print(f"[{check['status']}] {check['scope']} :: {check['name']} :: {check['message']}")
        return 0 if report["summary"]["status"] == "ok" else 1

    if args.command == "validate-markdown":
        files: list[Path] = []
        if args.paths:
            for raw_path in args.paths:
                path = Path(raw_path)
                resolved = path.resolve() if path.is_absolute() else (root / path).resolve()
                if resolved.exists() and resolved.is_file() and resolved.suffix.lower() == ".md":
                    files.append(resolved)
        else:
            files = collect_changed_files_by_suffix(root, {".md"})

        report = report_markdown_validation(root, files, args.require_changed or bool(args.paths))
        if args.json:
            return print_json(report)

        if not report["checkedFiles"]:
            print("OK: 当前没有需要校验的 Markdown 文件")
            return 0
        if not report["issues"]:
            print("OK: 所有目标 Markdown 文件都通过了专项写入校验")
            return 0
        for issue in report["issues"]:
            print(f"[{issue['severity']}] {issue['path']} :: {issue['code']} :: {issue['message']}")
        return 1

    if args.command == "workspace-map":
        payload = build_workspace_map(root, args.max_depth, args.focus)
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        print(root.as_posix())
        print("\n".join(render_tree(payload["entries"])))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
