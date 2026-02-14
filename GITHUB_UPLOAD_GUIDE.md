# GitHub 上传文件选择指南

> 本文档说明在上传项目到 GitHub 时应该包含和排除的文件和目录。

---

## 📋 应该包含的文件

### 1. 源代码文件

#### 前端（React + Vite）

```
✅ src/                    # React 源代码
✅ src/main.jsx            # 应用入口文件
✅ src/App.jsx             # 主应用组件
✅ src/index.css           # 全局样式
✅ index.html              # HTML 模板
```

#### 后端（Python Flask）

```
✅ backend/                # Python 后端目录
✅ backend/app.py          # Flask 应用主文件
✅ backend/cloudflare_db.py # Cloudflare D1 数据库管理器
✅ backend/crawler.py       # 新闻爬虫
✅ backend/deepseek_client.py  # DeepSeek API 客户端
✅ backend/gemini_client.py   # Gemini API 客户端
✅ backend/r2_storage.py     # R2 存储管理器
✅ backend/supabase_client.py # Supabase 客户端（备选）
✅ backend/test_deepseek.py # 测试文件
```

#### Vercel Serverless Functions

```
✅ api/                   # Vercel Functions 目录
✅ api/index.py          # Vercel 函数入口
✅ api/requirements.txt   # Python 依赖
```

### 2. 配置文件

```
✅ package.json           # Node.js 依赖和脚本
✅ vite.config.js        # Vite 配置
✅ tailwind.config.js    # Tailwind CSS 配置
✅ postcss.config.js     # PostCSS 配置
✅ wrangler.toml         # Cloudflare Workers 配置
✅ vercel.json          # Vercel 配置（如果存在）
```

### 3. 数据库文件

```
✅ database/              # 数据库目录
✅ database/schema.sql    # 数据库表结构
```

### 4. 文档文件

```
✅ README.md             # 项目说明文档（如果存在）
✅ DEPLOYMENT.md        # 部署指南
✅ MANUAL_DEPLOYMENT_GUIDE.md  # 手动部署说明
✅ CLOUDFLARE_D1_TUTORIAL.md   # Cloudflare D1 教程
✅ LICENSE              # 许可证文件（如果存在）
```

### 5. 环境变量模板

```
✅ .env.example          # 环境变量模板（不包含敏感信息）
```

### 6. 脚本文件

```
✅ scripts/              # 工具脚本目录
✅ scripts/init_db.py   # 数据库初始化脚本
```

### 7. Git 配置

```
✅ .gitignore           # Git 忽略规则
```

---

## ❌ 应该排除的文件

### 1. 依赖目录

```
❌ node_modules/         # Node.js 依赖
❌ .venv/              # Python 虚拟环境
❌ venv/               # Python 虚拟环境
❌ ENV/                 # Python 虚拟环境
❌ env/                 # Python 虚拟环境
```

### 2. 构建输出

```
❌ dist/                # Vite 构建输出
❌ build/               # 构建输出
❌ .next/               # Next.js 构建输出
❌ out/                 # 构建输出
```

### 3. 环境变量（包含敏感信息）

```
❌ .env                 # 本地环境变量（包含 API 密钥）
❌ .env.local           # 本地环境变量
❌ .env.development.local
❌ .env.test.local
❌ .env.production.local
```

### 4. IDE 配置

```
❌ .vscode/             # VS Code 配置
❌ .idea/               # IntelliJ IDEA 配置
❌ *.suo               # Visual Studio 用户选项
❌ *.ntvs*              # Visual Studio 配置
❌ *.njsproj            # Visual Studio 项目
❌ *.sln                # Visual Studio 解决方案
```

### 5. Python 缓存和编译文件

```
❌ __pycache__/        # Python 字节码缓存
❌ *.py[cod]           # Python 编译文件
❌ *$py.class           # Python 类文件
❌ *.so                 # Python 共享对象
❌ *.pyc                # Python 字节码
❌ *.pyo                # Python 优化字节码
```

### 6. 操作系统文件

```
❌ .DS_Store            # macOS 文件
❌ .DS_Store?           # macOS 文件
❌ ._*                 # macOS 资源分支文件
❌ Thumbs.db            # Windows 缩略图缓存
❌ desktop.ini          # Windows 配置
```

