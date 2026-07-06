#!/bin/bash
# 文希知识网络 v2.5 一键创建脚本
# 使用方法：修改下方 VAULT_ROOT 为你的目标路径，然后运行 bash setup-vault.sh

# ==================== 配置 ====================
VAULT_ROOT="$HOME/文希知识网络"  # ⚠️ 请修改为你想要创建知识库的路径
# ===============================================

set -e  # 遇错退出

echo "🚀 开始创建文希知识网络 v2.5..."
echo "目标路径: $VAULT_ROOT"

# 创建主目录
mkdir -p "$VAULT_ROOT"

# 创建编码笔记（7学科）
echo "📝 创建编码笔记目录..."
mkdir -p "$VAULT_ROOT/编码笔记/01-LE-人生体验-LifeExperience"
mkdir -p "$VAULT_ROOT/编码笔记/02-DK-学科知识-DisciplineKnowledge"
mkdir -p "$VAULT_ROOT/编码笔记/03-AP-艺术感知-ArtisticPerception"
mkdir -p "$VAULT_ROOT/编码笔记/04-CE-认知进化-CognitiveEvolution"
mkdir -p "$VAULT_ROOT/编码笔记/05-PA-实践活动-PracticalActivity"
mkdir -p "$VAULT_ROOT/编码笔记/06-LT-文学创作-Literature"
mkdir -p "$VAULT_ROOT/编码笔记/07-XX-交叉学科-Interdisciplinary"

# 创建解码笔记（镜像7学科）
echo "🔍 创建解码笔记目录..."
mkdir -p "$VAULT_ROOT/解码笔记/01-LE-人生体验-LifeExperience"
mkdir -p "$VAULT_ROOT/解码笔记/02-DK-学科知识-DisciplineKnowledge"
mkdir -p "$VAULT_ROOT/解码笔记/03-AP-艺术感知-ArtisticPerception"
mkdir -p "$VAULT_ROOT/解码笔记/04-CE-认知进化-CognitiveEvolution"
mkdir -p "$VAULT_ROOT/解码笔记/05-PA-实践活动-PracticalActivity"
mkdir -p "$VAULT_ROOT/解码笔记/06-LT-文学创作-Literature"
mkdir -p "$VAULT_ROOT/解码笔记/07-XX-交叉学科-Interdisciplinary"

# 创建 Obsidian Vault 核心库
echo "📚 创建 Obsidian Vault 核心结构..."
mkdir -p "$VAULT_ROOT/Obsidian Vault/00-Inbox"
mkdir -p "$VAULT_ROOT/Obsidian Vault/01-Projects"
mkdir -p "$VAULT_ROOT/Obsidian Vault/02-Areas"

# 创建原子笔记（已证实）
echo "⚛️  创建原子笔记（已证实）目录..."
for discipline in CE DK LE LT AP PA XX; do
    mkdir -p "$VAULT_ROOT/Obsidian Vault/03-Atomic/TC-术语/TC-$discipline-${discipline}学科"
    mkdir -p "$VAULT_ROOT/Obsidian Vault/03-Atomic/TM-思维模型/TM-$discipline-${discipline}学科"
    mkdir -p "$VAULT_ROOT/Obsidian Vault/03-Atomic/TN-概念/TN-$discipline-${discipline}学科"
done
mkdir -p "$VAULT_ROOT/Obsidian Vault/03-Atomic/视图"

# 创建原创库
echo "💡 创建原创库目录..."
for discipline in CE DK LE LT AP PA XX; do
    mkdir -p "$VAULT_ROOT/Obsidian Vault/04-原创/OT-原创术语/OT-$discipline-${discipline}学科"
    mkdir -p "$VAULT_ROOT/Obsidian Vault/04-原创/OM-原创思维模型/OM-$discipline-${discipline}学科"
    mkdir -p "$VAULT_ROOT/Obsidian Vault/04-原创/OC-原创概念/OC-$discipline-${discipline}学科"
done

# 创建其他系统目录
echo "🔧 创建系统目录..."
mkdir -p "$VAULT_ROOT/Obsidian Vault/05-Resources"
mkdir -p "$VAULT_ROOT/Obsidian Vault/06-参考资料"
mkdir -p "$VAULT_ROOT/Obsidian Vault/07-System"
mkdir -p "$VAULT_ROOT/Obsidian Vault/08-Daily"
mkdir -p "$VAULT_ROOT/Obsidian Vault/09-MOC"
mkdir -p "$VAULT_ROOT/Obsidian Vault/10-MAP"
mkdir -p "$VAULT_ROOT/Obsidian Vault/11-Data"
mkdir -p "$VAULT_ROOT/Obsidian Vault/AI融合笔记"
mkdir -p "$VAULT_ROOT/Obsidian Vault/Templates"

# 创建 Output 和 Business
mkdir -p "$VAULT_ROOT/Output/公众号文章"
mkdir -p "$VAULT_ROOT/Output/视频脚本"
mkdir -p "$VAULT_ROOT/Output/社群内容"
mkdir -p "$VAULT_ROOT/Business"

# 创建概念注册表空文件
echo "📋 创建概念注册表..."
touch "$VAULT_ROOT/Obsidian Vault/07-System/concept-registry.yaml"

# 创建配置文件
echo "⚙️  创建配置文件..."
cat > "$VAULT_ROOT/.knowledge-network-config.yaml" << EOF
version: 2.5.0
paths:
  vault_root: "$VAULT_ROOT"
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
  atomic_note_format: "{prefix}-{code}-{concept}.md"
  original_note_format: "{prefix}-{code}-{concept}.md"
  encoding_note_format: "{code}-{date}-{seq}@{type}-{title}.md"
  decoding_note_format: "{code}-{date}-{seq}@解码-{title}-解码.md"
EOF

# 创建 README
cat > "$VAULT_ROOT/README.md" << EOF
# 文希知识网络 v2.5

这是你的个人知识管理系统。

## 快速开始

1. 用 Obsidian 打开这个文件夹（$VAULT_ROOT）
2. 开始在 \`编码笔记/\` 中记录你的想法
3. 使用 Python 脚本进行知识管理

## 目录说明

- \`编码笔记/\`: 手写/摘录笔记，按7学科分类
- \`解码笔记/\`: AI 解码后的笔记
- \`Obsidian Vault/03-Atomic/\`: 已被证实的知识（原子笔记）
- \`Obsidian Vault/04-原创/\`: 你自己创造的概念和框架
- \`Output/\`: 可发布的内容

## 工具脚本

参见项目 GitHub 仓库的 scripts/ 目录。

---

已证实归已证实，原创归原创。让知识有序生长。
EOF

echo ""
echo "✅ 文希知识网络 v2.5 创建完成！"
echo ""
echo "📍 位置: $VAULT_ROOT"
echo ""
echo "下一步："
echo "1. 用 Obsidian 打开: $VAULT_ROOT"
echo "2. 开始记录你的第一条编码笔记"
echo "3. 使用 Python 脚本管理知识网络"
echo ""
echo "🎉 祝知识管理愉快！"
