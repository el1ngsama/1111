#!/usr/bin/env python3
"""
数据库初始化脚本
用于初始化 Cloudflare D1 数据库
"""

import os
import sys
from dotenv import load_dotenv
from cloudflare_db import CloudflareDBManager

load_dotenv()

def init_database():
    """
    初始化数据库表结构
    """
    print("开始初始化 Cloudflare D1 数据库...")
    
    try:
        # 初始化数据库管理器
        db_manager = CloudflareDBManager()
        print("✓ 数据库连接成功")
        
        # 读取 SQL 文件
        sql_file = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
        
        if not os.path.exists(sql_file):
            print(f"✗ SQL 文件不存在: {sql_file}")
            return False
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 分割 SQL 语句
        sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        print(f"找到 {len(sql_statements)} 条 SQL 语句")
        
        # 执行每条 SQL 语句
        success_count = 0
        for i, sql in enumerate(sql_statements, 1):
            result = db_manager.execute_sql(sql)
            if result is not None:
                success_count += 1
                print(f"✓ 执行成功 [{i}/{len(sql_statements)}]: {sql[:50]}...")
            else:
                print(f"✗ 执行失败 [{i}/{len(sql_statements)}]: {sql[:50]}...")
        
        print(f"\n初始化完成！成功执行 {success_count}/{len(sql_statements)} 条语句")
        
        # 验证表是否创建成功
        print("\n验证数据库表...")
        tables_sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        result = db_manager.execute_sql(tables_sql)
        
        if result and len(result) > 0:
            tables = result[0].get('results', [])
            print(f"✓ 数据库包含以下表:")
            for table in tables:
                print(f"  - {table['name']}")
        else:
            print("✗ 无法获取表列表")
        
        return True
        
    except Exception as e:
        print(f"✗ 初始化失败: {e}")
        return False

def test_database():
    """
    测试数据库连接和基本操作
    """
    print("\n测试数据库连接...")
    
    try:
        db_manager = CloudflareDBManager()
        
        # 测试查询
        news_list = db_manager.get_all_news(limit=5)
        print(f"✓ 查询成功，当前有 {len(news_list)} 条新闻")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Cloudflare D1 数据库初始化工具")
    print("=" * 60)
    print()
    
    # 检查环境变量
    required_vars = ['CLOUDFLARE_ACCOUNT_ID', 'CLOUDFLARE_API_TOKEN', 'CLOUDFLARE_D1_DATABASE_ID']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("✗ 缺少必要的环境变量:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\n请在 .env 文件中配置这些变量")
        sys.exit(1)
    
    # 初始化数据库
    if init_database():
        # 测试数据库
        test_database()
        print("\n" + "=" * 60)
        print("数据库初始化完成！")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("数据库初始化失败！")
        print("=" * 60)
        sys.exit(1)
