#!/usr/bin/env python3
"""
kn_dedup.py — 原子笔记去重检测 + 概念注册表同步 v2.5

实现 SKILL v2.5 第七章「提取与去重规则」。

用法:
  # 全库扫描，报告所有重复（不写盘）
  python kn_dedup.py --vault <ROOT> scan

  # 检查某个待提取概念是否已存在
  python kn_dedup.py --vault <ROOT> check --concept 符号暴力

  # 重建概念注册表（按全库现状，--apply 写盘）
  python kn_dedup.py --vault <ROOT> sync-registry [--apply]

输出: JSON 报告。所有写操作需 --apply，否则 dry-run。
"""
import argparse
import yaml
from pathlib import Path
from collections import defaultdict
from kn_common import (
    load_config, scan_all_knowledge, abspath, emit, today,
)


def detect_duplicates(notes):
    """
    v2.5: 按概念名分组，识别四类重复：
      cross_library  同概念跨库（atomic vs original）⚠️ 最重要的新规则
      cross_type     同概念不同形态 (术语/思维模型/概念)
      cross_disc     同概念不同学科
      same           完全同名（应合并）
    """
    by_concept = defaultdict(list)
    for n in notes:
        by_concept[n["concept"]].append(n)

    issues = []
    for concept, group in by_concept.items():
        if len(group) == 1:
            continue
        
        libraries = {g["library"] for g in group}
        forms = {g["form"] for g in group}
        discs = {g["code"] for g in group}
        kind = []
        
        # v2.5 新规则：跨库检测（最高优先级）
        if len(libraries) > 1:
            kind.append("cross_library")
        
        if len(forms) > 1:
            kind.append("cross_type")
        if len(discs) > 1:
            kind.append("cross_disc")
        if len(libraries) == 1 and len(forms) == 1 and len(discs) == 1:
            kind.append("same")
        
        # 检测"1"后缀污染
        suffix_polluted = [g["filename"] for g in group
                           if g["concept"].rstrip().endswith(("1", "2", "3"))]
        
        issues.append({
            "concept": concept,
            "kind": kind,
            "count": len(group),
            "files": [{"filename": g["filename"], "prefix": g["prefix"],
                       "code": g["code"], "library": g["library"], 
                       "form": g["form"], "path": g["path"]} for g in group],
            "suffix_polluted": suffix_polluted,
            "suggestion": _suggest(kind),
        })
    return issues


def _suggest(kind):
    if "cross_library" in kind:
        return "⚠️ 跨库冲突：一个在原子笔记、一个在原创库，需人工确认是否误判归类"
    if "same" in kind:
        return "合并更新到单一文件，追加 source_note，不创建新文件"
    if "cross_type" in kind:
        return "按本质判断形态：术语/思维模型/概念"
    if "cross_disc" in kind:
        return "查注册表确定主学科，其余作为跨学科实例整合到主版本"
    return "人工确认"


def build_registry(notes):
    """v2.5: 按全库现状生成注册表。同概念多条时，取最早 created 作为主版本。"""
    by_concept = defaultdict(list)
    for n in notes:
        by_concept[n["concept"]].append(n)

    registry = {}
    for concept, group in by_concept.items():
        # 主版本选择：优先原创 > 最早 created
        def sort_key(g):
            created = str(g["fm"].get("created", "9999"))
            is_orig = bool(g["fm"].get("is_original", False))
            # 原创优先（is_orig=True 排前），再按 created 升序
            return (not is_orig, created)
        
        primary = sorted(group, key=sort_key)[0]
        
        # v2.5: 新增 library 和 form 字段
        registry[concept] = {
            "library": primary["library"],
            "primary_discipline": primary["code"],
            "primary_version": primary["filename"],
            "form": primary["form"],
            "prefix": primary["prefix"],
            "first_seen": str(primary["fm"].get("created", today())),
            "is_original": bool(primary["fm"].get("is_original", False)),
        }
    return registry


def cmd_scan(cfg):
    notes = scan_all_knowledge(cfg)
    issues = detect_duplicates(notes)
    emit({
        "command": "scan",
        "total_notes": len(notes),
        "atomic_notes": len([n for n in notes if n["library"] == "atomic"]),
        "original_notes": len([n for n in notes if n["library"] == "original"]),
        "duplicate_groups": len(issues),
        "issues": issues,
        "action_required": bool(issues),
    })


def cmd_check(cfg, concept):
    notes = scan_all_knowledge(cfg)
    matches = [n for n in notes if concept in n["concept"]]
    registry = _load_registry(cfg)
    reg_entry = registry.get(concept)
    
    emit({
        "command": "check",
        "concept": concept,
        "exists": bool(matches),
        "matches": [{"filename": m["filename"], "prefix": m["prefix"],
                     "code": m["code"], "library": m["library"],
                     "form": m["form"], "path": m["path"]} for m in matches],
        "registry_entry": reg_entry,
        "verdict": (
            "已存在→走合并/确认流程" if matches
            else "全新概念→可创建，创建后须写入注册表"
        ),
    })


def _load_registry(cfg):
    path = abspath(cfg, "registry")
    if not Path(path).exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def cmd_sync_registry(cfg, apply):
    notes = scan_all_knowledge(cfg)
    new_registry = build_registry(notes)
    old_registry = _load_registry(cfg)

    added = [k for k in new_registry if k not in old_registry]
    changed = [k for k in new_registry
               if k in old_registry and old_registry[k] != new_registry[k]]
    removed = [k for k in old_registry if k not in new_registry]

    if apply:
        path = abspath(cfg, "registry")
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(new_registry, f, allow_unicode=True, sort_keys=True)

    emit({
        "command": "sync-registry",
        "applied": apply,
        "registry_path": cfg["registry"],
        "total_concepts": len(new_registry),
        "added": added,
        "changed": changed,
        "removed_stale": removed,
        "note": "未加 --apply 则仅 dry-run，未写盘" if not apply else "已写入注册表",
    })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scan")
    c = sub.add_parser("check"); c.add_argument("--concept", required=True)
    s = sub.add_parser("sync-registry"); s.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    cfg = load_config(args.vault)
    if args.cmd == "scan":
        cmd_scan(cfg)
    elif args.cmd == "check":
        cmd_check(cfg, args.concept)
    elif args.cmd == "sync-registry":
        cmd_sync_registry(cfg, args.apply)


if __name__ == "__main__":
    main()
