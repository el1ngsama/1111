# Vercel 部署指南

## 项目概述

这是一个印尼新闻 PWA 应用，包含：
- **前端**: React + Vite + Tailwind CSS
- **后端**: Python Flask
- **数据库**: Cloudflare D1
- **图片存储**: Cloudflare R2
- **AI 翻译**: DeepSeek API

## 部署步骤

### 1. 准备 Cloudflare 账户信息

#### 1.1 获取 Cloudflare Account ID

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 在页面右侧可以看到 **Account ID**
3. 复制并保存这个 ID

#### 1.2 准备 Cloudflare API Token

1. 在 Cloudflare Dashboard 中点击右上角头像 → **"My Profile"**
2. 选择 **"API Tokens"** 标签
3. 点击 **"Create Token"**
4. 选择 **"Create Custom Token"**
5. 配置权限：
   - **Account** → **D1** → **Edit**
6. 设置 TTL（建议 90 天）
7. 点击 **"Continue to summary"** → **"Create Token"**
8. **重要**：复制并保存 Token（只会显示一次）

#### 1.3 确认 D1 数据库

1. 在 Cloudflare Dashboard 中进入 **Workers & Pages** → **D1**
2. 确认你的数据库已创建
3. 记录数据库 ID（格式：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx）

### 2. 初始化数据库表结构

#### 方式一：使用 Wrangler CLI（推荐）

```bash
# 1. 安装 Wrangler CLI
npm install -g wrangler

# 2. 登录 Cloudflare
wrangler login

# 3. 执行数据库初始化脚本
wrangler d1 execute cc-test-database --file=database/schema.sql

# 4. 验证表是否创建成功
wrangler d1 execute cc-test-database --command="SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
```

#### 方式二：使用 Dashboard

1. 进入 D1 数据库详情页面
2. 点击 **"Console"** 标签
3. 复制 [database/schema.sql](database/schema.sql) 文件的内容
4. 粘贴到 SQL 编辑器中
5. 点击 **"Execute"**

### 3. 配置环境变量

#### 3.1 创建 .env 文件

```bash
# 复制环境变量模板
cp .env.example .env
```

#### 3.2 编辑 .env 文件

```env
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Cloudflare D1 数据库配置
CLOUDFLARE_D1_DATABASE_ID=6fec1b24-3c6c-4f94-aaa5-aa15b0ecaeb3
CLOUDFLARE_API_TOKEN=5bpeAAggUdULNIvmOAIvIRzRuR9nHN8TKHjO4nda
CLOUDFLARE_ACCOUNT_ID=your_account_id_here

# Cloudflare R2 配置（用于图片存储）
R2_ENDPOINT=your_r2_endpoint
R2_ACCESS_KEY=your_r2_access_key
R2_SECRET_KEY=your_r2_secret_key
R2_BUCKET_NAME=your_r2_bucket_name
R2_PUBLIC_URL=your_r2_public_url
```

**重要提示**：
- 将 `your_account_id_here` 替换为你的 Cloudflare Account ID
- 将 `your_deepseek_api_key_here` 替换为你的 DeepSeek API Key
- 如果不使用 R2，可以暂时留空或注释掉相关配置

### 4. 准备 Cloudflare R2（图片存储，可选）

1. 在 Cloudflare Dashboard 中进入 **R2**
2. 创建新的 R2 Bucket
3. 获取访问凭证（Endpoint, Access Key, Secret Key）
4. 设置公共访问 URL

### 5. 部署到 Vercel

#### 步骤 5.1: 安装 Vercel CLI

```bash
npm install -g vercel
```

#### 步骤 5.2: 登录 Vercel

```bash
vercel login
```

#### 步骤 5.3: 配置 Vercel 环境变量

在 Vercel 项目设置中添加以下环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `DEEPSEEK_API_KEY` | 你的 DeepSeek API Key | AI 翻译服务 |
| `CLOUDFLARE_D1_DATABASE_ID` | `6fec1b24-3c6c-4f94-aaa5-aa15b0ecaeb3` | 数据库 ID |
| `CLOUDFLARE_API_TOKEN` | `5bpeAAggUdULNIvmOAIvIRzRuR9nHN8TKHjO4nda` | API Token |
| `CLOUDFLARE_ACCOUNT_ID` | 你的 Cloudflare Account ID | 账户 ID |
| `R2_ENDPOINT` | R2 Endpoint | 图片存储 |
| `R2_ACCESS_KEY` | R2 Access Key | 图片存储认证 |
| `R2_SECRET_KEY` | R2 Secret Key | 图片存储认证 |
| `R2_BUCKET_NAME` | R2 Bucket 名称 | 图片存储桶 |
| `R2_PUBLIC_URL` | R2 公共 URL | 图片访问地址 |

