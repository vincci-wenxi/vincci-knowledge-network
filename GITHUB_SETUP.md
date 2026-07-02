# GitHub 仓库创建与上传指南

## 第一步：注册 GitHub 账号

1. 访问 [https://github.com/signup](https://github.com/signup)
2. 填写信息：
   - 邮箱地址
   - 密码（至少15个字符或8个字符+数字和小写字母）
   - 用户名（建议：vincci-tech 或 wenxi-ai 等）
3. 完成验证并登录

## 第二步：创建新仓库

### 方式一：网页创建（推荐新手）

1. 登录后，点击右上角 "+" → "New repository"
2. 填写信息：
   - **Repository name**: `vincci-knowledge-network`
   - **Description**: 文希知识网络 v2.5 - Obsidian 知识管理系统
   - **Public** (选择公开)
   - ⚠️ **不要勾选** "Add a README file"（我们已经有了）
   - ⚠️ **不要选择** .gitignore 和 license（我们已经有了）
3. 点击 "Create repository"

### 方式二：命令行创建（需要 GitHub CLI）

```bash
gh repo create vincci-knowledge-network --public --description "文希知识网络 v2.5 - Obsidian 知识管理系统"
```

## 第三步：配置 Git 用户信息

在终端执行：

```bash
# 配置用户名（替换为你的GitHub用户名）
git config --global user.name "你的GitHub用户名"

# 配置邮箱（替换为你在GitHub注册的邮箱）
git config --global user.email "你的邮箱@example.com"

# 验证配置
git config --global --list
```

## 第四步：连接远程仓库并推送

### A. 使用 HTTPS（推荐新手）

在项目目录执行：

```bash
cd "/Users/vpn/Library/Mobile Documents/com~apple~CloudDocs/Claude MD/vincci-knowledge-network"

# 添加远程仓库（替换 YOUR_USERNAME 为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/vincci-knowledge-network.git

# 重命名主分支为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

**首次推送时会要求身份验证**：
- 用户名：你的GitHub用户名
- 密码：**不是账号密码！需要用 Personal Access Token（见下方）**

#### 创建 Personal Access Token（PAT）

1. GitHub 网站登录后，点击右上角头像 → Settings
2. 左侧菜单最下方：Developer settings
3. Personal access tokens → Tokens (classic)
4. Generate new token (classic)
5. 设置：
   - Note: `vincci-knowledge-network-upload`
   - Expiration: 90 days（或自定义）
   - 勾选权限：`repo`（完整仓库权限）
6. 点击 "Generate token"
7. **立即复制 token**（离开页面后无法再看到！）
8. 在终端推送时，密码处粘贴这个 token

### B. 使用 SSH（推荐熟练用户）

```bash
# 1. 生成 SSH 密钥（如果没有）
ssh-keygen -t ed25519 -C "你的邮箱@example.com"

# 2. 复制公钥
cat ~/.ssh/id_ed25519.pub | pbcopy

# 3. 在 GitHub 添加 SSH 密钥
# Settings → SSH and GPG keys → New SSH key → 粘贴公钥

# 4. 添加远程仓库（SSH 地址）
git remote add origin git@github.com:YOUR_USERNAME/vincci-knowledge-network.git

# 5. 推送
git branch -M main
git push -u origin main
```

## 第五步：验证上传成功

1. 访问 `https://github.com/YOUR_USERNAME/vincci-knowledge-network`
2. 应该能看到：
   - README.md 显示为首页
   - 所有脚本文件
   - docs/ 目录
   - LICENSE 文件

## 后续更新代码

每次修改后推送：

```bash
cd "/Users/vpn/Library/Mobile Documents/com~apple~CloudDocs/Claude MD/vincci-knowledge-network"

# 查看修改
git status

# 添加修改
git add .

# 提交
git commit -m "描述你的修改"

# 推送到 GitHub
git push
```

## 常见问题

### Q: 推送时报错 "remote: Repository not found"

**解决**：检查远程地址是否正确

```bash
git remote -v
# 如果地址错误，删除后重新添加
git remote remove origin
git remote add origin https://github.com/正确的用户名/vincci-knowledge-network.git
```

### Q: 推送时报错 "failed to push some refs"

**解决**：远程仓库有文件但本地没有（比如你在GitHub创建时勾选了README）

```bash
# 先拉取远程内容
git pull origin main --allow-unrelated-histories

# 解决冲突后再推送
git push -u origin main
```

### Q: 推送时报错 "Support for password authentication was removed"

**解决**：不能用密码，必须用 Personal Access Token（见上方"创建 PAT"）

### Q: 忘记保存 Personal Access Token

**解决**：重新生成一个新的 token，旧的会失效

## 可选：添加仓库徽章

编辑 README.md，在顶部添加：

```markdown
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/vincci-knowledge-network?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/vincci-knowledge-network?style=social)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/vincci-knowledge-network)
```

## 下一步

✅ 仓库上传完成后，你可以：

1. 在 README.md 中添加你的GitHub用户名链接
2. 创建 GitHub Release 发布 v2.5.0 版本
3. 邀请其他人 Star 你的仓库
4. 设置 GitHub Pages 展示文档
5. 添加贡献指南 CONTRIBUTING.md

---

**需要帮助？**

- [GitHub 官方文档](https://docs.github.com)
- [Git 教程](https://git-scm.com/book/zh/v2)
