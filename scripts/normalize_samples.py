#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
normalize_samples.py — 把原始素材文件夹归一化为带 frontmatter 的 markdown 样本。

支持的输入格式：.md / .txt / .html / .htm
输出：samples_normalized/NNN-标题前20字.md，每个都带统一的 YAML frontmatter。

用法：
    python normalize_samples.py <input_dir> [--out <out_dir>] [--author <name>] [--platform <name>]

示例：
    python normalize_samples.py ./raw_articles
    python normalize_samples.py ./raw --out ./samples_normalized --author 量子位 --platform 公众号

不抓网络、不处理 docx/pdf——这两种由用户先用其他工具转 md 后再喂进来。
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

INVALID_FILENAME_CHARS = r'[\\/:*?"<>|]'

# 噪音模式：常见的公众号底部 / 网页噪音
NOISE_PATTERNS = [
    r"长按.{0,4}关注",
    r"点击.{0,6}关注",
    r"点击.{0,4}阅读原文",
    r"扫码.{0,8}关注",
    r"一键三连",
    r"在看.{0,4}点赞",
    r"广告.{0,2}合作",
    r"商务.{0,2}合作",
    r"投稿.{0,4}邮箱",
    r"^\s*©.{0,30}版权所有",
    r"未经.{0,6}授权.{0,6}转载",
]