#### 步骤 5.4: 部署项目

```bash
# 在项目根目录执行
vercel
```

按照提示操作：
1. 选择 "Set up and deploy"
2. 选择项目范围
3. 确认项目设置
4. 等待部署完成

### 6. 配置服务器区域

部署完成后，在 Vercel 项目设置中：

1. 进入 **Settings** > **General**
2. 在 **Regions** 部分，选择以下区域之一：
   - **Singapore (sin1)** - 新加坡（推荐）
   - **Hong Kong (hkg1)** - 香港（备选）
3. 保存设置

### 7. 验证部署

1. 访问 Vercel 提供的部署 URL
2. 测试以下功能：
   - 访问首页
   - 获取新闻列表（`/api/news`）
   - 查看文章详情（`/api/article?url=...`）
   - 单词分析（`/api/analyze/word`）

## 数据库管理

### 查看数据库表

```bash
wrangler d1 execute cc-test-database --command="SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
```

### 查看表结构

```bash
wrangler d1 execute cc-test-database --command="PRAGMA table_info(news_feed);"
```

### 查询数据

```bash
# 查看所有新闻
wrangler d1 execute cc-test-database --command="SELECT * FROM news_feed LIMIT 10;"

# 查看特定日期的新闻
wrangler d1 execute cc-test-database --command="SELECT * FROM news_feed WHERE date(published_at) = '2025-02-10';"
```

### 清空表

```bash
# 清空新闻表
wrangler d1 execute cc-test-database --command="DELETE FROM news_feed;"
```

## 常见问题

### Q: 部署失败怎么办？

A: 检查以下几点：
1. 确保所有环境变量已正确配置
2. 检查 Vercel 构建日志
3. 确认 Python 版本兼容性

### Q: 数据库连接失败？

A: 
1. 验证 Cloudflare Account ID、API Token 和数据库 ID 是否正确
2. 检查 API Token 权限（需要 D1 Edit 权限）
3. 确认数据库表是否已创建
4. 使用 `wrangler d1 list` 查看数据库列表

### Q: 图片无法加载？

A:
1. 检查 R2 配置
2. 确认 R2 Bucket 已设置为公共访问
3. 验证 R2_PUBLIC_URL 配置

### Q: 翻译功能不工作？

A:
1. 验证 DEEPSEEK_API_KEY 是否正确
2. 检查 DeepSeek API 配额
3. 查看后端日志

### Q: 如何获取 Cloudflare Account ID？

A:
1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 在页面右侧可以看到 **Account ID**
3. 点击复制按钮复制 ID

### Q: 如何重新初始化数据库？

A:
```bash
# 删除所有表
wrangler d1 execute cc-test-database --command="DROP TABLE IF EXISTS news_feed; DROP TABLE IF EXISTS vocabulary; DROP TABLE IF EXISTS daily_digest;"

# 重新创建表
wrangler d1 execute cc-test-database --file=database/schema.sql
```

## 更新部署

当代码更新后，重新部署：

```bash
vercel --prod
```

## 本地开发

```bash
# 安装前端依赖
npm install

# 安装后端依赖
cd backend
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的配置

# 启动前端
npm run dev

# 启动后端
cd backend
python app.py
```

## 数据库初始化脚本

项目包含一个数据库初始化脚本，可以帮助你检查配置和初始化数据库：

```bash
# 运行初始化脚本
python scripts/init_db.py
```

这个脚本会：
1. 检查必要的环境变量
2. 显示当前配置
3. 测试数据库连接
4. 提供初始化步骤说明

## 技术支持

如有问题，请检查：
- [Vercel 文档](https://vercel.com/docs)
- [Cloudflare D1 文档](https://developers.cloudflare.com/d1/)
- [Cloudflare D1 教程](CLOUDFLARE_D1_TUTORIAL.md)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [Cloudflare Community Forum](https://community.cloudflare.com/)

## 安全建议

1. **不要将敏感信息提交到版本控制**
   - 确保 `.env` 文件在 `.gitignore` 中
   - 不要在代码中硬编码密钥

2. **定期轮换 API Token**
   - 每 90 天更换一次 Cloudflare API Token
   - 定期更新 DeepSeek API Key

3. **使用最小权限原则**
   - 只授予必要的权限
   - 为不同环境创建不同的 Token

4. **启用日志记录**
   - 记录所有数据库访问
   - 监控异常访问模式
