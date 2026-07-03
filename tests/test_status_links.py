import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from kn_common import load_config  # noqa: E402
from kn_status import build_linked_atomic  # noqa: E402


def write_markdown(path, frontmatter, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    path.write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8")


class StatusLinkTests(unittest.TestCase):
    def test_outgoing_link_alone_does_not_mark_source_as_mature(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            source_code = "DK-20260703-001@v1"
            write_markdown(
                vault / "Obsidian Vault" / "03-Atomic" / "TC-术语" / "TC-CE-符号暴力.md",
                {"source_note": source_code},
                "[[TN-CE-认知失调]]",
            )

            cfg = load_config(vault)

            self.assertNotIn(source_code, build_linked_atomic(cfg))

    def test_bidirectional_link_marks_source_as_mature(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            source_code = "DK-20260703-001@v1"
            write_markdown(
                vault / "Obsidian Vault" / "03-Atomic" / "TC-术语" / "TC-CE-符号暴力.md",
                {"source_note": source_code},
                "[[TN-CE-认知失调]]",
            )
            write_markdown(
                vault / "Obsidian Vault" / "03-Atomic" / "TN-概念" / "TN-CE-认知失调.md",
                {},
                "[[TC-CE-符号暴力]]",
            )

            cfg = load_config(vault)

            self.assertIn(source_code, build_linked_atomic(cfg))


if __name__ == "__main__":
    unittest.main()
