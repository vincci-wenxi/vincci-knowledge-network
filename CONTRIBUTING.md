# 贡献指南

感谢你有兴趣为文希知识网络项目做出贡献！

## 如何贡献

### 报告 Bug

如果你发现了 bug，请：

1. 检查 [Issues](https://github.com/YOUR_USERNAME/vincci-knowledge-network/issues) 中是否已有相关报告
2. 如果没有，创建新 Issue，包含：
   - Bug 描述
   - 复现步骤
   - 预期行为 vs 实际行为
   - 环境信息（操作系统、Python版本等）
   - 错误日志或截图

### 提出新功能

1. 创建 Issue，标签选择 `enhancement`
2. 清晰描述：
   - 功能用途
   - 使用场景
   - 可能的实现思路

### 提交代码

#### 1. Fork 项目

点击页面右上角的 "Fork" 按钮

#### 2. 克隆到本地

```bash
git clone https://github.com/你的用户名/vincci-knowledge-network.git
cd vincci-knowledge-network
```

#### 3. 创建分支

```bash
git checkout -b feature/新功能名称
# 或
git checkout -b fix/修复的问题
```

#### 4. 编写代码

- 遵循现有代码风格
- 添加必要的注释
- 更新相关文档

#### 5. 测试

```bash
# 确保所有脚本能正常运行
python scripts/kn_common.py
python scripts/kn_dedup.py --vault /path/to/test/vault scan
python scripts/kn_links.py --vault /path/to/test/vault check
python scripts/kn_status.py --vault /path/to/test/vault check
```

#### 6. 提交

```bash
git add .
git commit -m "feat: 添加XXX功能" 
# 或
git commit -m "fix: 修复XXX问题"
```

提交信息格式：
- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具变动

#### 7. 推送到你的仓库

```bash
git push origin feature/新功能名称
```

#### 8. 创建 Pull Request

1. 访问你的 Fork 仓库页面
2. 点击 "New Pull Request"
3. 填写 PR 描述：
   - 修改了什么
   - 为什么要修改
   - 如何测试

## 代码规范

### Python 代码

- 使用 4 空格缩进
- 函数和类使用文档字符串
- 变量名使用 `snake_case`
- 常量使用 `UPPER_CASE`
- 遵循 PEP 8 风格指南

### Markdown 文档

- 使用中文标点
- 代码块指定语言
- 链接使用相对路径（同仓库内）
- 保持目录结构清晰

### 脚本

- Shell 脚本添加 `#!/usr/bin/env bash` 开头
- PowerShell 脚本使用 `.ps1` 后缀，并提供与 Shell 脚本等价的入口
- 使用 `set -e` 或 `$ErrorActionPreference = "Stop"` 遇错退出
- 重要操作前添加 echo 说明
- 变量使用 `${VAR_NAME}` 格式

## 项目结构

```
vincci-knowledge-network/
├── scripts/           # Python 工具脚本
│   ├── kn_common.py
│   ├── kn_dedup.py
│   ├── kn_links.py
│   └── kn_status.py
├── docs/              # 文档
│   ├── FAQ.md
│   ├── SKILL-v2_5.md
│   └── ...
├── setup-vault.sh     # macOS / Linux / Git Bash 建库脚本
├── setup-vault.ps1    # Windows PowerShell 建库脚本
├── README.md
├── LICENSE
└── requirements.txt
```

## 版本发布流程

（仅维护者）

1. 更新版本号（在相关文件中）
2. 更新 CHANGELOG.md
3. 创建 Git tag
4. 推送 tag
5. 在 GitHub 创建 Release

```bash
git tag -a v2.5.1 -m "Release v2.5.1"
git push origin v2.5.1
```

## 社区准则

- 尊重他人
- 建设性讨论
- 欢迎新人
- 包容不同观点

## 许可证

贡献的代码将遵循项目的 MIT 许可证。

## 联系方式

- Issue 讨论
- 文希AI社区
- #AI搭子圈

---

再次感谢你的贡献！🎉
