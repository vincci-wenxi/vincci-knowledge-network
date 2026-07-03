#!/usr/bin/env python3
"""Cross-platform vault creation for Vincci Knowledge Network v2.5."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from textwrap import dedent


DEFAULT_VAULT_ROOT = "~/文希知识库"

DISCIPLINES = [
    ("LE", "人生体验-LifeExperience"),
    ("DK", "学科知识-DisciplineKnowledge"),
    ("AP", "艺术感知-ArtisticPerception"),
    ("CE", "认知进化-CognitiveEvolution"),
    ("PA", "实践活动-PracticalActivity"),
    ("LT", "文学创作-Literature"),
    ("XX", "交叉学科-Interdisciplinary"),
]

ATOMIC_FORMS = [
    ("TC", "术语"),
    ("TM", "思维模型"),
    ("TN", "概念"),
]

ORIGINAL_FORMS = [
    ("OT", "原创术语"),
    ("OM", "原创思维模型"),
    ("OC", "原创概念"),
]


def normalize_vault_root(vault_root: str | os.PathLike[str]) -> Path:
    return Path(vault_root).expanduser()


def write_text(path: Path, content: str) -> None:
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def yaml_single_quote(value: str | os.PathLike[str]) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def create_vault(vault_root: str | os.PathLike[str]) -> Path:
    root = normalize_vault_root(vault_root)
    root.mkdir(parents=True, exist_ok=True)

    for index, (code, label) in enumerate(DISCIPLINES, start=1):
        (root / "编码笔记" / f"{index:02d}-{code}-{label}").mkdir(parents=True, exist_ok=True)
        (root / "解码笔记" / f"{index:02d}-{code}-{label}").mkdir(parents=True, exist_ok=True)

    for path in [
        "Obsidian Vault/00-Inbox",
        "Obsidian Vault/01-Projects",
        "Obsidian Vault/02-Areas",
        "Obsidian Vault/03-Atomic/视图",
        "Obsidian Vault/05-Resources",
        "Obsidian Vault/06-参考资料",
        "Obsidian Vault/07-System",
        "Obsidian Vault/08-Daily",
        "Obsidian Vault/09-MOC",
        "Obsidian Vault/10-MAP",
        "Obsidian Vault/11-Data",
        "Obsidian Vault/AI融合笔记",
        "Obsidian Vault/Templates",
        "Output/公众号文章",
        "Output/视频脚本",
        "Output/社群内容",
        "Business",
    ]:
        (root / path).mkdir(parents=True, exist_ok=True)

    for code, _label in DISCIPLINES:
        for prefix, form in ATOMIC_FORMS:
            (root / "Obsidian Vault" / "03-Atomic" / f"{prefix}-{form}" / f"{prefix}-{code}-{code}学科").mkdir(
                parents=True,
                exist_ok=True,
            )
        for prefix, form in ORIGINAL_FORMS:
            (root / "Obsidian Vault" / "04-原创" / f"{prefix}-{form}" / f"{prefix}-{code}-{code}学科").mkdir(
                parents=True,
                exist_ok=True,
            )

    registry = root / "Obsidian Vault" / "07-System" / "concept-registry.yaml"
    registry.touch(exist_ok=True)

    write_text(
        root / ".knowledge-network-config.yaml",
        f"""
        version: 2.5.0
        paths:
          vault_root: {yaml_single_quote(root)}
          inbox: "Obsidian Vault/00-Inbox"
          atomic: "Obsidian Vault/03-Atomic"
          original: "Obsidian Vault/04-原创"
          encoded: "编码笔记"
          decoded: "解码笔记"
          output: "Output"
          resources: "Obsidian Vault/05-Resources"
          ai_fusion: "Obsidian Vault/AI融合笔记"
          registry: "Obsidian Vault/07-System/concept-registry.yaml"
          map: "Obsidian Vault/10-MAP/知识网络图"

        rules:
          encoding_note_subdir_threshold: 20
          ai_collaboration_review_days: 7
          external_archive_days: 30

        naming:
          atomic_note_format: "{{prefix}}-{{code}}-{{concept}}.md"
          original_note_format: "{{prefix}}-{{code}}-{{concept}}.md"
          encoding_note_format: "{{code}}-{{date}}-{{seq}}@{{type}}-{{title}}.md"
          decoding_note_format: "{{code}}-{{date}}-{{seq}}@解码-{{title}}-解码.md"
        """,
    )

    write_text(
        root / "README.md",
        f"""
        # 文希知识库 v2.5

        这是你的个人知识管理系统。

        ## 快速开始

        1. 用 Obsidian 打开这个文件夹（{root}）
        2. 开始在 `编码笔记/` 中记录你的想法
        3. 使用 Python 脚本进行知识管理

        ## 目录说明

        - `编码笔记/`: 手写/摘录笔记，按7学科分类
        - `解码笔记/`: AI 解码后的笔记
        - `Obsidian Vault/03-Atomic/`: 已被证实的知识（原子笔记）
        - `Obsidian Vault/04-原创/`: 你自己创造的概念和框架
        - `Output/`: 可发布的内容

        ## 工具脚本

        参见项目 GitHub 仓库的 `scripts/` 目录。

        ---

        已证实归已证实，原创归原创。让知识有序生长。
        """,
    )

    return root


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Vincci Knowledge Network vault.")
    parser.add_argument(
        "--vault",
        default=os.environ.get("VAULT_ROOT", DEFAULT_VAULT_ROOT),
        help="Target vault root. Defaults to VAULT_ROOT or ~/文希知识库.",
    )
    args = parser.parse_args()

    root = create_vault(args.vault)
    print(f"文希知识库 v2.5 创建完成: {root}")
    print("下一步：用 Obsidian 打开这个文件夹，并开始记录第一条编码笔记。")


if __name__ == "__main__":
    main()
