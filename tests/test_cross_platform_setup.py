import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from kn_common import load_config  # noqa: E402
from setup_vault import create_vault  # noqa: E402


class CrossPlatformSetupTests(unittest.TestCase):
    def test_load_config_expands_home_directory(self):
        with tempfile.TemporaryDirectory() as home:
            vault = Path(home) / "文希知识库"
            vault.mkdir()
            (vault / ".knowledge-network-config.yaml").write_text(
                yaml.safe_dump({"paths": {"encoded": "编码笔记"}}, allow_unicode=True),
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"HOME": home, "USERPROFILE": home}, clear=False):
                cfg = load_config("~/文希知识库")

            self.assertEqual(Path(cfg["_root"]), vault)
            self.assertEqual(cfg["encoded"], "编码笔记")

    def test_create_vault_builds_expected_structure_and_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "Windows Vault"

            create_vault(vault)

            expected_paths = [
                vault / "编码笔记" / "01-LE-人生体验-LifeExperience",
                vault / "解码笔记" / "07-XX-交叉学科-Interdisciplinary",
                vault / "Obsidian Vault" / "03-Atomic" / "TC-术语" / "TC-CE-CE学科",
                vault / "Obsidian Vault" / "04-原创" / "OC-原创概念" / "OC-XX-XX学科",
                vault / "Obsidian Vault" / "07-System" / "concept-registry.yaml",
                vault / "Output" / "公众号文章",
                vault / ".knowledge-network-config.yaml",
                vault / "README.md",
            ]
            for path in expected_paths:
                self.assertTrue(path.exists(), f"missing {path}")

            cfg = yaml.safe_load((vault / ".knowledge-network-config.yaml").read_text(encoding="utf-8"))
            self.assertEqual(cfg["paths"]["vault_root"], str(vault))
            self.assertEqual(cfg["paths"]["encoded"], "编码笔记")

    def test_powershell_wrapper_source_is_ascii_safe(self):
        (ROOT / "setup-vault.ps1").read_bytes().decode("ascii")


if __name__ == "__main__":
    unittest.main()
