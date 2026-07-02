# 常见问题 FAQ

## 基础概念

### Q1: v2.5 和 v2.4 有什么区别？

**核心区别**：v2.5 将原子笔记（已证实）和原创库（新创）物理分离。

| 维度 | v2.4 | v2.5 |
|------|------|------|
| 原子笔记 | 混装 TC/CC/MM | 仅已证实（TC/TM/TN） |
| 原创内容 | 混在 03-Atomic | 独立成 04-原创（OT/OM/OC） |
| PREFIX | 3种 | 6种 |

### Q2: 什么算"已证实"，什么算"原创"？

**已证实**：
- 有权威学术来源
- 有行业标准定义
- 被广泛研究和验证
- 例：符号暴力（布迪厄）、第一性原理、SWOT分析

**原创**：
- 你自己创造的概念
- 你总结的独特方法论
- 你提出的新框架
- 例：你的"AB面分析框架"、"框架觉知"概念

**原则**：AI 拿不准时必须问你，不擅自归类。

### Q3: 为什么要分离原子笔记和原创库？

三个原因：

1. **检索清晰**：找已证实知识时不被原创内容干扰
2. **知识产权**：原创内容可独立管理、导出、商业化
3. **学习路径**：看原子笔记=学习前人成果，看原创库=复盘自己创新

## 命名规范

### Q4: PREFIX 是什么意思？

PREFIX 是文件名开头的两个字母，表示笔记的**库归属**和**形态**：

**已证实**（T = Trusted/Tested）
- `TC` = 已证实术语
- `TM` = 已证实思维模型  
- `TN` = 已证实概念

**原创**（O = Original）
- `OT` = 原创术语
- `OM` = 原创思维模型
- `OC` = 原创概念

### Q5: 如何判断一个知识单元是"术语"、"思维模型"还是"概念"？

决策树：

```
是已有明确来源的学术/行业术语？（有英文原名、独立词条）
├── 是 → 术语（TC/OT）
└── 否 → 是可复用的方法论/操作框架？（名称含框架/模型/方法，有操作步骤）
    ├── 是 → 思维模型（TM/OM）
    └── 否 → 概念（TN/OC）
```

**示例**：
- 术语：符号暴力、认知负荷、刻意练习
- 思维模型：第一性原理、SWOT分析、PDCA循环
- 概念：认知失调、心流、成长型思维

### Q6: 文件名里能不能有序号（001-）或版本号（@v1）？

**不能**。v2.5 禁止在原子/原创笔记文件名中使用：
- 序号：`TC-CE-001-符号暴力.md` ❌
- 版本号：`TC-CE-符号暴力@v1.md` ❌

正确格式：`TC-CE-符号暴力.md` ✅

旧格式会被 `kn_links.py` 检测为幽灵链接并提示修复。

## 工作流

### Q7: 编码→解码→原子化的流程是什么？

```
1. @编码：手写笔记 → 生成编码笔记（status=种子）
2. @解码：AI 7维度分析 → 生成解码笔记 + 提取原子/原创笔记（status→萌芽）
3. @知识图谱：建立双向链接 → 更新 Canvas（status→成熟）
```

### Q8: status 状态机如何流转？

| 状态 | 触发条件 | 谁操作 |
|------|---------|--------|
| 种子 | 编码笔记刚创建 | AI 自动 |
| 萌芽 | 已生成解码笔记+提取笔记 | AI 自动 |
| 成熟 | 派生笔记建立≥1条双链 | AI 自动 |
| 归档 | 过时/不再关注 | **用户手动** |

运行 `python kn_status.py --vault <ROOT> advance --apply` 自动流转。

### Q9: 同一个概念在原子笔记和原创库都有怎么办？

**这是重要边界！** `kn_dedup.py scan` 会检测并报告 `cross_library` 冲突。

可能原因：
1. 把已证实误判为原创
2. 把原创误判为已证实
3. 你在已有概念基础上提出了新解释（需改名区分）

**处理**：人工确认后，保留一个，删除或迁移另一个。

## 脚本使用

### Q10: 脚本执行顺序是什么？

