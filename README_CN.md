# 📚 文希知识网络 v2.5 - 完整使用指南

## 🎯 项目简介

这是一个完整的 **Obsidian 知识管理系统**，实现了编码-解码-原子化的三段式知识加工流程。

### 核心特色

🌟 **原子笔记与原创库分离** - 已证实的知识与原创概念物理隔离  
📝 **7学科分类体系** - LE/DK/AP/CE/PA/LT/XX 完整覆盖  
🤖 **AI辅助工作流** - 从编码到知识图谱全流程支持  
🔧 **Python自动化工具** - 去重、修链、状态流转一键完成  
📖 **完善的文档** - 20+ FAQ + 详细教程

---

## 🚀 10分钟快速开始

### 准备工作

```bash
# 确认 Python 版本
python3 --version  # 需要 3.7+

# 克隆项目
git clone https://github.com/YOUR_USERNAME/vincci-knowledge-network.git
cd vincci-knowledge-network

# 安装依赖
pip3 install -r requirements.txt
```

### 创建知识库

```bash
# 1. 编辑建库脚本，修改目标路径（第6行）
nano setup-vault.sh
# 将 VAULT_ROOT="$HOME/文希知识库" 改为你想要的路径

# 2. 运行建库脚本
bash setup-vault.sh

# 3. 配置路径
cp config-template.yaml .knowledge-network-config.yaml
nano .knowledge-network-config.yaml  # 填入你的 vault_root
```

### 用 Obsidian 打开

1. 启动 Obsidian
2. 打开文件夹：选择你在上面设置的 `VAULT_ROOT` 路径
3. 开始记录你的第一条笔记！

---

## 📁 目录结构一览

```
文希知识库/
├── 编码笔记/          📝 手写笔记，按7学科分类
│   ├── 01-LE-人生体验/
│   ├── 02-DK-学科知识/
│   ├── 03-AP-艺术感知/
│   ├── 04-CE-认知进化/
│   ├── 05-PA-实践活动/
│   ├── 06-LT-文学创作/
│   └── 07-XX-交叉学科/
│
├── 解码笔记/          🔍 AI解码分析
│   └── （镜像7学科）
│
├── Obsidian Vault/
│   ├── 03-Atomic/     ⚛️ 原子笔记（已证实）
│   │   ├── TC-术语/
│   │   ├── TM-思维模型/
│   │   └── TN-概念/
│   │
│   ├── 04-原创/       💡 原创库（你的创造）
│   │   ├── OT-原创术语/
│   │   ├── OM-原创思维模型/
│   │   └── OC-原创概念/
│   │
│   └── 07-System/
│       └── concept-registry.yaml  📋 概念注册表
│
└── Output/            📤 可发布内容
```

---

## 🛠️ 工具脚本速查

### 去重检测

```bash
# 扫描全库，查找重复概念
python scripts/kn_dedup.py --vault ~/文希知识库 scan

# 检查单个概念是否已存在
python scripts/kn_dedup.py --vault ~/文希知识库 check --concept 符号暴力

# 重建概念注册表（先预览）
python scripts/kn_dedup.py --vault ~/文希知识库 sync-registry

# 确认无误后写入
python scripts/kn_dedup.py --vault ~/文希知识库 sync-registry --apply
```

### 链接修复

```bash
# 检查幽灵链接（断链）
python scripts/kn_links.py --vault ~/文希知识库 check

# 自动修复
python scripts/kn_links.py --vault ~/文希知识库 fix --apply
```

### 状态管理

```bash
# 检查可流转的笔记
python scripts/kn_status.py --vault ~/文希知识库 check

# 自动流转状态（种子→萌芽→成熟）
python scripts/kn_status.py --vault ~/文希知识库 advance --apply
```

---

## 📝 命名规范速查

### 编码笔记

```
格式：CODE-YYYYMMDD-SEQ@TYPE-标题.md
示例：DK-20250510-001@v1-读《思考快与慢》笔记.md
```

| 部分 | 说明 | 示例 |
|------|------|------|
| CODE | 学科代码 | DK, CE, LE... |
| YYYYMMDD | 创建日期 | 20250510 |
| SEQ | 当日序号 | 001 |
| TYPE | 版本类型 | v1, draft, final |

### 原子笔记（已证实）

```
格式：PREFIX-CODE-概念名.md
示例：TC-CE-符号暴力.md
```

| PREFIX | 含义 | 示例 |
|--------|------|------|
| TC | 已证实术语 | TC-CE-符号暴力.md |
| TM | 已证实思维模型 | TM-DK-第一性原理.md |
| TN | 已证实概念 | TN-CE-认知失调.md |

### 原创笔记

