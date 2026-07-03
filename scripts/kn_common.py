"""
kn_common.py — 知识网络工作流共享工具库 v2.5
被各 CLI 脚本复用。无外部依赖（除 pyyaml）。
"""
import os
import re
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

# ---------- 配置加载 ----------

DEFAULT_CONFIG = {
    "atomic": "Obsidian Vault/03-Atomic",
    "original": "Obsidian Vault/04-原创",
    "encoded": "编码笔记",
    "decoded": "解码笔记",
    "registry": "Obsidian Vault/07-System/concept-registry.yaml",
}

# v2.5: 新增原创PREFIX（OT/OM/OC）
PREFIXES = ["TC", "TM", "TN", "OT", "OM", "OC"]
VERIFIED_PREFIXES = ["TC", "TM", "TN"]  # 已证实
ORIGINAL_PREFIXES = ["OT", "OM", "OC"]  # 原创

DISCIPLINE_CODES = ["LE", "DK", "AP", "CE", "PA", "LT", "XX"]
STATUS_ORDER = ["种子", "萌芽", "成熟", "归档"]


def load_config(vault_root):
    """读取 .knowledge-network-config.yaml，缺省用默认。"""
    root = Path(vault_root).expanduser()
    cfg_path = root / ".knowledge-network-config.yaml"
    cfg = dict(DEFAULT_CONFIG)
    if cfg_path.exists():
        with open(cfg_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        cfg.update(data.get("paths", {}))
    cfg["_root"] = str(root)
    return cfg


def abspath(cfg, key):
    path = Path(str(cfg[key])).expanduser()
    if path.is_absolute():
        return path
    return Path(cfg["_root"]) / path


def get_library_from_prefix(prefix):
    """v2.5: 根据PREFIX判断库归属"""
    if prefix in VERIFIED_PREFIXES:
        return "atomic"
    elif prefix in ORIGINAL_PREFIXES:
        return "original"
    return None


def get_form_from_prefix(prefix):
    """v2.5: 根据PREFIX判断形态"""
    form_map = {
        "TC": "术语", "TM": "思维模型", "TN": "概念",
        "OT": "术语", "OM": "思维模型", "OC": "概念",
    }
    return form_map.get(prefix)


# ---------- frontmatter ----------

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def read_note(path):
    """返回 (frontmatter_dict, body_str, raw_str)。无 fm 时 fm={}。"""
    raw = Path(path).read_text(encoding="utf-8")
    m = FM_RE.match(raw)
    if not m:
        return {}, raw, raw
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    body = raw[m.end():]
    return fm, body, raw


def write_note(path, fm, body):
    """写回 frontmatter + body。"""
    fm_str = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()
    content = f"---\n{fm_str}\n---\n{body}"
    Path(path).write_text(content, encoding="utf-8")


# ---------- 原子/原创笔记命名解析 ----------

# v2.5: 支持6种PREFIX
ATOMIC_NAME_RE = re.compile(r"^(TC|TM|TN|OT|OM|OC)-([A-Z]{2})-(.+)$")


def parse_atomic_filename(filename):
    """
    v2.5: 支持新PREFIX体系
    TC-CE-符号暴力.md -> {prefix, code, concept, library, form}
    兼容旧格式 TC-CE-001-符号暴力.md（剥离纯数字段）
    解析失败返回 None。
    """
    stem = Path(filename).stem
    m = ATOMIC_NAME_RE.match(stem)
    if not m:
        return None
    prefix, code, rest = m.groups()
    # 剥离旧格式的序号段 / @v1 后缀 / 原创标记 *
    rest = re.sub(r"^\d{3}-", "", rest)        # 去 001-
    rest = re.sub(r"@v?\d+$", "", rest)        # 去 @v1
    concept = rest.rstrip("*").replace("（原创）", "").strip()
    
    return {
        "prefix": prefix,
        "code": code,
        "concept": concept,
        "library": get_library_from_prefix(prefix),
        "form": get_form_from_prefix(prefix),
    }


def scan_atomic(cfg):
    """v2.5: 递归扫描 03-Atomic，返回所有原子笔记记录列表。"""
    root = abspath(cfg, "atomic")
    notes = []
    if not root.exists():
        return notes
    for p in root.rglob("*.md"):
        parsed = parse_atomic_filename(p.name)
        if not parsed:
            continue
        fm, body, _ = read_note(p)
        notes.append({
            "path": str(p),
            "filename": p.name,
            "prefix": parsed["prefix"],
            "code": parsed["code"],
            "concept": parsed["concept"],
            "library": parsed["library"],
            "form": parsed["form"],
            "fm": fm,
            "body": body,
        })
    return notes


def scan_original(cfg):
    """v2.5: 递归扫描 04-原创，返回所有原创笔记记录列表。"""
    root = abspath(cfg, "original")
    notes = []
    if not root.exists():
        return notes
    for p in root.rglob("*.md"):
        parsed = parse_atomic_filename(p.name)
        if not parsed:
            continue
        fm, body, _ = read_note(p)
        notes.append({
            "path": str(p),
            "filename": p.name,
            "prefix": parsed["prefix"],
            "code": parsed["code"],
            "concept": parsed["concept"],
            "library": parsed["library"],
            "form": parsed["form"],
            "fm": fm,
            "body": body,
        })
    return notes


def scan_all_knowledge(cfg):
    """v2.5: 扫描原子笔记+原创库，返回合并列表"""
    return scan_atomic(cfg) + scan_original(cfg)


# ---------- 编码/解码笔记扫描 ----------

def scan_notes(cfg, key):
    """扫描 编码笔记 或 解码笔记 目录。"""
    root = abspath(cfg, key)
    out = []
    if not root.exists():
        return out
    for p in root.rglob("*.md"):
        fm, body, _ = read_note(p)
        out.append({"path": str(p), "filename": p.name, "fm": fm, "body": body})
    return out


# ---------- 输出 ----------

def emit(report):
    """统一 JSON 输出（供 Claude Code 解析）。"""
    print(json.dumps(report, ensure_ascii=False, indent=2))


def today():
    return datetime.now().strftime("%Y-%m-%d")