**首次使用**：
```bash
# 1. 建库
bash setup-vault.sh

# 2. 初始化注册表（干跑预览）
python scripts/kn_dedup.py --vault <ROOT> sync-registry

# 3. 确认无误后写入
python scripts/kn_dedup.py --vault <ROOT> sync-registry --apply
```

**日常维护**：
```bash
# 1. 检查去重
python scripts/kn_dedup.py --vault <ROOT> scan

# 2. 修复链接
python scripts/kn_links.py --vault <ROOT> fix --apply

# 3. 更新状态
python scripts/kn_status.py --vault <ROOT> advance --apply
```

### Q11: --apply 和不加 --apply 有什么区别？

- **不加**：dry-run（干跑），只报告不写盘，安全预览
- **加了**：真正写入文件，不可撤销

**建议**：首次运行脚本时先不加 `--apply`，确认无误再加。

### Q12: 如何检查某个概念是否已存在？

```bash
python scripts/kn_dedup.py --vault <ROOT> check --concept 符号暴力
```

返回：
- 是否存在
- 在哪个库（atomic/original）
- 主学科
- 文件路径

## 迁移

### Q13: 如何从 v2.4 迁移到 v2.5？

当前仓库尚未提供自动迁移脚本，建议先备份知识库，再按下面步骤手动迁移。

**手动迁移**：
1. 扫描 `03-Atomic/` 下所有笔记
2. 读取 frontmatter 的 `is_original` 字段
3. `is_original: true` → 迁移到 `04-原创/`，改PREFIX（CC→OC, MM→OM）
4. `is_original: false` → 留在 `03-Atomic/`，改PREFIX（CC→TN, MM→TM）

### Q14: 旧笔记文件名有 @v1 后缀怎么办？

运行链接修复脚本会自动处理：
```bash
python scripts/kn_links.py --vault <ROOT> fix --apply
```

或手动批量重命名：
```bash
cd "Obsidian Vault/03-Atomic"
find . -name "*@v*.md" -exec rename 's/@v\d+//' {} \;
```

## 故障排查

### Q15: 脚本报错 "ModuleNotFoundError: No module named 'yaml'"

安装依赖：
```bash
pip install pyyaml
# 或
pip install -r requirements.txt
```

### Q16: 概念注册表损坏了怎么办？

重建注册表：
```bash
# 备份旧文件
cp .../concept-registry.yaml .../concept-registry.yaml.backup

# 重建
python scripts/kn_dedup.py --vault <ROOT> sync-registry --apply
```

### Q17: 幽灵链接修复后还是有问题

可能原因：
1. 多候选匹配（如"效率"同时指向"认知效率"和"工作效率"）
2. 目标文件名本身不规范

查看详细报告：
```bash
python scripts/kn_links.py --vault <ROOT> check
```

手动处理 `unresolved` 列表中的链接。

## 最佳实践

### Q18: 每天应该怎么使用这个系统？

**晨间**：
1. 在 `编码笔记/` 写新想法/读书笔记
2. 运行 `@编码` 生成编码笔记

**傍晚**：
1. 运行 `@解码` 分析今日笔记
2. 审阅提取的原子/原创笔记
3. 运行脚本维护

**周末**：
1. 运行 `@知识图谱` 建立链接
2. 检查去重、修复链接
3. 归档过时内容

### Q19: 如何避免概念重复？

**提取前**：
```bash
python scripts/kn_dedup.py --vault <ROOT> check --concept <概念名>
```

**提取后**：
- AI 会自动查注册表
- 发现重复会暂停询问
- 选择：合并/跨学科实例/改名/跳过

### Q20: 原创概念和已证实概念之间能建立链接吗？

**能！** 这是知识创新的重要环节。

例如：
```markdown
# OC-CE-框架觉知.md（你的原创概念）

基于 [[TC-CE-符号暴力]]（布迪厄）和 [[TN-CE-认知失调]]（费斯廷格）
提出的新概念...
```

跨库链接不仅可以，而且应该鼓励——这展示了你如何站在前人肩膀上创新。

---

**还有问题？**

- 查看 [完整文档](./文希·Obsidian知识库文件架构v2.5.md)
- 提交 GitHub Issue
- 加入文希AI社区讨论