### 7. 日志和临时文件

```
❌ *.log                # 日志文件
❌ logs/                # 日志目录
❌ *.tmp                # 临时文件
❌ tmp/                 # 临时目录
❌ .cache/              # 缓存目录
❌ temp/                # 临时目录
```

### 8. 测试和覆盖率

```
❌ coverage/            # 测试覆盖率报告
❌ .nyc_output/         # NYC 覆盖率输出
❌ *.cover              # 覆盖率文件
```

### 9. 数据库文件

```
❌ *.db                 # SQLite 数据库
❌ *.sqlite              # SQLite 数据库
❌ *.sqlite3            # SQLite 数据库
```

### 10. 备份文件

```
❌ *.bak                # 备份文件
❌ *.backup             # 备份文件
```

### 11. 其他临时和系统文件

```
❌ *.swp                # Vim 交换文件
❌ *.swo                # Vim 交换文件
❌ *~                   # 备份文件
❌ .Spotlight-V100     # macOS 索引
❌ .Trashes/            # macOS 回收站
```

---

## 📝 .gitignore 配置说明

项目已配置了完整的 `.gitignore` 文件，自动排除以下内容：

### 已排除的文件和目录

```gitignore
# 日志
logs
*.log

# 依赖
node_modules
.pnp
.pnp.js

# 构建输出
dist
dist-ssr
build
.next
out

# 环境变量
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.env.*.local

# 虚拟环境
.venv/
venv/
ENV/
env/
.trae/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/*
!.vscode/extensions.json
.idea
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
*.swp
*.swo
*~

# 操作系统
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# 测试
coverage
.nyc_output
.coverage
.pytest_cache/
.cache

# 其他
.cache/
.temp/
tmp/
*.tmp

# 数据库
*.db
*.sqlite
*.sqlite3

# 备份文件
*.bak
*.backup
```

### 重要的例外

```gitignore
# VS Code 配置（保留扩展配置）
!.vscode/extensions.json
```

---

## 🚀 上传步骤

### 步骤 1：初始化 Git 仓库

```bash
# 进入项目目录
cd c:\Users\Lenovo\Desktop\cc-test

# 初始化 Git 仓库（如果尚未初始化）
git init

# 添加所有文件
git add .

# 检查哪些文件会被添加
git status

# 提交初始版本
git commit -m "Initial commit"
```

### 步骤 2：创建 GitHub 仓库