def strip_html_to_md(html: str) -> str:
    """极简 HTML → Markdown 转换。不引入外部依赖（保持脚本零依赖）。

    保留：strong/b → **，em/i → *，blockquote → >，img → ![](image-placeholder)，
        h1-h6 → #，p / br → 换行，a → [text](url)
    丢弃：所有其他标签，但保留其内部文本。
    """
    s = html

    # 删除 script/style
    s = re.sub(r"<script[^>]*>.*?</script>", "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<style[^>]*>.*?</style>", "", s, flags=re.DOTALL | re.IGNORECASE)
    # 删除注释
    s = re.sub(r"<!--.*?-->", "", s, flags=re.DOTALL)

    # 加粗 / 斜体
    # 注意：单字母标签 b/i 必须用 \b 词边界，否则 <body>/<img>/<input> 会被误匹配
    s = re.sub(r"<\s*(?:strong|b)\b[^>]*>(.*?)</\s*(?:strong|b)\s*>", r"**\1**", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<\s*(?:em|i)\b[^>]*>(.*?)</\s*(?:em|i)\s*>", r"*\1*", s, flags=re.DOTALL | re.IGNORECASE)

    # 标题 h1-h6
    for level in range(6, 0, -1):
        s = re.sub(
            rf"<\s*h{level}\s*[^>]*>(.*?)</\s*h{level}\s*>",
            lambda m, lv=level: "\n" + ("#" * lv) + " " + m.group(1).strip() + "\n",
            s,
            flags=re.DOTALL | re.IGNORECASE,
        )

    # 引用
    s = re.sub(
        r"<\s*blockquote\s*[^>]*>(.*?)</\s*blockquote\s*>",
        lambda m: "\n" + "\n".join("> " + line for line in m.group(1).strip().splitlines() if line.strip()) + "\n",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # 图片
    s = re.sub(
        r"<\s*img\s+[^>]*alt\s*=\s*[\"']([^\"']*)[\"'][^>]*>",
        r"![\1](image-placeholder)",
        s,
        flags=re.IGNORECASE,
    )
    s = re.sub(r"<\s*img[^>]*>", "![](image-placeholder)", s, flags=re.IGNORECASE)

    # 链接
    s = re.sub(
        r"<\s*a\s+[^>]*href\s*=\s*[\"']([^\"']+)[\"'][^>]*>(.*?)</\s*a\s*>",
        r"[\2](\1)",
        s,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # 列表项（li 用 \b 防止误匹配 <link>）
    s = re.sub(r"<\s*li\b[^>]*>(.*?)</\s*li\s*>", r"- \1\n", s, flags=re.DOTALL | re.IGNORECASE)

    # 段落 / 换行（p 用 \b 防止误匹配 <pre>）
    s = re.sub(r"<\s*br\b[^>]*/?\s*>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<\s*/?\s*p\b[^>]*>", "\n\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<\s*/?\s*div\b[^>]*>", "\n", s, flags=re.IGNORECASE)

    # 剥掉所有剩余标签
    s = re.sub(r"<[^>]+>", "", s)

    # 解码常见 HTML 实体（简易版）
    entities = {
        "&nbsp;": " ",
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": '"',
        "&#39;": "'",
        "&ldquo;": "“",
        "&rdquo;": "”",
        "&lsquo;": "‘",
        "&rsquo;": "’",
        "&hellip;": "…",
        "&mdash;": "—",
        "&ndash;": "–",
    }
    for k, v in entities.items():
        s = s.replace(k, v)

    return s


def remove_noise(md: str) -> str:
    lines = md.splitlines()
    out = []
    for line in lines:
        stripped = line.strip()
        if any(re.search(p, stripped) for p in NOISE_PATTERNS):
            continue
        out.append(line)
    return "\n".join(out)


def collapse_blank_lines(md: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"


def extract_title(md: str, fallback: str) -> str:
    """优先取第一个 # 标题；否则取第一行非空文本前 40 字。"""
    for line in md.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^#{1,6}\s+(.+)$", line)
        if m:
            return m.group(1).strip()
        # 第一行非空就当标题候选
        return line[:60]
    return fallback


def safe_filename(s: str, max_len: int = 20) -> str:
    s = re.sub(INVALID_FILENAME_CHARS, "", s)
    s = s.replace("\n", " ").replace("\r", " ").strip()
    return s[:max_len] if s else "untitled"


def count_words(md: str) -> int:
    """中英混合的字数统计：中文按字算，英文按词算。"""
    text = re.sub(r"```.*?```", "", md, flags=re.DOTALL)  # 去代码块
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)  # 去图片
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # 链接保留文字
    text = re.sub(r"[#>*`\-]", "", text)
    chinese = re.findall(r"[一-鿿]", text)
    english = re.findall(r"[A-Za-z][A-Za-z']*", text)
    return len(chinese) + len(english)


def detect_language(md: str) -> str:
    chinese = len(re.findall(r"[一-鿿]", md))
    english = len(re.findall(r"[A-Za-z]", md))
    total = chinese + english
    if total == 0:
        return "zh"
    if chinese / total > 0.7:
        return "zh"
    if english / total > 0.7:
        return "en"
    return "mixed"


def build_frontmatter(
    *,
    title: str,
    author: str,
    platform: str,
    url: str,
    publish_date: str,
    word_count: int,
    source_file: str,
    language: str,
) -> str:
    def esc(v: str) -> str:
        # YAML 简易转义：含特殊字符就加单引号并 escape 内嵌单引号
        if v == "" or v is None:
            return ""
        if re.search(r"[:#@`'\"\[\]{}|>!&*?,%]", v) or v.startswith(" ") or v.endswith(" "):
            return "'" + v.replace("'", "''") + "'"
        return v

    fields = [
        ("title", esc(title)),
        ("author", esc(author or "未知")),
        ("platform", esc(platform or "未知")),
        ("url", esc(url)),
        ("publish_date", esc(publish_date)),
        ("word_count", str(word_count)),
        ("source_file", esc(source_file)),
        ("language", esc(language)),
        ("content_type", ""),  # 留空，分析阶段填
    ]
    lines = ["---"]
    for k, v in fields:
        if v == "":
            lines.append(f"{k}: ")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def normalize_one(path: Path, *, author: str, platform: str) -> tuple[str, str]:
    """返回 (frontmatter+body, suggested_filename_stem)"""
    raw = path.read_text(encoding="utf-8", errors="replace")

    suffix = path.suffix.lower()
    if suffix in {".html", ".htm"}:
        body = strip_html_to_md(raw)
    elif suffix in {".md", ".markdown"}:
        body = raw
    elif suffix == ".txt":
        body = raw
    else:
        raise ValueError(f"unsupported extension: {suffix}")

    # 如果已有 frontmatter，把它剥掉（避免双 frontmatter）
    fm_match = re.match(r"^---\s*\n.*?\n---\s*\n", body, flags=re.DOTALL)
    if fm_match:
        body = body[fm_match.end():]

    body = remove_noise(body)
    body = collapse_blank_lines(body)

    title = extract_title(body, fallback=path.stem)

    # 如果正文第一行不是 # 标题，加一个
    if not re.match(r"^#\s+", body.lstrip()):
        body = f"# {title}\n\n{body.lstrip()}"

    wc = count_words(body)
    lang = detect_language(body)

    try:
        rel = path.relative_to(path.parent.parent).as_posix()
    except ValueError:
        rel = path.name
    fm = build_frontmatter(
        title=title,
        author=author,
        platform=platform,
        url="",
        publish_date="",
        word_count=wc,
        source_file=rel,
        language=lang,
    )

    full = fm + "\n\n" + body.strip() + "\n"
    return full, safe_filename(title)


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize raw articles into a standard samples folder.")
    ap.add_argument("input_dir", type=Path, help="原始素材目录")
    ap.add_argument("--out", type=Path, default=None, help="输出目录（默认: <input>/../samples_normalized）")
    ap.add_argument("--author", default="未知", help="作者/账号名（统一应用到所有样本）")
    ap.add_argument("--platform", default="未知", help="平台名（公众号/知乎/小红书/Twitter/X/博客/学术/个人散文/新闻媒体/其他）")
    args = ap.parse_args()

    input_dir: Path = args.input_dir
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"[error] input dir not found: {input_dir}", file=sys.stderr)
        return 2

    out_dir: Path = args.out if args.out else input_dir.parent / "samples_normalized"
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        p
        for p in input_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in {".md", ".markdown", ".txt", ".html", ".htm"}
    )

    if not files:
        print(f"[warn] no supported files found in {input_dir}", file=sys.stderr)
        return 1

    print(f"[info] found {len(files)} files. writing to {out_dir}")

    used_names: set[str] = set()
    success = 0
    for idx, src in enumerate(files, start=1):
        try:
            content, stem = normalize_one(src, author=args.author, platform=args.platform)
        except Exception as e:
            print(f"[skip] {src.name}: {e}", file=sys.stderr)
            continue

        name = f"{idx:03d}-{stem}.md"
        # 防止重名
        n = 2
        while name in used_names:
            name = f"{idx:03d}-{stem}-{n}.md"
            n += 1
        used_names.add(name)

        (out_dir / name).write_text(content, encoding="utf-8")
        success += 1
        print(f"  [{idx:03d}] {src.name} -> {name}")

    print(f"[done] {success}/{len(files)} normalized. output: {out_dir}")
    print("[hint] 请人工 review 一遍 frontmatter，特别是 platform / content_type 字段。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
