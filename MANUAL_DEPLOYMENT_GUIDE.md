# 手动部署1操作说明

> 本文档提供详细的部署操作步骤，适合具有基础技术知识的人员按照步骤独立完成部署。

---

## 目录

1. [部署环境准备要求](#1-部署环境准备要求)
2. [部署前的准备工作](#2-部署前的准备工作)
3. [具体的部署步骤](#3-具体的部署步骤)
4. [部署后的验证方法](#4-部署后的验证方法)
5. [常见问题及解决方案](#5-常见问题及解决方案)
6. [回滚机制](#6-回滚机制)

---

## 1. 部署环境准备要求

### 1.1 操作系统要求

| 组件 | 最低要求 | 推荐配置 |
|--------|-----------|-----------|
| **操作系统** | Windows 10/11, macOS 10.15+, Ubuntu 18.04+ | Windows 11, macOS 12+, Ubuntu 22.04+ |
| **处理器** | 双核 CPU | 四核或更高 |
| **内存** | 4 GB RAM | 8 GB RAM 或更高 |
| **磁盘空间** | 2 GB 可用空间 | 5 GB 或更高 |

### 1.2 必要依赖软件及版本

#### 前端依赖

| 软件 | 最低版本 | 推荐版本 | 安装命令 |
|------|-----------|-----------|---------|
| **Node.js** | v16.0.0 | v18.18.0 或更高 | `nvm install 18` 或从 [nodejs.org](https://nodejs.org/) 下载 |
| **npm** | v8.0.0 | v9.0.0 或更高 | 随 Node.js 安装 |
| **Git** | v2.0.0 | v2.40.0 或更高 | `sudo apt install git` (Linux) 或从 [git-scm.com](https://git-scm.com/) 下载 |

#### 后端依赖

| 软件 | 最低版本 | 推荐版本 | 安装命令 |
|------|-----------|-----------|---------|
| **Python** | v3.8.0 | v3.10.0 或更高 | `python3 --version` 或从 [python.org](https://www.python.org/) 下载 |
| **pip** | v21.0 | v23.0 或更高 | 随 Python 安装 |

#### 部署工具

| 软件 | 最低版本 | 推荐版本 | 用途 | 安装命令 |
|------|-----------|-----------|------|---------|
| **Vercel CLI** | v28.0.0 | v32.0.0 或更高 | 部署到 Vercel | `npm install -g vercel` |
| **Wrangler CLI** | v3.0.0 | v3.22.0 或更高 | 管理 Cloudflare D1 | `npm install -g wrangler` |

### 1.3 网络要求

- 稳定的互联网连接
- 能够访问以下域名：
  - `vercel.com`
  - `cloudflare.com`
  - `api.cloudflare.com`
  - `api.deepseek.com`

---

## 2. 部署前的准备工作

### 2.1 代码拉取

#### 步骤 2.1.1：克隆或下载代码

**方式一：使用 Git 克隆（推荐）**

```bash
# 克隆仓库
git clone <your-repository-url>
cd cc-test

# 查看当前分支
git branch

# 切换到正确的分支（如果需要）
git checkout main
```

**方式二：下载 ZIP 压缩包**

1. 访问代码仓库
2. 点击 "Code" → "Download ZIP"
3. 解压到本地目录
4. 进入项目目录：`cd cc-test`

#### 步骤 2.1.2：验证文件结构

```bash
# 查看项目结构
ls -la

# 应该看到以下主要文件/目录：
# - api/              # Vercel Serverless Functions
# - backend/           # Python Flask 后端
# - database/          # 数据库 SQL 文件
# - scripts/           # 工具脚本
# - src/               # React 前端源码
# - package.json        # Node.js 依赖
# - wrangler.toml       # Cloudflare Workers 配置
# - vercel.json        # Vercel 配置
# - .env.example       # 环境变量模板
```

### 2.2 配置文件修改

#### 步骤 2.2.1：创建本地环境变量文件

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# Windows: notepad .env
# macOS/Linux: nano .env 或 vim .env
```

#### 步骤 2.2.2：验证环境变量配置

打开 `.env` 文件，确认以下变量已正确配置：

```env
# DeepSeek API 配置
DEEPSEEK_API_KEY=sk-58d565ce05854668b97c5209aeb5c595

# Cloudflare D1 数据库配置
CLOUDFLARE_D1_DATABASE_ID=6fec1b24-3c6c-4f94-aaa5-aa15b0ecaeb3
CLOUDFLARE_API_TOKEN=5bpeAAggUdULNIvmOAIvIRzRuR9nHN8TKHjO4nda
CLOUDFLARE_ACCOUNT_ID=ebc304d642ceaec2c9b3ca7f24539736

# Cloudflare R2 配置（可选）
# R2_ENDPOINT=your_r2_endpoint
# R2_ACCESS_KEY=your_r2_access_key
# R2_SECRET_KEY=your_r2_secret_key
# R2_BUCKET_NAME=your_r2_bucket_name
# R2_PUBLIC_URL=your_r2_public_url
```

**验证清单**：
- [ ] DEEPSEEK_API_KEY 已设置
- [ ] CLOUDFLARE_D1_DATABASE_ID 已设置
- [ ] CLOUDFLARE_API_TOKEN 已设置
- [ ] CLOUDFLARE_ACCOUNT_ID 已设置

### 2.3 安装项目依赖

#### 步骤 2.3.1：安装前端依赖

```bash
# 进入项目根目录
cd c:\Users\Lenovo\Desktop\cc-test

# 安装 Node.js 依赖
npm install

# 验证安装
npm list --depth=0
```

**预期输出**：应该看到 react, vite, tailwindcss 等依赖包

#### 步骤 2.3.2：安装后端依赖

```bash
# 进入后端目录
cd backend

# 创建 Python 虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装 Python 依赖
pip install -r requirements.txt

# 验证安装
pip list
```

**预期输出**：应该看到 flask, requests, beautifulsoup4 等依赖包

### 2.4 初始化数据库

#### 步骤 2.4.1：安装 Wrangler CLI

```bash
# 全局安装 Wrangler
npm install -g wrangler

# 验证安装
wrangler --version
```

**预期输出**：`3.x.x` 或更高版本

#### 步骤 2.4.2：登录 Cloudflare

```bash
# 登录 Cloudflare
wrangler login

# 浏览器会自动打开，点击授权
# 授权成功后会显示：
# ⛅️ wrangler 3.x.x
# -------------------
# ⚡️ Successfully logged in with your Cloudflare account!
```

#### 步骤 2.4.3：执行数据库初始化

```bash
# 方式一：使用 SQL 文件初始化（推荐）
wrangler d1 execute cc-test-database --file=database/schema.sql

# 预期输出：
# 🌀 Executing on database cc-test-database...
# ✅ Executed 9 commands in 123ms

# 方式二：使用 Dashboard 初始化
# 1. 访问 https://dash.cloudflare.com/
# 2. 进入 Workers & Pages → D1 → cc-test-database
# 3. 点击 Console 标签
# 4. 复制 database/schema.sql 内容
# 5. 粘贴到 SQL 编辑器
# 6. 点击 Execute
```

#### 步骤 2.4.4：验证数据库表创建

```bash
# 查看所有表
wrangler d1 execute cc-test-database --command="SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"

# 预期输出：
# [
#   {
#     "success": true,
#     "result": [
#       {
#         "results": [
#           {"name": "daily_digest"},
#           {"name": "news_feed"},
#           {"name": "vocabulary"}
#         ]
#       }
#     ]
#   }
# ]
```

**验证清单**：
- [ ] news_feed 表已创建
- [ ] vocabulary 表已创建
- [ ] daily_digest 表已创建

### 2.5 本地测试（可选但推荐）

#### 步骤 2.5.1：启动前端开发服务器

```bash
# 打开新的终端窗口
# 进入项目根目录
cd c:\Users\Lenovo\Desktop\cc-test

# 启动前端开发服务器
npm run dev

# 预期输出：
#   VITE v5.x.x  ready in xxx ms
#
#   ➜  Local:   http://localhost:5173/
#   ➜  Network: use --host to expose
```

#### 步骤 2.5.2：启动后端开发服务器

```bash
# 打开另一个新的终端窗口
# 进入后端目录
cd c:\Users\Lenovo\Desktop\cc-test\backend

# 激活虚拟环境（如果尚未激活）
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 启动 Flask 服务器
python app.py

# 预期输出：
#  * Running on http://0.0.0.0:8080
#  * Running on http://127.0.0.1:8080
#  * Running on http://localhost:8080
```

#### 步骤 2.5.3：测试本地应用

1. 打开浏览器访问 `http://localhost:5173`
2. 检查页面是否正常加载
3. 测试 API 端点：
   - `http://localhost:8080/api/news`
   - `http://localhost:8080/api/health`

---

## 3. 具体的部署步骤

### 3.1 部署到 Vercel

#### 步骤 3.1.1：安装 Vercel CLI

```bash
# 全局安装 Vercel CLI
npm install -g vercel

# 验证安装
vercel --version
```

**预期输出**：`32.x.x` 或更高版本

#### 步骤 3.1.2：登录 Vercel

```bash
# 登录 Vercel
vercel login

# 按照提示操作：
# 1. 选择登录方式（推荐使用 GitHub 账号）
# 2. 在浏览器中授权 Vercel 访问
# 3. 授权成功后会显示：
# ✅ Logged in as <your-email>
```

#### 步骤 3.1.3：初始化 Vercel 项目

```bash
# 在项目根目录执行
cd c:\Users\Lenovo\Desktop\cc-test

# 初始化项目
vercel

# 按照提示操作：
#
# ? Set up and deploy "~/cc-test"? [Y/n] Y
# ? Which scope do you want to deploy to? 
#   Your username (recommended)
# ? Link to existing project? [y/N] N
# ? What's your project's name? cc-test
# ? In which directory is your code located? ./
# ? Want to override the settings? [y/N] N
#
# 🔗  Linked to <your-username>/cc-test
# 🐘  Preview: https://cc-test-<random>.vercel.app
# ✅ Production: https://cc-test.vercel.app
```

**重要提示**：
- 记录下预览 URL 和生产 URL
- 如果项目已存在，选择链接到现有项目

#### 步骤 3.1.4：配置 Vercel 环境变量

**方式一：通过 Vercel Dashboard（推荐）**

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择项目 `cc-test`
3. 进入 **Settings** → **Environment Variables**
4. 点击 **"Add New"** 添加以下变量：

| 变量名 | 值 | 环境 |
|--------|-----|------|
| `DEEPSEEK_API_KEY` | `sk-58d565ce05854668b97c5209aeb5c595` | Production, Preview, Development |
| `CLOUDFLARE_D1_DATABASE_ID` | `6fec1b24-3c6c-4f94-aaa5-aa15b0ecaeb3` | Production, Preview, Development |
| `CLOUDFLARE_API_TOKEN` | `5bpeAAggUdULNIvmOAIvIRzRuR9nHN8TKHjO4nda` | Production, Preview, Development |
| `CLOUDFLARE_ACCOUNT_ID` | `ebc304d642ceaec2c9b3ca7f24539736` | Production, Preview, Development |

5. 点击 **"Save"** 保存每个变量

**方式二：通过 CLI 命令**

```bash
# 添加环境变量
vercel env add DEEPSEEK_API_KEY sk-58d565ce05854668b97c5209aeb5c595
vercel env add CLOUDFLARE_D1_DATABASE_ID 6fec1b24-3c6c-4f94-aaa5-aa15b0ecaeb3
vercel env add CLOUDFLARE_API_TOKEN 5bpeAAggUdULNIvmOAIvIRzRuR9nHN8TKHjO4nda
vercel env add CLOUDFLARE_ACCOUNT_ID ebc304d642ceaec2c9b3ca7f24539736

# 按照提示选择环境（Production, Preview, Development）
```

#### 步骤 3.1.5：配置服务器区域

1. 在 Vercel Dashboard 中进入项目设置
2. 进入 **Settings** → **General**
3. 找到 **"Regions"** 部分
4. 点击 **"Edit"**
5. 选择以下区域之一：
   - **Singapore (sin1)** - 新加坡（推荐）
   - **Hong Kong (hkg1)** - 香港（备选）
6. 点击 **"Save"**

#### 步骤 3.1.6：部署到生产环境

```bash
# 部署到生产环境
vercel --prod

# 预期输出：
# ⚙️  Production: https://cc-test.vercel.app [3s]
# 🔨  Build completed in 2.3s
# ✅ Deployed to production in 5s
```

### 3.2 部署到 Cloudflare Workers（可选）

如果你想使用 Cloudflare Workers 作为后端，可以按照以下步骤部署：

#### 步骤 3.2.1：部署 Worker

```bash
# 使用 Wrangler 部署
wrangler deploy

# 预期输出：
# ⛅️ wrangler 3.x.x
# -------------------
# Total Upload: 0.23 kB / gzip: 0.12 kB
# Uploaded cc-test-worker (1.23 sec)
# Published cc-test-worker (0.45 sec)
#   https://cc-test-worker.<your-subdomain>.workers.dev
```

#### 步骤 3.2.2：验证 Worker 部署

```bash
# 查看 Worker 日志
wrangler tail

# 访问 Worker URL
curl https://cc-test-worker.<your-subdomain>.workers.dev/api/health
```

---

## 4. 部署后的验证方法

### 4.1 基础功能验证

#### 步骤 4.1.1：访问部署的应用

1. 打开浏览器访问生产 URL：`https://cc-test.vercel.app`
2. 检查页面是否正常加载
3. 打开浏览器开发者工具（F12）
4. 查看 Console 标签，确认没有 JavaScript 错误

#### 步骤 4.1.2：测试 API 端点

**测试健康检查**

```bash
# 使用 curl 测试
curl https://cc-test.vercel.app/api/health

# 预期响应：
# {"success":true,"message":"服务正常运行","timestamp":"now()"}
```

**测试新闻列表 API**

```bash
# 获取今天的新闻
curl https://cc-test.vercel.app/api/news

# 预期响应：
# {"success":true,"data":[...],"message":"获取 2025-02-10 的新闻列表成功"}
```

**测试单词分析 API**

```bash
# 分析单词
curl -X POST https://cc-test.vercel.app/api/analyze/word \
  -H "Content-Type: application/json" \
  -d '{"word":"kabar","context":"Ini adalah kabar terbaru."}'

# 预期响应：
# {"success":true,"data":{"word":"kabar","meaning_cn":"消息",...},"message":"分析单词 kabar 成功"}
```

### 4.2 数据库验证

#### 步骤 4.2.1：检查数据库连接

```bash
# 使用 Wrangler 查询数据库
wrangler d1 execute cc-test-database --command="SELECT COUNT(*) as count FROM news_feed;"

# 预期输出：
# [
#   {
#     "success": true,
#     "result": [
#       {
#         "results": [
#           {"count": 0}
#         ]
#       }
#     ]
#   }
# ]
```

#### 步骤 4.2.2：验证表结构

```bash
# 查看 news_feed 表结构
wrangler d1 execute cc-test-database --command="PRAGMA table_info(news_feed);"

# 预期输出应该包含以下列：
# - id
# - original_url
# - title_cn
# - title_id
# - thumbnail_r2_url
# - published_at
# - content_structure
# - is_crawled
# - created_at
# - updated_at
```

### 4.3 性能验证

#### 步骤 4.3.1：测试响应时间

```bash
# 使用 time 命令测量响应时间
time curl https://cc-test.vercel.app/api/health

# 预期输出：
# real    0m0.234s
# user    0m0.012s
# sys     0m0.008s
```

**性能指标**：
- 健康检查：< 500ms
- 新闻列表：< 2s
- 文章详情：< 3s

#### 步骤 4.3.2：检查 Vercel 部署日志

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择项目 `cc-test`
3. 进入 **Deployments** 标签
4. 点击最新的部署
5. 查看 **Build Logs** 和 **Function Logs**
6. 确认没有错误或警告

### 4.4 验证清单

完成以下检查项：

- [ ] 应用首页可以正常访问
- [ ] 前端页面样式正常加载
- [ ] API 健康检查返回成功
- [ ] 新闻列表 API 返回数据
- [ ] 单词分析 API 正常工作
- [ ] 数据库表结构正确
- [ ] Vercel 部署日志无错误
- [ ] 响应时间在可接受范围内
- [ ] 浏览器控制台无 JavaScript 错误

---

## 5. 常见问题及解决方案

### 5.1 部署相关

#### 问题 5.1.1：Vercel 部署失败

**症状**：
```
Error: Build failed with exit code 1
```

**可能原因**：
1. 依赖安装失败
2. 构建配置错误
3. 环境变量缺失

**解决方案**：

```bash
# 1. 清除缓存并重新安装
rm -rf node_modules
npm cache clean --force
npm install

# 2. 检查 package.json 配置
cat package.json

# 3. 本地构建测试
npm run build

# 4. 查看详细错误日志
vercel --prod --debug
```

#### 问题 5.1.2：环境变量未生效

**症状**：
```
Error: Missing required environment variable
```

**解决方案**：

1. 检查 Vercel Dashboard 中的环境变量
2. 确认变量名拼写正确（区分大小写）
3. 重新部署项目：
   ```bash
   vercel --prod
   ```
4. 检查环境变量作用域（Production, Preview, Development）

#### 问题 5.1.3：部署超时

**症状**：
```
Error: Deployment timed out
```

**解决方案**：

1. 检查网络连接
2. 减少 node_modules 大小：
   ```bash
   npm install --production
   ```
3. 增加 Vercel 部署超时时间（在 vercel.json 中配置）

### 5.2 数据库相关

#### 问题 5.2.1：数据库连接失败

**症状**：
```
Error: Cloudflare database client initialization failed
```

**可能原因**：
1. API Token 无效或过期
2. Account ID 错误
3. 数据库 ID 错误
4. 网络连接问题

**解决方案**：

```bash
# 1. 验证 Cloudflare 凭证
wrangler d1 list

# 2. 测试 API Token
curl -H "Authorization: Bearer 5bpeAAggUdULNIvmOAIvIRzRuR9nHN8TKHjO4nda" \
  https://api.cloudflare.com/client/v4/user/tokens/verify

# 3. 检查数据库是否存在
wrangler d1 info cc-test-database

# 4. 重新生成 API Token（如果需要）
# 访问：https://dash.cloudflare.com/profile/api-tokens
```

#### 问题 5.2.2：表不存在

**症状**：
```
Error: no such table: news_feed
```

**解决方案**：

```bash
# 1. 检查表是否存在
wrangler d1 execute cc-test-database --command="SELECT name FROM sqlite_master WHERE type='table';"

# 2. 重新创建表
wrangler d1 execute cc-test-database --file=database/schema.sql

# 3. 验证表创建
wrangler d1 execute cc-test-database --command="PRAGMA table_info(news_feed);"
```

#### 问题 5.2.3：SQL 执行失败

**症状**：
```
Error: SQL execution failed: syntax error
```

**解决方案**：

1. 检查 SQL 语法
2. 使用 SQLite 在线验证工具：[https://www.sqlitetutorial.net/sqlite-online-compiler/](https://www.sqlitetutorial.net/sqlite-online-compiler/)
3. 逐条执行 SQL 语句以定位问题

### 5.3 API 相关

#### 问题 5.3.1：DeepSeek API 调用失败

**症状**：
```
Error: DeepSeek API request failed
```

**可能原因**：
1. API Key 无效
2. API 配额用尽
3. 网络连接问题

**解决方案**：

```bash
# 1. 验证 API Key
curl -H "Authorization: Bearer sk-58d565ce05854668b97c5209aeb5c595" \
  https://api.deepseek.com/v1/models

# 2. 检查 API 配额
# 访问：https://platform.deepseek.com/dashboard

# 3. 测试 API 连接
curl -X POST https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer sk-58d565ce05854668b97c5209aeb5c595" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"test"}]}'
```

#### 问题 5.3.2：跨域错误（CORS）

**症状**：
```
Error: CORS policy: No 'Access-Control-Allow-Origin' header
```

**解决方案**：

1. 检查后端 CORS 配置：
   ```python
   # backend/app.py
   from flask_cors import CORS
   app = Flask(__name__)
   CORS(app)
   ```
2. 确认 Vercel API 路由配置正确
3. 测试使用 CORS 代理或浏览器扩展

### 5.4 性能相关

#### 问题 5.4.1：响应速度慢

**症状**：
- API 响应时间 > 5s
- 页面加载缓慢

**解决方案**：

1. 检查数据库查询性能
2. 添加适当的索引
3. 使用 Vercel Edge Functions 缓存
4. 启用 CDN 缓存

#### 问题 5.4.2：内存不足

**症状**：
```
Error: JavaScript heap out of memory
```

**解决方案**：

1. 增加 Node.js 内存限制：
   ```json
   // vercel.json
   {
     "buildCommand": "NODE_OPTIONS=--max-old-space-size=4096 npm run build"
   }
   ```
2. 优化代码减少内存使用
3. 分批处理大数据集

---

## 6. 回滚机制

### 6.1 Vercel 回滚

#### 步骤 6.1.1：查看部署历史

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择项目 `cc-test`
3. 进入 **Deployments** 标签
4. 查看所有部署历史

#### 步骤 6.1.2：回滚到之前的版本

**方式一：通过 Dashboard（推荐）**

1. 在部署列表中找到要回滚的版本
2. 点击版本右侧的 **"..."** 菜单
3. 选择 **"Promote to Production"**
4. 确认回滚操作

**方式二：通过 CLI 命令**

```bash
# 查看部署历史
vercel ls

# 回滚到特定部署
vercel rollback <deployment-url>

# 示例：
# vercel rollback https://cc-test.vercel.app/_next/data/deployments/1234567890abcdef
```

#### 步骤 6.1.3：验证回滚

```bash
# 访问应用
curl https://cc-test.vercel.app/api/health

# 确认应用已回滚到之前的版本
```

### 6.2 数据库回滚

#### 步骤 6.2.1：导出当前数据

```bash
# 导出数据库
wrangler d1 export cc-test-database --output=backup-$(date +%Y%m%d-%H%M%S).sql
```

#### 步骤 6.2.2：恢复到之前的状态

```bash
# 方式一：从备份恢复
wrangler d1 execute cc-test-database --file=backup-20250210-120000.sql

# 方式二：手动恢复特定表
# 1. 删除当前表
wrangler d1 execute cc-test-database --command="DROP TABLE IF EXISTS news_feed;"

# 2. 从备份恢复
wrangler d1 execute cc-test-database --command="CREATE TABLE news_feed AS SELECT * FROM backup_news_feed;"
```

### 6.3 Git 版本回滚

#### 步骤 6.3.1：查看 Git 历史

```bash
# 查看提交历史
git log --oneline --graph --all

# 查看特定提交的详细信息
git show <commit-hash>
```

#### 步骤 6.3.2：回滚到特定提交

```bash
# 回滚到特定提交
git checkout <commit-hash>

# 或回滚到特定标签
git checkout v1.0.0

# 重新部署
vercel --prod
```

#### 步骤 6.3.3：创建新分支进行修复

```bash
# 从当前状态创建新分支
git checkout -b fix-deployment-issue

# 进行修复
# ...

# 提交修复
git add .
git commit -m "Fix deployment issue"

# 合并回主分支
git checkout main
git merge fix-deployment-issue

# 重新部署
vercel --prod
```

### 6.4 紧急回滚流程

如果部署导致严重问题，按照以下紧急回滚流程：

```bash
# 1. 立即回滚 Vercel 部署
vercel rollback <last-stable-deployment-url>

# 2. 验证应用状态
curl https://cc-test.vercel.app/api/health

# 3. 如果数据库有问题，恢复备份
wrangler d1 execute cc-test-database --file=emergency-backup.sql

# 4. 通知团队成员
# 发送通知邮件或消息

# 5. 创建问题报告
# 记录问题、原因和解决方案
```

---

## 7. 部署检查清单

在完成部署后，使用以下清单确认所有步骤都已完成：

### 7.1 部署前检查

- [ ] 操作系统满足要求
- [ ] 所有依赖软件已安装
- [ ] 网络连接正常
- [ ] 代码已拉取到本地
- [ ] 环境变量已配置
- [ ] 数据库表已创建
- [ ] 本地测试通过

### 7.2 部署过程检查

- [ ] Vercel CLI 已安装
- [ ] Vercel 账号已登录
- [ ] Vercel 项目已初始化
- [ ] 环境变量已配置
- [ ] 服务器区域已设置
- [ ] 部署命令已执行
- [ ] 部署日志无错误

### 7.3 部署后验证检查

- [ ] 应用可以正常访问
- [ ] 前端功能正常
- [ ] API 端点正常工作
- [ ] 数据库连接正常
- [ ] 性能指标符合要求
- [ ] 浏览器控制台无错误
- [ ] 部署日志正常

### 7.4 文档和监控检查

- [ ] 部署文档已更新
- [ ] 团队已通知部署完成
- [ ] 监控告警已配置
- [ ] 备份策略已确认
- [ ] 回滚计划已准备

---

## 8. 附录

### 8.1 有用的命令速查表

```bash
# Vercel 命令
vercel login                    # 登录 Vercel
vercel --prod                  # 部署到生产环境
vercel ls                       # 列出所有部署
vercel logs                     # 查看日志
vercel env ls                   # 列出环境变量
vercel rollback <url>            # 回滚部署

# Wrangler 命令
wrangler login                  # 登录 Cloudflare
wrangler d1 list                # 列出所有 D1 数据库
wrangler d1 execute <db> --command="SQL"  # 执行 SQL
wrangler d1 execute <db> --file=file.sql  # 执行 SQL 文件
wrangler tail                    # 查看 Worker 日志

# Git 命令
git status                     # 查看文件状态
git add .                      # 添加文件
git commit -m "message"        # 提交更改
git push                       # 推送到远程
git log --oneline            # 查看提交历史
git checkout <branch>           # 切换分支
```

### 8.2 配置文件位置

| 文件 | 位置 | 用途 |
|------|--------|------|
| `.env` | 项目根目录 | 本地环境变量 |
| `.env.example` | 项目根目录 | 环境变量模板 |
| `wrangler.toml` | 项目根目录 | Cloudflare Workers 配置 |
| `vercel.json` | 项目根目录 | Vercel 配置 |
| `package.json` | 项目根目录 | Node.js 依赖 |
| `requirements.txt` | backend/ 目录 | Python 依赖 |
| `database/schema.sql` | database/ 目录 | 数据库表结构 |

### 8.3 重要 URL

| 服务 | URL |
|------|-----|
| Vercel Dashboard | https://vercel.com/dashboard |
| Cloudflare Dashboard | https://dash.cloudflare.com |
| Cloudflare D1 文档 | https://developers.cloudflare.com/d1/ |
| DeepSeek API 文档 | https://platform.deepseek.com/docs |
| 项目部署文档 | DEPLOYMENT.md |
| Cloudflare D1 教程 | CLOUDFLARE_D1_TUTORIAL.md |

---

## 9. 联系支持

如果遇到本文档未涵盖的问题：

1. 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 获取更多部署信息
2. 查看 [CLOUDFLARE_D1_TUTORIAL.md](CLOUDFLARE_D1_TUTORIAL.md) 了解 Cloudflare D1 使用
3. 访问 [Vercel 文档](https://vercel.com/docs)
4. 访问 [Cloudflare Community](https://community.cloudflare.com/)
5. 访问 [DeepSeek 支持](https://platform.deepseek.com/support)

---

**文档版本**: 1.0.0  
**最后更新**: 2025-02-10  
**维护者**: Deployment Team
