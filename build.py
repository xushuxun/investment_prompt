#!/usr/bin/env python3
"""
扫描 reports/ 目录，生成 reports.json 目录索引。
运行一次即可：python build.py
"""
import json
import re
from pathlib import Path

REPORTS_DIR = Path("reports")
OUTPUT = Path("reports.json")


def extract_title(md: str, filename: str) -> str:
    # 优先取第一个 # 标题
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # 否则用文件名（去掉扩展名）
    return filename.removesuffix(".md")


def build_index():
    reports = []
    if not REPORTS_DIR.exists():
        raise SystemExit(f"目录不存在: {REPORTS_DIR}")

    for path in sorted(REPORTS_DIR.glob("*.md")):
        md = path.read_text(encoding="utf-8")
        title = extract_title(md, path.name)
        reports.append({
            "file": path.name,
            "title": title,
        })

    OUTPUT.write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已生成 {OUTPUT}，共 {len(reports)} 篇报告")


if __name__ == "__main__":
    build_index()
