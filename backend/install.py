#!/usr/bin/env python
"""
安装脚本：设置必要的环境和数据库
"""
import os
import sys
import subprocess
import getpass
from pathlib import Path

def print_header(message):
    print("\n" + "=" * 50)
    print(message.center(50))
    print("=" * 50 + "\n")

def check_python_version():
    """检查Python版本是否满足要求"""
    print("检查Python版本...")
    version_info = sys.version_info
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 7):
        print("❌ 需要Python 3.7或更高版本")
        return False
    print(f"✓ Python版本: {sys.version.split()[0]}")
    return True

def install_requirements():
    """安装项目依赖包"""
    print("\n安装项目依赖...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("✓ 依赖安装完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")
        return False

def setup_env_file():
    """设置环境变量文件"""
    print("\n配置环境变量...")
    env_file = Path(".env")
    
    if env_file.exists():
        print("发现已有的.env文件，是否要覆盖? (y/N): ", end="")
        choice = input().strip().lower()
        if choice != 'y':
            print("✓ 保留现有.env文件")
            return True
    
    try:
        # 提示用户输入数据库信息
        db_host = input("数据库主机 (默认: localhost): ").strip() or "localhost"
        db_user = input("数据库用户名 (默认: root): ").strip() or "root"
        db_password = getpass.getpass("数据库密码 (默认: 空): ") or ""
        db_name = input("数据库名称 (默认: workout_app): ").strip() or "workout_app"
        
        # 创建.env文件
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(f"# 数据库配置\n")
            f.write(f"DB_HOST={db_host}\n")
            f.write(f"DB_USER={db_user}\n")
            f.write(f"DB_PASSWORD={db_password}\n")
            f.write(f"DB_NAME={db_name}\n\n")
            
            f.write(f"# Flask配置\n")
            f.write(f"FLASK_APP=app.py\n")
            f.write(f"FLASK_ENV=development\n")
            f.write(f"SECRET_KEY=workout_app_secret_key_{os.urandom(4).hex()}\n\n")
            
            f.write(f"# 服务器配置\n")
            f.write(f"SERVER_HOST=0.0.0.0\n")
            f.write(f"SERVER_PORT=5000\n")
            f.write(f"DEBUG=True\n")
        
        print("✓ .env文件创建成功")
        return True
    except Exception as e:
        print(f"❌ .env文件创建失败: {e}")
        return False

def create_database():
    """创建MySQL数据库"""
    print("\n创建数据库...")
    
    # 从.env文件加载配置
    if not Path(".env").exists():
        print("❌ 找不到.env文件，无法创建数据库")
        return False
    
    try:
        # 尝试加载dotenv模块
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("❌ 无法加载dotenv模块，请先安装依赖")
        return False
    
    # 获取数据库配置
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "workout_app")
    
    try:
        import mysql.connector
        
        # 连接到MySQL服务器
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        
        cursor = conn.cursor()
        
        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        print(f"✓ 数据库 '{db_name}' 创建成功或已存在")
        
        # 关闭连接
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库创建失败: {e}")
        return False

def main():
    print_header("健康运动API服务器 - 安装程序")
    
    success = True
    
    # 检查Python版本
    if not check_python_version():
        success = False
    
    # 安装依赖
    if success and not install_requirements():
        success = False
    
    # 设置.env文件
    if success and not setup_env_file():
        success = False
    
    # 创建数据库
    if success and not create_database():
        print("⚠️  数据库创建失败，但可能是因为权限问题或数据库已存在")
        print("   您可以手动创建数据库，然后运行init_db.py脚本初始化表结构")
    
    # 安装结果
    if success:
        print_header("安装成功!")
        print("接下来你可以运行:")
        print("1. python init_db.py  # 初始化数据库表结构和基础数据")
        print("2. python run.py      # 启动Flask服务器")
    else:
        print_header("安装过程中遇到错误")
        print("请解决上述问题后重新运行安装程序")
        sys.exit(1)

if __name__ == "__main__":
    main()