```
格式：PREFIX-CODE-概念名.md
示例：OC-CE-框架觉知.md
```

| PREFIX | 含义 | 示例 |
|--------|------|------|
| OT | 原创术语 | OT-CE-新术语.md |
| OM | 原创思维模型 | OM-CE-AB面分析.md |
| OC | 原创概念 | OC-CE-框架觉知.md |

---

## 🔤 学科代码速查

| 代码 | 中文 | English |
|:---:|------|---------|
| LE | 人生体验 | Life Experience |
| DK | 学科知识 | Discipline Knowledge |
| AP | 艺术感知 | Artistic Perception |
| CE | 认知进化 | Cognitive Evolution |
| PA | 实践活动 | Practical Activity |
| LT | 文学创作 | Literature |
| XX | 交叉学科 | Interdisciplinary |

---

## 🔄 工作流程图

```
1. 编码阶段
   ↓
   手写笔记 → 编码笔记（status=种子）
   存放：编码笔记/XX-学科/

2. 解码阶段
   ↓
   AI 7维度分析 → 解码笔记 + 提取知识单元
   |
   ├→ 已证实知识 → 03-Atomic/（TC/TM/TN）
   └→ 原创内容 → 04-原创/（OT/OM/OC）
   
   status → 萌芽

3. 知识图谱
   ↓
   建立双向链接 → Canvas可视化
   
   status → 成熟
```

---

## 💡 最佳实践

### 每日流程

**早晨** ☀️
- 在 `编码笔记/` 写新想法/读书摘要
- 使用简洁的标题和标签

**下午** 🌤️
- 运行 AI 解码分析
- 审阅提取的概念

**晚上** 🌙
- 运行维护脚本
- 检查重复和链接

### 每周维护

**周末** 🎯
- 运行 `@知识图谱` 建立联系
- 归档过时内容
- 备份概念注册表

---

## 📚 详细文档

| 文档 | 内容 |
|------|------|
| [SKILL-v2_5.md](docs/SKILL-v2_5.md) | 完整工作流规范 |
| [FAQ.md](docs/FAQ.md) | 20+ 常见问题解答 |
| [文希·Obsidian知识库文件架构v2.5.md](docs/文希·Obsidian知识库文件架构v2.5.md) | 架构详解 |
| [v2.5改动说明](docs/文希·v2.5改动说明与脚本调整指引.md) | 版本变更 |
| [GITHUB_SETUP.md](GITHUB_SETUP.md) | GitHub 上传指南 |
| [立即上传到GitHub.md](立即上传到GitHub.md) | 快速上传流程 |

---

## ❓ 快速答疑

<details>
<summary><b>Q: v2.5 和 v2.4 有什么区别？</b></summary>

核心区别是**物理分离**：
- v2.4: 原子笔记混装（TC/CC/MM）
- v2.5: 已证实（TC/TM/TN）与原创（OT/OM/OC）分离
- 新增 `04-原创/` 独立库

</details>

<details>
<summary><b>Q: 什么算"已证实"，什么算"原创"？</b></summary>

**已证实**：有权威学术来源、被广泛验证（如：符号暴力、第一性原理）  
**原创**：你自己创造的概念、方法论（如：你的AB面分析框架）

AI 拿不准时会询问你。

</details>

<details>
<summary><b>Q: 脚本安全吗？会覆盖我的文件吗？</b></summary>

安全！所有脚本默认 **dry-run 模式**（预览）：
- 不加 `--apply` = 只报告，不写盘
- 加 `--apply` = 真正修改

建议：首次运行先不加 `--apply`，确认无误再加。

</details>

<details>
<summary><b>Q: 如何从 v2.4 迁移？</b></summary>

运行迁移脚本（开发中）：
```bash
python scripts/migrate_v24_to_v25.py --vault ~/文希知识库 --apply
```

或参考 [v2.5改动说明](docs/文希·v2.5改动说明与脚本调整指引.md) 手动迁移。

</details>

<details>
<summary><b>Q: 遇到问题怎么办？</b></summary>

1. 查看 [FAQ.md](docs/FAQ.md)
2. 提交 [GitHub Issue](https://github.com/YOUR_USERNAME/vincci-knowledge-network/issues)
3. 加入文希AI社区讨论

</details>

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

### 如何贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交改动 (`git commit -m 'feat: 添加某某功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License © 2026 众推客科技 · 文希AI社区

---

## 🌟 Star History

如果这个项目对你有帮助，请给个 Star ⭐

---

## 📞 联系我们

- 众推客科技
- 文希AI社区
- #AI搭子圈

---

**让知识有序生长，已证实归已证实，原创归原创。** 🌱