1. 访问 [GitHub](https://github.com/)
2. 点击右上角的 **"+"** 按钮
3. 选择 **"New repository"**
4. 填写仓库信息：
   - **Repository name**: `cc-test` 或你喜欢的名称
   - **Description**: 印尼新闻 PWA 应用
   - **Public/Private**: 根据需要选择
5. 点击 **"Create repository"**

### 步骤 3：连接本地仓库到 GitHub

```bash
# 添加远程仓库
git remote add origin https://github.com/<your-username>/cc-test.git

# 推送到 GitHub
git push -u origin main

# 或者如果使用不同的分支名
git branch -M main
git push -u origin main
```

### 步骤 4：验证上传的文件

```bash
# 查看仓库中的文件
git ls-files

# 应该看到以下文件结构：
# api/
# backend/
# database/
# scripts/
# src/
# .env.example
# .gitignore
# package.json
# vite.config.js
# wrangler.toml
# 等等...

# 不应该看到：
# node_modules/
# .venv/
# .env
# dist/
# 等等...
```

---

## ✅ 上传前检查清单

在推送到 GitHub 之前，确保：

- [ ] `.gitignore` 文件已正确配置
- [ ] `.env` 文件没有被添加（包含敏感信息）
- [ ] `node_modules/` 目录没有被添加
- [ ] `.venv/` 目录没有被添加
- [ ] `dist/` 目录没有被添加
- [ ] 所有必要的源代码文件都已添加
- [ ] 配置文件（package.json, wrangler.toml）已添加
- [ ] 文档文件已添加
- [ ] `.env.example` 已添加（不包含敏感信息）

---

## 🔍 验证上传结果

### 在 GitHub 仓库中检查

1. 访问你的 GitHub 仓库
2. 检查 **Files** 标签
3. 确认以下内容：

#### 应该看到的文件和目录

```
✅ api/
✅ api/index.py
✅ api/requirements.txt
✅ backend/
✅ backend/app.py
✅ backend/cloudflare_db.py
✅ backend/crawler.py
✅ backend/deepseek_client.py
✅ backend/gemini_client.py
✅ backend/r2_storage.py
✅ backend/supabase_client.py
✅ backend/test_deepseek.py
✅ database/
✅ database/schema.sql
✅ scripts/
✅ scripts/init_db.py
✅ src/
✅ src/App.jsx
✅ src/index.css
✅ src/main.jsx
✅ .env.example
✅ .gitignore
✅ package.json
✅ vite.config.js
✅ tailwind.config.js
✅ postcss.config.js
✅ wrangler.toml
✅ DEPLOYMENT.md
✅ MANUAL_DEPLOYMENT_GUIDE.md
✅ CLOUDFLARE_D1_TUTORIAL.md
```

#### 不应该看到的文件和目录

```
❌ node_modules/
❌ .venv/
❌ venv/
❌ ENV/
❌ env/
❌ .trae/
❌ .env
❌ .env.local
❌ dist/
❌ build/
❌ __pycache__/
❌ *.pyc
❌ *.pyo
❌ .vscode/
❌ .idea/
❌ .DS_Store
❌ Thumbs.db
❌ logs/
❌ *.log
```

---

## 📊 文件大小参考

| 文件/目录 | 预期大小 | 说明 |
|-----------|-----------|------|
| `src/` | ~100 KB | React 源代码 |
| `backend/` | ~50 KB | Python 后端 |
| `api/` | ~10 KB | Vercel Functions |
| `database/` | ~5 KB | SQL 文件 |
| `node_modules/` | ~200 MB+ | Node.js 依赖（已排除）|
| `.venv/` | ~100 MB+ | Python 虚拟环境（已排除）|

**总大小**（不包括依赖）：< 200 KB

---

## 🛡️ 安全建议

1. **永远不要上传敏感信息**
   - ❌ 不要上传 `.env` 文件
   - ❌ 不要上传包含 API 密钥的任何文件
   - ✅ 只上传 `.env.example` 模板

2. **使用 `.gitignore` 保护敏感信息**
   - ✅ 确保 `.gitignore` 正确配置
   - ✅ 定期检查 `git status` 确认没有意外添加敏感文件

3. **定期审查仓库内容**
   - ✅ 检查是否有意外提交的敏感信息
   - ✅ 使用 GitHub 的 **"Secret scanning"** 功能

4. **使用 GitHub Secrets 管理敏感信息**
   - ✅ 在 GitHub 仓库设置中添加 Secrets
   - ✅ 在 CI/CD 中使用 Secrets 而不是硬编码

---

## 📞 常见问题

### Q: 如何检查哪些文件会被上传？

A: 使用以下命令：

```bash
# 查看将被跟踪的文件
git ls-files

# 查看未被跟踪的文件
git ls-files --others --exclude-standard

# 查看所有文件（包括被忽略的）
git ls-files --cached --others
```

### Q: 如何强制添加被忽略的文件？

A: 不推荐！但如果确实需要：

```bash
# 强制添加特定文件
git add -f .env

# 或者临时移除忽略规则
git add -f node_modules/specific-package/
```

### Q: 如何移除已提交的敏感信息？

A: 如果意外提交了敏感信息：

```bash
# 1. 从历史中移除文件
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env'

# 2. 重写历史
git reset --hard

# 3. 强制推送
git push -f origin main
```

**注意**：这会重写 Git 历史，只在紧急情况下使用！

### Q: 如何修复 .gitignore 后重新添加文件？

A:

```bash
# 1. 清除 Git 缓存
git rm -r --cached .

# 2. 重新添加文件
git add .

# 3. 提交
git commit -m "Update .gitignore and re-add files"
```

---

## 📚 相关资源

- [Git 忽略文档](https://git-scm.com/docs/gitignore)
- [GitHub .gitignore 模板](https://github.com/github/gitignore)
- [GitHub 安全最佳实践](https://docs.github.com/en/code-security/getting-started/best-practices-for-secret-management)

---

**文档版本**: 1.0.0  
**最后更新**: 2025-02-10  
**维护者**: Deployment Team
