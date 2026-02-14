# Cloudflare D1 数据库新手完整教程

> 本教程专为 Cloudflare 新手用户设计，从零开始教你如何创建、配置和使用 Cloudflare D1 数据库。

---

## 目录

1. [Cloudflare 账户注册与登录](#1-cloudflare-账户注册与登录)
2. [D1 数据库基本概念](#2-d1-数据库基本概念)
3. [创建 D1 数据库](#3-创建-d1-数据库)
4. [数据库初始化配置](#4-数据库初始化配置)
5. [基本 SQL 操作示例](#5-基本-sql-操作示例)
6. [权限管理设置](#6-权限管理设置)
7. [与 Cloudflare Workers 集成](#7-与-cloudflare-workers-集成)
8. [数据备份与恢复策略](#8-数据备份与恢复策略)
9. [常见问题排查指南](#9-常见问题排查指南)

---

## 1. Cloudflare 账户注册与登录

### 1.1 注册 Cloudflare 账户

#### 步骤 1：访问 Cloudflare 官网
打开浏览器，访问 [https://dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up)

#### 步骤 2：填写注册信息
在注册页面填写以下信息：
- **电子邮件地址**：使用你的常用邮箱
- **密码**：设置一个强密码（至少 8 个字符，包含字母和数字）
- **确认密码**：再次输入密码

#### 步骤 3：验证邮箱
1. 提交注册信息后，Cloudflare 会向你填写的邮箱发送验证邮件
2. 登录你的邮箱，找到来自 Cloudflare 的验证邮件
3. 点击邮件中的 "Verify Email" 按钮或链接
4. 验证成功后会自动跳转到 Cloudflare Dashboard

#### 步骤 4：完善账户信息（可选）
首次登录后，系统可能会要求你：
- 设置账户名称
- 选择使用场景（个人/企业）
- 添加支付方式（免费账户不需要，但建议添加以便后续升级）

### 1.2 登录 Cloudflare 账户

#### 方式一：网页登录
1. 访问 [https://dash.cloudflare.com](https://dash.cloudflare.com)
2. 输入注册时的邮箱和密码
3. 点击 "Sign In" 按钮

#### 方式二：使用 Google 账号登录（推荐）
1. 在登录页面点击 "Continue with Google"
2. 选择你的 Google 账号
3. 授权 Cloudflare 访问你的账号信息

#### 登录安全设置
建议启用以下安全功能：
- **两步验证（2FA）**：在账户设置中启用
- **登录通知**：收到新设备登录通知
- **API Token 管理**：为不同应用创建独立的 API Token

---

## 2. D1 数据库基本概念

### 2.1 什么是 Cloudflare D1？

Cloudflare D1 是 Cloudflare 推出的**无服务器 SQL 数据库**，基于 SQLite 构建，专为边缘计算环境设计。它让开发者能够在 Cloudflare 的全球边缘网络上运行数据库查询，实现超低延迟的数据访问。

### 2.2 D1 的核心特性

#### ✅ 全球分布式部署
- 数据库自动复制到 Cloudflare 的全球边缘节点
- 用户请求从最近的边缘节点响应，延迟极低
- 无需手动配置多地域部署

#### ✅ 无服务器架构
- 无需管理服务器实例
- 自动扩缩容，根据流量自动调整资源
- 按实际使用量计费

#### ✅ SQLite 兼容
- 完全兼容 SQLite 语法
- 支持标准 SQL 查询
- 可以使用现有的 SQLite 工具和库

#### ✅ 与 Workers 无缝集成
- 通过 Worker 绑定直接访问数据库
- 支持 TypeScript/JavaScript 类型安全
- 简化的 API 调用

#### ✅ 免费额度（2025年）
- **存储空间**：5 GB
- **读取操作**：每天 500 万次
- **写入操作**：每天 10 万次
- **数据库数量**：每个账户 10 个

### 2.3 适用场景

#### 适合使用 D1 的场景
- ✅ 需要全球低延迟访问的应用
- ✅ 中小规模的数据存储需求
- ✅ 与 Cloudflare Workers 配合使用
- ✅ 内容管理系统（CMS）
- ✅ 用户配置和偏好设置
- ✅ 分析数据和日志存储

#### 不适合使用 D1 的场景
- ❌ 需要复杂关系型数据库功能的应用
- ❌ 超大规模数据存储（TB 级别）
- ❌ 需要实时数据同步的场景
- ❌ 复杂的事务处理需求

### 2.4 D1 与传统数据库对比

| 特性 | Cloudflare D1 | MySQL/PostgreSQL | MongoDB |
|------|---------------|------------------|---------|
| 部署方式 | 无服务器 | 需要服务器 | 需要服务器 |
| 全球分布 | 自动 | 手动配置 | 手动配置 |
| 延迟 | 极低（边缘） | 中等 | 中等 |
| 扩展性 | 自动 | 手动 | 手动 |
| SQL 支持 | SQLite | 完整 | 有限 |
| 免费额度 | 5GB/天 | 通常无 | 通常无 |
| 管理复杂度 | 低 | 高 | 中等 |

---

## 3. 创建 D1 数据库

### 3.1 方式一：通过 Dashboard 图形界面创建

#### 步骤 1：进入 D1 管理页面

1. 登录 Cloudflare Dashboard：[https://dash.cloudflare.com](https://dash.cloudflare.com)
2. 在左侧导航栏中找到 **"Workers & Pages"**
3. 点击展开后选择 **"D1"**
4. 点击 **"Create database"** 按钮

```
┌─────────────────────────────────────────────────────────────┐
│  Cloudflare Dashboard                                       │
│                                                             │
│  [Home] [Workers & Pages ▼] [R2] [Zero Trust] [Security]   │
│                            └─ Workers                       │
│                            └─ Pages                         │
│                            └─ D1 ← 点击这里                 │
│                            └─ KV                            │
│                            └─ Durable Objects              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 步骤 2：填写数据库信息

在创建页面填写以下信息：

| 字段 | 说明 | 示例 |
|------|------|------|
| **Database name** | 数据库名称（必填） | `my-first-database` |
| **Location** | 数据库位置（可选） | 选择离用户最近的区域 |

**命名规则**：
- 只能包含小写字母、数字和连字符
- 不能以连字符开头或结尾
- 长度：3-63 个字符
- 必须在账户内唯一

#### 步骤 3：创建并获取数据库信息

点击 **"Create"** 按钮后，系统会创建数据库并显示以下重要信息：

```
┌─────────────────────────────────────────────────────────────┐
│  Database created successfully!                              │
│                                                             │
│  Database ID:  xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx         │
│  Database name: my-first-database                           │
│  Created at:  2025-02-10 10:30:00 UTC                        │
│                                                             │
│  [Copy Database ID] [View Dashboard]                         │
└─────────────────────────────────────────────────────────────┘
```

**重要提示**：请务必复制并保存 **Database ID**，后续配置时需要使用！

#### 步骤 4：查看数据库详情

创建成功后，你会进入数据库详情页面，可以看到：

- **数据库概览**：存储使用量、读写操作统计
- **控制台**：在线 SQL 查询界面
- **数据导入/导出**：数据备份和恢复功能
- **设置**：数据库配置选项

---

### 3.2 方式二：通过 Wrangler 命令行工具创建

#### 步骤 1：安装 Wrangler CLI

**前提条件**：需要先安装 [Node.js](https://nodejs.org/)（建议 v16 或更高版本）

##### Windows 系统
```bash
# 使用 npm 安装（推荐）
npm install -g wrangler

# 或使用 yarn
yarn global add wrangler

# 或使用 pnpm
pnpm add -g wrangler
```

##### macOS/Linux 系统
```bash
# 使用 npm 安装
npm install -g wrangler

# 或使用 Homebrew（macOS）
brew install wrangler
```

#### 步骤 2：登录 Cloudflare 账户

```bash
# 登录命令
wrangler login

# 执行后会打开浏览器进行授权
# 授权成功后会显示：
# ⛅️ wrangler 3.x.x
# -------------------
# ⚡️ Successfully logged in with your Cloudflare account!
```

#### 步骤 3：创建 D1 数据库

```bash
# 创建数据库
wrangler d1 create my-first-database

# 输出示例：
# 🌀 Creating database 'my-first-database'...
# ✅ Successfully created DB!
# 
# [[d1_databases]]
# binding = "DB"
# database_name = "my-first-database"
# database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

**重要**：复制输出的 `database_id`，保存到安全的地方！

#### 步骤 4：配置 wrangler.toml 文件

在项目根目录创建 `wrangler.toml` 文件：

```toml
name = "my-worker"
main = "src/index.js"
compatibility_date = "2024-01-01"

# D1 数据库绑定
[[d1_databases]]
binding = "DB"  # 在 Worker 代码中使用的变量名
database_name = "my-first-database"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # 替换为你的数据库 ID
```

#### 步骤 5：验证数据库创建

```bash
# 列出所有 D1 数据库
wrangler d1 list

# 输出示例：
# [
#   {
#     "name": "my-first-database",
#     "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#     "created_at": "2025-02-10T10:30:00Z",
#     "version": "1"
#   }
# ]

# 查看数据库详细信息
wrangler d1 info my-first-database
```

---

### 3.3 Wrangler 常用命令速查表

| 命令 | 说明 | 示例 |
|------|------|------|
| `wrangler d1 create <name>` | 创建数据库 | `wrangler d1 create mydb` |
| `wrangler d1 list` | 列出所有数据库 | `wrangler d1 list` |
| `wrangler d1 info <name>` | 查看数据库信息 | `wrangler d1 info mydb` |
| `wrangler d1 delete <name>` | 删除数据库 | `wrangler d1 delete mydb` |
| `wrangler d1 execute <name> --command="SQL"` | 执行 SQL 命令 | `wrangler d1 execute mydb --command="SELECT * FROM users"` |
| `wrangler d1 execute <name> --file=sqlfile.sql` | 执行 SQL 文件 | `wrangler d1 execute mydb --file=schema.sql` |
| `wrangler d1 export <name> --output=backup.sql` | 导出数据库 | `wrangler d1 export mydb --output=backup.sql` |

---

## 4. 数据库初始化配置

### 4.1 创建表结构

#### 方式一：通过 Dashboard 控制台

1. 进入 D1 数据库详情页面
2. 点击 **"Console"** 标签
3. 在 SQL 编辑器中输入创建表的 SQL 语句
4. 点击 **"Execute"** 或按 `Ctrl+Enter` 执行

#### 示例：创建用户表

```sql
-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
```

#### 方式二：通过 Wrangler CLI

创建 `schema.sql` 文件：

```sql
-- schema.sql

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 文章表
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    published_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 评论表
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_articles_author ON articles(author_id);
CREATE INDEX IF NOT EXISTS idx_comments_article ON comments(article_id);
CREATE INDEX IF NOT EXISTS idx_comments_user ON comments(user_id);
```

执行 SQL 文件：

```bash
# 执行 schema.sql 文件
wrangler d1 execute my-first-database --file=schema.sql

# 输出示例：
# 🌀 Executing on database my-first-database...
# ✅ Executed 4 commands in 123ms
```

### 4.2 插入初始数据

#### 示例：插入测试数据

```sql
-- 插入测试用户
INSERT INTO users (email, username, password_hash) VALUES
    ('user1@example.com', 'alice', '$2a$10$abcdefghijklmnopqrstuvwxyz'),
    ('user2@example.com', 'bob', '$2a$10$abcdefghijklmnopqrstuvwxyz'),
    ('user3@example.com', 'charlie', '$2a$10$abcdefghijklmnopqrstuvwxyz');

-- 插入测试文章
INSERT INTO articles (title, content, author_id) VALUES
    ('我的第一篇文章', '这是文章内容...', 1),
    ('Cloudflare D1 入门', 'D1 是一个强大的数据库...', 2),
    ('无服务器架构最佳实践', '本文介绍无服务器架构...', 1);

-- 插入测试评论
INSERT INTO comments (article_id, user_id, content) VALUES
    (1, 2, '很好的文章！'),
    (1, 3, '学到了很多'),
    (2, 1, '期待更多教程');
```

### 4.3 验证表结构

```sql
-- 查看所有表
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- 查看表结构
PRAGMA table_info(users);

-- 查看索引
SELECT name FROM sqlite_master WHERE type='index' ORDER BY name;
```

---

## 5. 基本 SQL 操作示例

### 5.1 CRUD 操作（增删改查）

#### CREATE - 插入数据

```sql
-- 插入单条记录
INSERT INTO users (email, username, password_hash)
VALUES ('newuser@example.com', 'newuser', 'hashed_password');

-- 插入多条记录
INSERT INTO articles (title, content, author_id) VALUES
    ('文章标题1', '文章内容1...', 1),
    ('文章标题2', '文章内容2...', 2),
    ('文章标题3', '文章内容3...', 1);

-- 插入并返回插入的 ID
INSERT INTO users (email, username, password_hash)
VALUES ('another@example.com', 'another', 'hash')
RETURNING id;
```

#### READ - 查询数据

```sql
-- 查询所有用户
SELECT * FROM users;

-- 查询特定字段
SELECT id, username, email FROM users;

-- 条件查询
SELECT * FROM users WHERE username = 'alice';

-- 模糊查询
SELECT * FROM users WHERE username LIKE '%ali%';

-- 排序
SELECT * FROM articles ORDER BY published_at DESC;

-- 限制结果数量
SELECT * FROM articles LIMIT 10;

-- 分页查询
SELECT * FROM articles 
ORDER BY published_at DESC 
LIMIT 10 OFFSET 20;  -- 第 3 页（每页 10 条）

-- 连接查询
SELECT 
    a.title,
    a.content,
    u.username as author_name
FROM articles a
JOIN users u ON a.author_id = u.id;

-- 聚合查询
SELECT 
    author_id,
    COUNT(*) as article_count
FROM articles
GROUP BY author_id;

-- 子查询
SELECT * FROM users
WHERE id IN (SELECT author_id FROM articles);
```

#### UPDATE - 更新数据

```sql
-- 更新单个字段
UPDATE users 
SET username = 'alice_new' 
WHERE id = 1;

-- 更新多个字段
UPDATE users 
SET email = 'newemail@example.com',
    updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- 条件更新
UPDATE articles 
SET title = '新标题'
WHERE author_id = 1 AND published_at < '2025-01-01';

-- 批量更新
UPDATE articles 
SET updated_at = CURRENT_TIMESTAMP
WHERE published_at < '2025-02-01';
```

#### DELETE - 删除数据

```sql
-- 删除单条记录
DELETE FROM users WHERE id = 1;

-- 条件删除
DELETE FROM articles WHERE published_at < '2025-01-01';

-- 批量删除
DELETE FROM comments WHERE created_at < '2025-01-01';

-- 删除所有数据（保留表结构）
DELETE FROM users;

-- 删除表
DROP TABLE IF EXISTS users;
```

### 5.2 查询优化技巧

#### 使用索引

```sql
-- 创建索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_articles_published ON articles(published_at DESC);

-- 复合索引
CREATE INDEX idx_articles_author_published 
ON articles(author_id, published_at DESC);
```

#### 查询优化建议

```sql
-- ✅ 好的查询（使用索引）
SELECT * FROM users WHERE email = 'user@example.com';

-- ❌ 不好的查询（不使用索引）
SELECT * FROM users WHERE email LIKE '%example.com';

-- ✅ 好的查询（限制结果）
SELECT * FROM articles LIMIT 10;

-- ❌ 不好的查询（获取所有数据）
SELECT * FROM articles;

-- ✅ 好的查询（只查询需要的字段）
SELECT id, title FROM articles;

-- ❌ 不好的查询（查询所有字段）
SELECT * FROM articles;
```

### 5.3 事务处理

```sql
-- 开始事务
BEGIN TRANSACTION;

-- 执行多个操作
INSERT INTO users (email, username, password_hash)
VALUES ('user1@example.com', 'user1', 'hash1');

INSERT INTO articles (title, content, author_id)
VALUES ('文章1', '内容1', 1);

-- 提交事务
COMMIT;

-- 或者回滚事务
-- ROLLBACK;

-- 示例：安全的事务处理
BEGIN TRANSACTION;

-- 检查用户是否存在
SELECT id FROM users WHERE email = 'existing@example.com';

-- 如果用户不存在，插入新用户
INSERT OR IGNORE INTO users (email, username, password_hash)
VALUES ('existing@example.com', 'user', 'hash');

-- 插入文章
INSERT INTO articles (title, content, author_id)
VALUES ('新文章', '内容', (SELECT id FROM users WHERE email = 'existing@example.com'));

COMMIT;
```

---

## 6. 权限管理设置

### 6.1 API Token 管理

#### 创建 API Token

1. 登录 Cloudflare Dashboard
2. 点击右上角头像 → **"My Profile"**
3. 选择 **"API Tokens"** 标签
4. 点击 **"Create Token"** 按钮

#### Token 权限配置

| 权限类型 | 说明 | 推荐设置 |
|---------|------|---------|
| **Account** | 账户级别权限 | `Cloudflare D1 - Edit` |
| **Zone** | 域名级别权限 | 通常不需要 |
| **User** | 用户级别权限 | 通常不需要 |

#### 创建 D1 专用 Token

```json
{
  "name": "D1 Database Token",
  "policies": [
    {
      "effect": "allow",
      "permission_groups": [
        {
          "id": "d1_database_edit",
          "account": {
            "id": "your_account_id"
          }
        }
      ]
    }
  ],
  "ttl": "8760h"
}
```

**重要提示**：
- Token 创建后只会显示一次，请立即复制保存
- 建议为不同环境（开发/生产）创建不同的 Token
- 定期轮换 Token 以提高安全性

### 6.2 访问控制配置

#### Worker 访问控制

在 Worker 代码中实现访问控制：

```javascript
// worker.js
export default {
  async fetch(request, env, ctx) {
    // 验证 API Token
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return new Response('Unauthorized', { status: 401 });
    }

    const token = authHeader.substring(7);
    if (token !== env.API_TOKEN) {
      return new Response('Invalid token', { status: 403 });
    }

    // 继续处理请求
    const { results } = await env.DB.prepare('SELECT * FROM users').all();
    return Response.json(results);
  }
};
```

#### IP 白名单（可选）

```javascript
// worker.js
const ALLOWED_IPS = ['1.2.3.4', '5.6.7.8'];

export default {
  async fetch(request, env, ctx) {
    const clientIP = request.headers.get('CF-Connecting-IP');
    
    if (!ALLOWED_IPS.includes(clientIP)) {
      return new Response('Access denied', { status: 403 });
    }

    // 继续处理请求
    // ...
  }
};
```

### 6.3 安全最佳实践

#### ✅ 推荐做法

1. **使用环境变量存储敏感信息**
   ```javascript
   // wrangler.toml
   [vars]
   API_TOKEN = "your_token_here"
   ```

2. **最小权限原则**
   - 只授予必要的权限
   - 为不同功能创建不同的 Token

3. **定期轮换密钥**
   - 每 90 天更换一次 API Token
   - 使用密钥管理服务

4. **启用日志记录**
   ```javascript
   console.log(`Database access from ${clientIP} at ${new Date().toISOString()}`);
   ```

5. **使用 HTTPS**
   - 所有 API 请求必须使用 HTTPS
   - Cloudflare 自动提供 SSL 证书

#### ❌ 避免的做法

1. ❌ 在代码中硬编码密钥
   ```javascript
   // 错误示例
   const API_TOKEN = 'sk-1234567890abcdef';
   ```

2. ❌ 将密钥提交到版本控制
   ```bash
   # 确保 .gitignore 包含
   .env
   wrangler.toml
   ```

3. ❌ 使用过期的 Token
   - 定期检查 Token 有效期
   - 及时更新即将过期的 Token

4. ❌ 忽略错误日志
   - 记录所有数据库访问
   - 监控异常访问模式

---

## 7. 与 Cloudflare Workers 集成

### 7.1 Worker 绑定 D1 数据库

#### 配置 wrangler.toml

```toml
name = "my-worker"
main = "src/index.js"
compatibility_date = "2024-01-01"

# D1 数据库绑定
[[d1_databases]]
binding = "DB"  # 在 Worker 代码中使用的变量名
database_name = "my-first-database"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# 环境变量
[vars]
API_TOKEN = "your_api_token_here"

# 生产环境配置
[env.production]
[[env.production.d1_databases]]
binding = "DB"
database_name = "my-first-database-prod"
database_id = "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
```

### 7.2 Worker 代码示例

#### 基础 CRUD API

```javascript
// src/index.js

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // 路由处理
    if (path === '/api/users' && request.method === 'GET') {
      return getUsers(request, env);
    } else if (path === '/api/users' && request.method === 'POST') {
      return createUser(request, env);
    } else if (path.startsWith('/api/users/') && request.method === 'GET') {
      const id = path.split('/')[3];
      return getUserById(id, env);
    } else if (path.startsWith('/api/users/') && request.method === 'PUT') {
      const id = path.split('/')[3];
      return updateUser(id, request, env);
    } else if (path.startsWith('/api/users/') && request.method === 'DELETE') {
      const id = path.split('/')[3];
      return deleteUser(id, env);
    }

    return new Response('Not Found', { status: 404 });
  }
};

// 获取所有用户
async function getUsers(request, env) {
  try {
    const { results } = await env.DB.prepare('SELECT * FROM users').all();
    return Response.json({
      success: true,
      data: results
    });
  } catch (error) {
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
}

// 创建用户
async function createUser(request, env) {
  try {
    const { email, username, password_hash } = await request.json();

    const result = await env.DB.prepare(
      'INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)'
    ).bind(email, username, password_hash).run();

    return Response.json({
      success: true,
      data: { id: result.meta.last_row_id }
    }, { status: 201 });
  } catch (error) {
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
}

// 获取单个用户
async function getUserById(id, env) {
  try {
    const result = await env.DB.prepare(
      'SELECT * FROM users WHERE id = ?'
    ).bind(id).first();

    if (!result) {
      return Response.json({
        success: false,
        error: 'User not found'
      }, { status: 404 });
    }

    return Response.json({
      success: true,
      data: result
    });
  } catch (error) {
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
}

// 更新用户
async function updateUser(id, request, env) {
  try {
    const { email, username } = await request.json();

    const result = await env.DB.prepare(
      'UPDATE users SET email = ?, username = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
    ).bind(email, username, id).run();

    if (result.meta.changes === 0) {
      return Response.json({
        success: false,
        error: 'User not found'
      }, { status: 404 });
    }

    return Response.json({
      success: true,
      message: 'User updated successfully'
    });
  } catch (error) {
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
}

// 删除用户
async function deleteUser(id, env) {
  try {
    const result = await env.DB.prepare(
      'DELETE FROM users WHERE id = ?'
    ).bind(id).run();

    if (result.meta.changes === 0) {
      return Response.json({
        success: false,
        error: 'User not found'
      }, { status: 404 });
    }

    return Response.json({
      success: true,
      message: 'User deleted successfully'
    });
  } catch (error) {
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
}
```

#### 复杂查询示例

```javascript
// 获取用户及其文章
async function getUserWithArticles(userId, env) {
  try {
    // 获取用户信息
    const user = await env.DB.prepare(
      'SELECT id, username, email FROM users WHERE id = ?'
    ).bind(userId).first();

    if (!user) {
      return Response.json({
        success: false,
        error: 'User not found'
      }, { status: 404 });
    }

    // 获取用户的文章
    const articles = await env.DB.prepare(
      'SELECT * FROM articles WHERE author_id = ? ORDER BY published_at DESC'
    ).bind(userId).all();

    return Response.json({
      success: true,
      data: {
        user,
        articles: articles.results
      }
    });
  } catch (error) {
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
}

// 分页查询
async function getArticlesPaginated(page, limit, env) {
  try {
    const offset = (page - 1) * limit;

    // 获取总数
    const countResult = await env.DB.prepare(
      'SELECT COUNT(*) as total FROM articles'
    ).first();
    const total = countResult.total;

    // 获取分页数据
    const articles = await env.DB.prepare(
      'SELECT * FROM articles ORDER BY published_at DESC LIMIT ? OFFSET ?'
    ).bind(limit, offset).all();

    return Response.json({
      success: true,
      data: {
        articles: articles.results,
        pagination: {
          page,
          limit,
          total,
          totalPages: Math.ceil(total / limit)
        }
      }
    });
  } catch (error) {
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
}
```

### 7.3 部署 Worker

#### 本地测试

```bash
# 启动本地开发服务器
wrangler dev

# 访问 http://localhost:8787 测试 API
```

#### 部署到生产环境

```bash
# 部署到默认环境
wrangler deploy

# 部署到生产环境
wrangler deploy --env production

# 指定入口文件部署
wrangler deploy src/index.js
```

#### 查看部署状态

```bash
# 查看所有 Workers
wrangler deployments list

# 查看特定 Worker 的部署
wrangler deployments list --name my-worker

# 回滚到上一个版本
wrangler rollback --name my-worker
```

---

## 8. 数据备份与恢复策略

### 8.1 数据导出方法

#### 方式一：通过 Wrangler CLI 导出

```bash
# 导出整个数据库
wrangler d1 export my-first-database --output=backup.sql

# 导出特定表
wrangler d1 execute my-first-database --command="SELECT * FROM users" --output=users.json

# 导出为 JSON 格式
wrangler d1 execute my-first-database --command="SELECT * FROM articles" --output=articles.json --json
```

#### 方式二：通过 Dashboard 导出

1. 进入 D1 数据库详情页面
2. 点击 **"Export"** 标签
3. 选择导出格式（SQL、JSON、CSV）
4. 点击 **"Export"** 按钮
5. 下载导出的文件

#### 方式三：通过 Worker API 导出

```javascript
// 导出数据的 Worker 端点
async function exportData(request, env) {
  const { results } = await env.DB.prepare('SELECT * FROM users').all();
  
  // 转换为 JSON
  const jsonData = JSON.stringify(results, null, 2);
  
  return new Response(jsonData, {
    headers: {
      'Content-Type': 'application/json',
      'Content-Disposition': 'attachment; filename="users.json"'
    }
  });
}
```

### 8.2 数据导入恢复

#### 方式一：通过 Wrangler CLI 导入

```bash
# 从 SQL 文件导入
wrangler d1 execute my-first-database --file=backup.sql

# 从 JSON 文件导入（需要编写转换脚本）
wrangler d1 execute my-first-database --file=import.sql

# 执行单条 SQL 命令
wrangler d1 execute my-first-database --command="INSERT INTO users (email, username) VALUES ('test@example.com', 'test')"
```

#### 方式二：通过 Dashboard 导入

1. 进入 D1 数据库详情页面
2. 点击 **"Import"** 标签
3. 选择要导入的文件（SQL、JSON、CSV）
4. 配置导入选项（覆盖、追加等）
5. 点击 **"Import"** 按钮

#### 方式三：通过 Worker API 导入

```javascript
// 导入数据的 Worker 端点
async function importData(request, env) {
  const data = await request.json();
  
  try {
    // 清空现有数据
    await env.DB.prepare('DELETE FROM users').run();
    
    // 批量插入新数据
    for (const user of data) {
      await env.DB.prepare(
        'INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)'
      ).bind(user.email, user.username, user.password_hash).run();
    }
    
    return Response.json({
      success: true,
      message: `Imported ${data.length} records`
    });
  } catch (error) {
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
}
```

### 8.3 自动化备份方案

#### 使用 Cloudflare Cron Triggers

```javascript
// worker.js
export default {
  async fetch(request, env, ctx) {
    // 正常的请求处理
    // ...
  },
  
  // 定时任务：每天凌晨 2 点备份
  async scheduled(event, env, ctx) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `backup-${timestamp}.sql`;
    
    try {
      // 导出数据库
      const { results } = await env.DB.prepare(
        "SELECT sql FROM sqlite_master WHERE type='table'"
      ).all();
      
      // 保存到 R2 或其他存储
      await env.R2.put(filename, JSON.stringify(results));
      
      console.log(`Backup completed: ${filename}`);
    } catch (error) {
      console.error(`Backup failed: ${error.message}`);
    }
  }
};
```

#### 配置 Cron Triggers

```toml
# wrangler.toml
[triggers]
crons = ["0 2 * * *"]  # 每天凌晨 2 点执行
```

#### 使用 GitHub Actions 自动备份

```yaml
# .github/workflows/backup.yml
name: Backup D1 Database

on:
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨 2 点
  workflow_dispatch:  # 手动触发

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install Wrangler
        run: npm install -g wrangler
      
      - name: Backup database
        run: |
          wrangler d1 export my-first-database --output=backup.sql
          mv backup.sql backups/backup-$(date +%Y%m%d-%H%M%S).sql
      
      - name: Commit backup
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add backups/
          git commit -m "Backup database"
          git push
```

### 8.4 备份策略建议

#### 备份频率

| 数据类型 | 备份频率 | 保留期限 |
|---------|---------|---------|
| 生产数据 | 每天一次 | 30 天 |
| 开发数据 | 每周一次 | 7 天 |
| 测试数据 | 按需备份 | 3 天 |

#### 备份存储位置

- **Cloudflare R2**：推荐，与 D1 集成良好
- **GitHub/GitLab**：适合小型项目
- **AWS S3**：适合已有 AWS 基础设施的项目
- **本地存储**：不推荐，存在丢失风险

#### 备份验证

```javascript
// 验证备份的 Worker 端点
async function verifyBackup(request, env) {
  try {
    // 获取备份文件
    const backup = await env.R2.get('backup-latest.sql');
    
    if (!backup) {
      return Response.json({
        success: false,
        error: 'Backup not found'
      }, { status: 404 });
    }
    
    // 解析并验证数据
    const data = await backup.text();
    const records = JSON.parse(data);
    
    return Response.json({
      success: true,
      data: {
        timestamp: backup.uploaded,
        recordCount: records.length,
        size: backup.size
      }
    });
  } catch (error) {
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
}
```

---

## 9. 常见问题排查指南

### 9.1 连接问题

#### 问题 1：无法连接到数据库

**症状**：
- Worker 返回 500 错误
- 日志显示 "Database connection failed"

**排查步骤**：

1. 检查 `wrangler.toml` 配置
   ```toml
   [[d1_databases]]
   binding = "DB"
   database_name = "my-first-database"
   database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # 确认 ID 正确
   ```

2. 验证数据库是否存在
   ```bash
   wrangler d1 list
   ```

3. 检查 Worker 代码中的绑定名称
   ```javascript
   // 确保使用正确的绑定名称
   const { results } = await env.DB.prepare('SELECT * FROM users').all();
   ```

4. 查看日志
   ```bash
   wrangler tail
   ```

**解决方案**：
- 确保 `database_id` 正确
- 重新部署 Worker
- 检查网络连接

---

#### 问题 2：超时错误

**症状**：
- 查询执行时间过长
- 返回 "504 Gateway Timeout"

**排查步骤**：

1. 检查查询复杂度
   ```sql
   -- 使用 EXPLAIN 分析查询
   EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'user@example.com';
   ```

2. 检查是否有索引
   ```sql
   -- 查看表的索引
   PRAGMA index_list('users');
   ```

3. 限制返回结果数量
   ```javascript
   // 添加 LIMIT 限制
   const { results } = await env.DB.prepare('SELECT * FROM users LIMIT 100').all();
   ```

**解决方案**：
- 添加适当的索引
- 优化查询语句
- 使用分页查询
- 考虑使用缓存

---

### 9.2 性能问题

#### 问题 3：查询速度慢

**症状**：
- API 响应时间长
- 数据库查询耗时超过 1 秒

**排查步骤**：

1. 分析慢查询
   ```javascript
   // 添加计时
   const startTime = Date.now();
   const { results } = await env.DB.prepare('SELECT * FROM users').all();
   const duration = Date.now() - startTime;
   console.log(`Query took ${duration}ms`);
   ```

2. 检查表大小
   ```sql
   -- 查看表行数
   SELECT COUNT(*) FROM users;
   ```

3. 检查索引使用情况
   ```sql
   -- 查看索引信息
   PRAGMA index_info('idx_users_email');
   ```

**解决方案**：
- 为常用查询字段创建索引
- 避免 `SELECT *`，只查询需要的字段
- 使用 `LIMIT` 限制结果数量
- 考虑使用缓存减少数据库访问

---

#### 问题 4：写入性能差

**症状**：
- 批量插入速度慢
- 写入操作超时

**排查步骤**：

1. 检查是否有大量索引
   ```sql
   -- 查看所有索引
   SELECT name FROM sqlite_master WHERE type='index';
   ```

2. 检查事务使用
   ```javascript
   // 确保使用事务批量插入
   BEGIN TRANSACTION;
   // ... 多个插入操作
   COMMIT;
   ```

**解决方案**：
- 使用事务批量操作
- 减少不必要的索引
- 考虑异步写入

---

### 9.3 权限问题

#### 问题 5：权限被拒绝

**症状**：
- 返回 403 Forbidden
- 日志显示 "Permission denied"

**排查步骤**：

1. 检查 API Token 权限
   ```bash
   # 验证 Token 是否有效
   curl -H "Authorization: Bearer YOUR_TOKEN" https://api.cloudflare.com/client/v4/user/tokens/verify
   ```

2. 检查 Worker 绑定配置
   ```toml
   # 确保绑定名称正确
   [[d1_databases]]
   binding = "DB"
   database_name = "my-first-database"
   database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   ```

3. 检查环境变量
   ```javascript
   // 确保环境变量正确设置
   console.log(env.API_TOKEN);
   ```

**解决方案**：
- 重新生成 API Token
- 更新 Worker 配置
- 检查账户权限设置

---

### 9.4 数据一致性问题

#### 问题 6：数据不同步

**症状**：
- 查询结果与预期不符
- 数据更新后没有立即生效

**排查步骤**：

1. 检查事务是否提交
   ```javascript
   // 确保事务已提交
   BEGIN TRANSACTION;
   // ... 操作
   COMMIT;
   ```

2. 检查并发访问
   ```javascript
   // 使用锁机制避免并发问题
   // SQLite 使用内置锁，但需要注意事务隔离级别
   ```

3. 检查缓存
   ```javascript
   // 清除缓存
   await env.CACHE.delete('users_list');
   ```

**解决方案**：
- 确保事务正确提交
- 使用适当的隔离级别
- 清除或更新缓存

---

### 9.5 错误代码说明

| 错误代码 | 说明 | 解决方案 |
|---------|------|---------|
| `400` | 请求格式错误 | 检查 SQL 语法 |
| `401` | 未授权 | 检查 API Token |
| `403` | 权限不足 | 检查 Token 权限 |
| `404` | 数据库不存在 | 检查 database_id |
| `500` | 服务器错误 | 检查日志 |
| `504` | 超时 | 优化查询或增加超时时间 |

---

### 9.6 调试技巧

#### 启用详细日志

```javascript
// worker.js
export default {
  async fetch(request, env, ctx) {
    console.log('Request received:', request.url);
    console.log('Method:', request.method);
    
    try {
      const startTime = Date.now();
      const { results } = await env.DB.prepare('SELECT * FROM users').all();
      const duration = Date.now() - startTime;
      
      console.log(`Query executed in ${duration}ms`);
      console.log(`Results: ${results.length} rows`);
      
      return Response.json(results);
    } catch (error) {
      console.error('Error:', error);
      return Response.json({ error: error.message }, { status: 500 });
    }
  }
};
```

#### 使用 Wrangler 实时日志

```bash
# 查看实时日志
wrangler tail

# 查看特定 Worker 的日志
wrangler tail --name my-worker

# 过滤日志
wrangler tail --format pretty
```

#### 本地开发环境

```bash
# 使用本地 D1 数据库进行开发
wrangler d1 execute my-first-database --local --command="SELECT * FROM users"

# 启动本地开发服务器
wrangler dev --local
```

---

## 10. 附录

### 10.1 有用的资源链接

- [Cloudflare D1 官方文档](https://developers.cloudflare.com/d1/)
- [Wrangler CLI 文档](https://developers.cloudflare.com/workers/wrangler/)
- [SQLite 官方文档](https://www.sqlite.org/docs.html)
- [Cloudflare Workers 文档](https://developers.cloudflare.com/workers/)

### 10.2 社区支持

- [Cloudflare Community Forum](https://community.cloudflare.com/)
- [Cloudflare Discord](https://discord.gg/cloudflaredev)
- [Stack Overflow - Cloudflare 标签](https://stackoverflow.com/questions/tagged/cloudflare)

### 10.3 常用 SQL 速查表

```sql
-- 创建表
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);

-- 插入数据
INSERT INTO users (name) VALUES ('Alice');

-- 查询数据
SELECT * FROM users;

-- 更新数据
UPDATE users SET name = 'Bob' WHERE id = 1;

-- 删除数据
DELETE FROM users WHERE id = 1;

-- 创建索引
CREATE INDEX idx_users_name ON users(name);

-- 查看表结构
PRAGMA table_info(users);

-- 查看索引
PRAGMA index_list('users');

-- 删除表
DROP TABLE users;
```

---

## 总结

恭喜你完成了 Cloudflare D1 数据库的完整学习！本教程涵盖了：

✅ Cloudflare 账户注册与登录  
✅ D1 数据库基本概念  
✅ 创建 D1 数据库（Dashboard 和 Wrangler 两种方式）  
✅ 数据库初始化配置  
✅ 基本 SQL 操作示例  
✅ 权限管理设置  
✅ 与 Cloudflare Workers 集成  
✅ 数据备份与恢复策略  
✅ 常见问题排查指南  

现在你已经具备了使用 Cloudflare D1 数据库的基础知识，可以开始构建自己的应用了！

**下一步建议**：
1. 尝试创建一个简单的 CRUD 应用
2. 学习更多高级 SQL 操作
3. 探索 Cloudflare Workers 的其他功能
4. 加入 Cloudflare 社区，与其他开发者交流

祝你学习愉快！🎉
