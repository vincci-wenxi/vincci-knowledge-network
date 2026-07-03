#!/usr/bin/env python3
"""
kn_status.py — 编码笔记 status 状态机自动流转 v2.5

实现 SKILL v2.5 第 3.4 节状态机：
  种子 → 萌芽 : 该编码笔记已有对应解码笔记（analysis_of 指向它）
  萌芽 → 成熟 : 该编码笔记派生的原子/原创笔记中，存在 ≥1 条双向链接
  归档        : 仅人工，脚本绝不自动置入

用法:
  python kn_status.py --vault <ROOT> check                 # 报告应流转的笔记
  python kn_status.py --vault <ROOT> advance [--apply]     # 执行正向流转

规则: 只正向流转，不回退；归档状态跳过不动。
"""
import argparse
import re
from pathlib import Path
from kn_common import (
    load_config, scan_notes, scan_all_knowledge, read_note, write_note,
    emit, STATUS_ORDER,
)

LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def get_code(fm, filename):
    """从 fm.code 或文件名提取 编码（如 DK-20250510-001@v1）。"""
    if fm.get("code"):
        return str(fm["code"])
    m = re.match(r"([A-Z]{2}-\d{8}-\d{3}@\w+)", filename)
    return m.group(1) if m else None


def build_decode_index(cfg):
    """返回被解码的编码集合：{被解码的 code}。"""
    decoded = scan_notes(cfg, "decoded")
    targets = set()
    for d in decoded:
        a = d["fm"].get("analysis_of")
        if a:
            targets.add(str(a))
    return targets


def build_linked_atomic(cfg):
    """
    v2.5: 返回已建立双链的笔记，映射回其 source_note(编码 code)。
    判定"双链"：该笔记 body 含 [[...]] 且被其他笔记反链。
    简化实现：笔记 body 中存在 [[...]] 即视为已织入网络（出链）。
    返回: set(编码 code) 表示这些编码已有成熟笔记。
    """
    # v2.5: 扫描原子笔记+原创库
    all_notes = scan_all_knowledge(cfg)
    
    # 先建立 文件名->是否有出链
    has_out = {}
    for n in all_notes:
        links = LINK_RE.findall(n["body"])
        has_out[Path(n["path"]).stem] = len(links) > 0
    
    # 反链：被任何笔记 [[]] 指向
    referenced = set()
    for n in all_notes:
        for tgt in LINK_RE.findall(n["body"]):
            referenced.add(tgt.split("|")[0].split("#")[0].strip())

    mature_codes = set()
    for n in all_notes:
        stem = Path(n["path"]).stem
        is_linked = has_out.get(stem) and (stem in referenced)
        if not is_linked:
            continue
        sn = n["fm"].get("source_note")
        if isinstance(sn, str):
            sn = [sn]
        for code in (sn or []):
            mature_codes.add(str(code))
    return mature_codes


def evaluate(cfg):
    notes = scan_notes(cfg, "encoded")
    decoded_targets = build_decode_index(cfg)
    mature_codes = build_linked_atomic(cfg)

    transitions = []
    for n in notes:
        fm = n["fm"]
        cur = fm.get("status", "种子")
        code = get_code(fm, n["filename"])
        if cur == "归档" or code is None:
            continue

        target = cur
        reason = None
        # 萌芽 → 成熟
        if cur in ("种子", "萌芽") and code in mature_codes:
            target = "成熟"
            reason = "派生笔记（原子/原创）已建立双向链接"
        # 种子 → 萌芽
        elif cur == "种子" and code in decoded_targets:
            target = "萌芽"
            reason = "已生成对应解码笔记"

        if target != cur and STATUS_ORDER.index(target) > STATUS_ORDER.index(cur):
            transitions.append({
                "path": n["path"], "code": code,
                "from": cur, "to": target, "reason": reason,
            })
    return transitions


def cmd_check(cfg):
    t = evaluate(cfg)
    emit({"command": "check", "pending_transitions": len(t), "transitions": t})


def cmd_advance(cfg, apply):
    t = evaluate(cfg)
    if apply:
        for item in t:
            fm, body, _ = read_note(item["path"])
            fm["status"] = item["to"]
            write_note(item["path"], fm, body)
    emit({
        "command": "advance", "applied": apply,
        "transitioned": len(t), "transitions": t,
        "note": "未加 --apply 则仅预览" if not apply else "已写入新 status",
    })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    a = sub.add_parser("advance"); a.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    cfg = load_config(args.vault)
    if args.cmd == "check":
        cmd_check(cfg)
    else:
        cmd_advance(cfg, args.apply)


if __name__ == "__main__":
    main()
