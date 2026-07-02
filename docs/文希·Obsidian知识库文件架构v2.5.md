# 文希 · Obsidian 知识库文件架构 v2.5

> 已证实（原子笔记）与原创（原创库）分离，各按 术语/思维模型/概念 × 7学科 细分
> 众推客科技 · 文希AI社区 · #AI搭子圈 ｜ 2026.07

如果你想先看流程图、思维导图和命名拆解，可以从 [知识库视觉导览](知识库视觉导览.md) 开始。

---

## 一、顶层全景

```
文希知识库/                          ← Obsidian 打开这一层作为库
├── 编码笔记/                        ← 输入：手写/摘录，按7学科
├── 解码笔记/                        ← 加工：AI 7维度解码，镜像7学科
├── Obsidian Vault/                  ← 核心库（PARA + 原子 + 原创 + 系统）
├── Output/                          ← 可发布内容
├── Business/                        ← 商业项目
├── .claude/skills/                  ← 工作流脚本
└── .knowledge-network-config.yaml   ← 路径配置
```

---

## 二、编码笔记（7 学科）

```
编码笔记/
├── 01-LE-人生体验-LifeExperience/
├── 02-DK-学科知识-DisciplineKnowledge/
├── 03-AP-艺术感知-ArtisticPerception/
├── 04-CE-认知进化-CognitiveEvolution/
├── 05-PA-实践活动-PracticalActivity/
├── 06-LT-文学创作-Literature/
└── 07-XX-交叉学科-Interdisciplinary/
```
> 命名：`CODE-YYYYMMDD-SEQ@版本-标题.md`（如 `DK-20250510-001@v1-读书笔记.md`）
> 某学科 ≥20 条时可加学科细分子目录。

---

## 三、解码笔记（镜像 7 学科）

```
解码笔记/
├── 01-LE-人生体验-LifeExperience/
├── 02-DK-学科知识-DisciplineKnowledge/
├── 03-AP-艺术感知-ArtisticPerception/
├── 04-CE-认知进化-CognitiveEvolution/
├── 05-PA-实践活动-PracticalActivity/
├── 06-LT-文学创作-Literature/
└── 07-XX-交叉学科-Interdisciplinary/
```
> 命名：`CODE-YYYYMMDD-SEQ@解码-标题-解码.md`

---

## 四、Obsidian Vault 核心库

```
Obsidian Vault/
├── 00-Inbox/                        收件箱（碎片临时存放）
├── 01-Projects/                     PARA：项目
├── 02-Areas/                        PARA：领域
│
├── 03-Atomic/                       ⭐ 原子笔记 = 已被证实的
│   ├── TC-术语/                     已证实术语
│   │   ├── TC-CE-认知进化/
│   │   ├── TC-DK-学科知识/
│   │   ├── TC-LE-人生体验/
│   │   ├── TC-LT-文学创作/
│   │   ├── TC-AP-艺术感知/
│   │   ├── TC-PA-实践活动/
│   │   └── TC-XX-交叉学科/
│   ├── TM-思维模型/                 已证实思维模型
│   │   └── （TM-CE / TM-DK / TM-LE / TM-LT / TM-AP / TM-PA / TM-XX）
│   ├── TN-概念/                     已证实概念
│   │   └── （TN-CE / TN-DK / TN-LE / TN-LT / TN-AP / TN-PA / TN-XX）
│   └── 视图/
│
├── 04-原创/                         ⭐ 原创库 = 你新创的
│   ├── OT-原创术语/                 原创术语
│   │   └── （OT-CE / OT-DK / OT-LE / OT-LT / OT-AP / OT-PA / OT-XX）
│   ├── OM-原创思维模型/             原创方法论/框架
│   │   └── （OM-CE / OM-DK / OM-LE / OM-LT / OM-AP / OM-PA / OM-XX）
│   └── OC-原创概念/                 原创概念
│       └── （OC-CE / OC-DK / OC-LE / OC-LT / OC-AP / OC-PA / OC-XX）
│
├── 05-Resources/                    PARA：外部资料
├── 06-参考资料/                     备用资源区
├── 07-System/                       系统配置（concept-registry.yaml）
├── 08-Daily/                        每日/周/月记录
├── 09-MOC/                          MOC 索引地图
├── 10-MAP/                          知识图谱（Canvas）
├── 11-Data/                         数据存储
├── AI融合笔记/                      原始 AI 输出（不编码）
└── Templates/                       笔记模板
```

---

## 五、原子笔记 vs 原创库（核心区别）

| | 原子笔记 03-Atomic | 原创库 04-原创 |
|---|---|---|
| 放什么 | **已被证实/研究出的**知识 | **你新创的**知识 |
| is_original | `false` | `true` |
| 术语 | `TC`（如符号暴力） | `OT` |
| 思维模型 | `TM`（如第一性原理） | `OM`（如AB面分析框架） |
| 概念 | `TN`（如认知失调） | `OC`（如框架觉知） |
| 命名 | `TC-CE-符号暴力.md` | `OC-CE-框架觉知.md` |

> 两库结构对称：形态（术语/思维模型/概念）→ 7 学科，均两层为止，禁止第三层。

---

## 六、Output / Business

```
Output/
├── 公众号文章/
├── 视频脚本/
└── 社群内容/

Business/            商业项目（房产/电商/外贸/大健康等按需建）
```

---

## 七、缩写速查

**7 学科 CODE：** LE人生体验 · DK学科知识 · AP艺术感知 · CE认知进化 · PA实践活动 · LT文学创作 · XX交叉学科

**已证实 PREFIX（T=Trusted）：** TC术语 · TM思维模型 · TN概念
**原创 PREFIX（O=Original）：** OT术语 · OM思维模型 · OC概念

**status：** 种子 → 萌芽 → 成熟 → 归档

---

*— 已证实归已证实，原创归原创，各按形态和学科归位 —*
