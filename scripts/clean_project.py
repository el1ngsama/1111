#!/usr/bin/env python3
"""
项目清理脚本
用于删除冗余文件，准备项目部署到 Vercel
"""

import os
import shutil
import sys
from pathlib import Path

def print_header(text):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_section(text):
    """打印章节"""
    print(f"\n{text}")
    print("-" * 60)

def print_info(text):
    """打印信息"""
    print(f"  ℹ️  {text}")

def print_success(text):
    """打印成功信息"""
    print(f"  ✅ {text}")

def print_warning(text):
    """打印警告信息"""
    print(f"  ⚠️  {text}")

def print_error(text):
    """打印错误信息"""
    print(f"  ❌ {text}")

def confirm_delete(files):
    """确认删除文件"""
    print_warning(f"准备删除 {len(files)} 个文件/目录：")
    for file in files:
        print(f"    - {file}")
    
    response = input("\n  确认删除这些文件？(y/n): ").strip().lower()
    return response in ['y', 'yes']

def delete_files(file_paths):
    """删除文件或目录"""
    deleted = []
    errors = []
    
    for path in file_paths:
        try:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                    deleted.append(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    deleted.append(path)
                else:
                    print_warning(f"路径不存在: {path}")
            else:
                print_warning(f"路径不存在: {path}")
        except Exception as e:
            errors.append((path, str(e)))
    
    return deleted, errors

def main():
    print_header("项目清理脚本")
    print_info("此脚本将删除冗余文件，准备项目部署到 Vercel")
    
    project_root = Path(__file__).parent
    
    # 定义要删除的文件和目录
    files_to_delete = [
        # 敏感信息文件
        ".env",
        
        # 不需要的文件
        ".git.zip",
        "init_database.py",  # 与 scripts/init_db.py 重复
        
        # 测试文件
        "backend/test_deepseek.py",
        
        # Python 缓存目录
        "backend/__pycache__",
        
        # 其他临时文件
        ".cache",
        ".temp",
        "tmp",
    ]
    
    # 转换为绝对路径
    files_to_delete = [str(project_root / f) for f in files_to_delete]
    
    # 检查哪些文件实际存在
    existing_files = [f for f in files_to_delete if os.path.exists(f)]
    
    if not existing_files:
        print_info("没有找到需要删除的文件")
        return
    
    print_section("找到以下文件可以删除：")
    for f in existing_files:
        file_type = "目录" if os.path.isdir(f) else "文件"
        print(f"  [{file_type}] {os.path.basename(f)}")
    
    # 确认删除
    if not confirm_delete(existing_files):
        print_info("取消删除操作")
        return
    
    # 执行删除
    print_section("开始删除...")
    deleted, errors = delete_files(existing_files)
    
    # 显示结果
    print_section("删除结果：")
    print_success(f"成功删除 {len(deleted)} 个文件/目录")
    
    if errors:
        print_section("删除错误：")
        for path, error in errors:
            print_error(f"  {os.path.basename(path)}: {error}")
    
    # 检查项目核心文件
    print_section("验证项目核心文件：")
    core_files = [
        "src/App.jsx",
        "src/main.jsx",
        "src/index.css",
        "index.html",
        "backend/app.py",
        "backend/cloudflare_db.py",
        "backend/crawler.py",
        "backend/deepseek_client.py",
        "api/index.py",
        "api/requirements.txt",
        "database/schema.sql",
        "package.json",
        "vite.config.js",
        "tailwind.config.js",
        "postcss.config.js",
        "wrangler.toml",
        "vercel.json",
        ".env.example",
        ".gitignore",
        "DEPLOYMENT.md",
        "MANUAL_DEPLOYMENT_GUIDE.md",
        "CLOUDFLARE_D1_TUTORIAL.md",
        "GITHUB_UPLOAD_GUIDE.md",
    ]
    
    all_core_exist = True
    for f in core_files:
        if not os.path.exists(project_root / f):
            print_warning(f"核心文件缺失: {f}")
            all_core_exist = False
    
    if all_core_exist:
        print_success("所有核心文件都存在")
    else:
        print_error("部分核心文件缺失，请检查项目结构")
    
    # 检查是否还有其他冗余文件
    print_section("检查其他冗余文件...")
    redundant_patterns = [
        "*.log",
        "*.pyc",
        "*.pyo",
        "*.bak",
        "*.backup",
        "*.tmp",
        "Thumbs.db",
        ".DS_Store",
    ]
    
    found_redundant = []
    for pattern in redundant_patterns:
        matches = list(project_root.glob(pattern))
        if matches:
            found_redundant.extend(matches)
    
    if found_redundant:
        print_warning(f"找到 {len(found_redundant)} 个冗余文件")
        for f in found_redundant[:10]:
            print(f"    - {f}")
        if len(found_redundant) > 10:
            print(f"    ... 还有 {len(found_redundant) - 10} 个文件")
    else:
        print_success("没有找到其他冗余文件")
    
    # 最终总结
    print_header("清理完成")
    print_info("项目已准备好部署到 Vercel")
    print_section("下一步：")
    print("  1. 初始化 Cloudflare D1 数据库")
    print("     wrangler d1 execute cc-test-database --file=database/schema.sql")
    print()
    print("  2. 上传到 GitHub")
    print("     按照 GITHUB_UPLOAD_GUIDE.md 中的步骤操作")
    print()
    print("  3. 部署到 Vercel")
    print("     vercel --prod")
    print()
    print("  4. 配置 Vercel 环境变量")
    print("     在 Vercel Dashboard 中添加环境变量")
    print()
    print_info("详细说明请查看：")
    print("  - MANUAL_DEPLOYMENT_GUIDE.md")
    print("  - DEPLOYMENT.md")
    print("  - CLOUDFLARE_D1_TUTORIAL.md")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_info("\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print_error(f"发生错误: {e}")
        sys.exit(1)
