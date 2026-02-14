#!/usr/bin/env python3
"""
数据库初始化脚本
用于初始化 Cloudflare D1 数据库表结构
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 60)
    print("Cloudflare D1 数据库初始化脚本")
    print("=" * 60)
    print()
    
    # 检查环境变量
    required_vars = ['CLOUDFLARE_ACCOUNT_ID', 'CLOUDFLARE_API_TOKEN', 'CLOUDFLARE_D1_DATABASE_ID']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ 错误：缺少必要的环境变量：")
        for var in missing_vars:
            print(f"   - {var}")
        print()
        print("请在 .env 文件中配置这些变量，然后重试。")
        sys.exit(1)
    
    print("✅ 环境变量检查通过")
    print()
    
    # 显示配置信息
    print("当前配置：")
    print(f"  Account ID: {os.getenv('CLOUDFLARE_ACCOUNT_ID')}")
    print(f"  Database ID: {os.getenv('CLOUDFLARE_D1_DATABASE_ID')}")
    print()
    
    # 检查 schema.sql 文件是否存在
    schema_file = 'database/schema.sql'
    if not os.path.exists(schema_file):
        print(f"❌ 错误：找不到 schema.sql 文件：{schema_file}")
        sys.exit(1)
    
    print(f"✅ 找到 schema.sql 文件")
    print()
    
    # 提示用户使用 Wrangler 初始化数据库
    print("=" * 60)
    print("初始化步骤：")
    print("=" * 60)
    print()
    print("1. 安装 Wrangler CLI（如果尚未安装）：")
    print("   npm install -g wrangler")
    print()
    print("2. 登录 Cloudflare：")
    print("   wrangler login")
    print()
    print("3. 执行数据库初始化脚本：")
    print(f"   wrangler d1 execute cc-test-database --file={schema_file}")
    print()
    print("4. 验证表是否创建成功：")
    print("   wrangler d1 execute cc-test-database --command=\"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;\"")
    print()
    print("=" * 60)
    print()
    
    # 测试数据库连接
    print("测试数据库连接...")
    try:
        from cloudflare_db import CloudflareDBManager
        db_manager = CloudflareDBManager()
        print("✅ 数据库连接成功")
        print()
        
        # 检查表是否存在
        print("检查数据库表...")
        result = db_manager.execute_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        
        if result and len(result) > 0:
            tables = result[0].get('results', [])
            if tables:
                print(f"✅ 当前数据库中有 {len(tables)} 个表：")
                for table in tables:
                    print(f"   - {table['name']}")
            else:
                print("⚠️  数据库中还没有表，请执行上述初始化步骤")
        else:
            print("⚠️  无法查询表信息，请检查配置")
        
    except Exception as e:
        print(f"❌ 数据库连接失败：{e}")
        print()
        print("请确保：")
        print("1. .env 文件中的配置正确")
        print("2. Cloudflare API Token 有足够的权限")
        print("3. 数据库 ID 正确")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("初始化脚本执行完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
