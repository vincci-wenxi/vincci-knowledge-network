#!/usr/bin/env python3
"""
kn_links.py — 幽灵链接（ghost link）检测与修复 v2.5

幽灵链接 = [[X]] 指向的笔记在库中不存在。
本脚本检测全库 wikilink，并对可自动修复的情况给出/执行修复：
  - 旧格式残留: [[TC-CE-符号暴力@v1]] -> [[TC-CE-符号暴力]]
  - 带序号残留: [[TC-CE-001-符号暴力]] -> [[TC-CE-符号暴力]]
  - 模糊匹配:   [[符号暴力]] -> [[TC-CE-符号暴力]]（库中唯一同名概念时）

用法:
  python kn_links.py --vault <ROOT> check                # 仅报告
  python kn_links.py --vault <ROOT> fix [--apply]        # 修复（默认 dry-run）

不可自动修复的（多候选/无候选）只报告，交人工。
"""
import argparse
import re
from pathlib import Path
from kn_common import load_config, read_note, write_note, abspath, emit

LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def all_md_files(cfg):
    root = Path(cfg["_root"])
    # v2.5: 扫描四大区：原子、原创、编码、解码 + Obsidian Vault 整体
    targets = [
        abspath(cfg, "atomic"),
        abspath(cfg, "original"),  # 新增
        abspath(cfg, "encoded"),
        abspath(cfg, "decoded")
    ]
    vault = Path(cfg["_root"]) / "Obsidian Vault"
    if vault.exists():
        targets.append(vault)
    seen = set()
    files = []
    for t in targets:
        if not Path(t).exists():
            continue
        for p in Path(t).rglob("*.md"):
            if str(p) not in seen:
                seen.add(str(p))
                files.append(p)
    return files


def normalize_link(target):
    """v2.5: 剥离旧格式: @v1 后缀、001- 序号，支持6种PREFIX。"""
    t = target.split("|")[0].split("#")[0].strip()
    t = re.sub(r"@v?\d+$", "", t)
    # v2.5: 支持新PREFIX
    t = re.sub(r"^(TC|TM|TN|OT|OM|OC)-([A-Z]{2})-\d{3}-", r"\1-\2-", t)
    return t


def cmd(cfg, do_fix, apply):
    files = all_md_files(cfg)
    # 库内所有可被链接的笔记 stem
    existing = {p.stem for p in files}
    # 概念名 -> 完整 stem 索引（用于模糊匹配）
    concept_index = {}
    for stem in existing:
        # v2.5: 支持6种PREFIX
        m = re.match(r"^(TC|TM|TN|OT|OM|OC)-([A-Z]{2})-(.+)$", stem)
        if m:
            concept_index.setdefault(m.group(3).rstrip("*"), []).append(stem)

    ghosts, fixes, unresolved = [], [], []

    for p in files:
        fm, body, raw = read_note(p)
        changed = False
        new_raw = raw
        for match in LINK_RE.finditer(raw):
            target = match.group(1)
            base = target.split("|")[0].split("#")[0].strip()
            if base in existing:
                continue  # 正常链接
            # 是幽灵链接，尝试修复
            norm = normalize_link(target)
            resolved = None
            if norm in existing:
                resolved = norm
            elif base in concept_index and len(concept_index[base]) == 1:
                resolved = concept_index[base][0]  # 唯一同名概念
            elif norm in concept_index and len(concept_index[norm]) == 1:
                resolved = concept_index[norm][0]

            if resolved:
                fixes.append({"file": str(p), "from": base, "to": resolved})
                new_raw = new_raw.replace(f"[[{base}", f"[[{resolved}")
                changed = True
            else:
                ghosts.append({"file": str(p), "link": base})
                cand = concept_index.get(base) or concept_index.get(norm) or []
                unresolved.append({"file": str(p), "link": base,
                                   "candidates": cand})

        if do_fix and apply and changed:
            p.write_text(new_raw, encoding="utf-8")

    emit({
        "command": "fix" if do_fix else "check",
        "applied": apply if do_fix else False,
        "scanned_files": len(files),
        "auto_fixable": len(fixes),
        "fixes": fixes,
        "unresolved_ghosts": len(unresolved),
        "unresolved": unresolved,
        "note": ("仅报告，未写盘" if not (do_fix and apply)
                 else "可自动修复项已写入；unresolved 需人工处理"),
    })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    f = sub.add_parser("fix"); f.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    cfg = load_config(args.vault)
    cmd(cfg, do_fix=(args.cmd == "fix"), apply=getattr(args, "apply", False))


if __name__ == "__main__":
    main()
