#!/usr/bin/env python
"""
启动脚本：初始化数据库并启动Flask服务器
"""
import os
import sys
import subprocess
import time

def print_header(message):
    print("\n" + "=" * 50)
    print(message.center(50))
    print("=" * 50 + "\n")

def check_requirements():
    print_header("检查依赖项")
    try:
        subprocess.run(
            ["pip", "install", "-r", "requirements.txt"], 
            check=True,
            capture_output=True
        )
        print("✅ 依赖项安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖项安装失败: {e}")
        print(f"错误输出: {e.stderr.decode('utf-8')}")
        return False

def init_database():
    print_header("初始化数据库")
    try:
        subprocess.run(["python", "init_db.py"], check=True)
        print("✅ 数据库初始化成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

def start_flask_server():
    print_header("启动Flask服务器")
    
    # 检查环境变量中是否有端口配置
    port = os.environ.get("SERVER_PORT", 5000)
    host = os.environ.get("SERVER_HOST", "0.0.0.0")
    debug = os.environ.get("DEBUG", "True").lower() == "true"
    
    print(f"服务器配置: host={host}, port={port}, debug={debug}")
    
    try:
        # 使用 app.py 启动应用程序
        from app import app
        print(f"✅ 服务器启动成功 - 监听在 http://{host}:{port}")
        app.run(host=host, port=int(port), debug=debug)
        return True
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        return False

def main():
    print_header("健康运动API服务器启动")
    
    if not check_requirements():
        sys.exit(1)
    
    if not init_database():
        print("\n⚠️  数据库初始化失败，但尝试继续启动服务器...")
    
    # 短暂延迟，确保数据库连接已就绪
    time.sleep(1)
    
    if not start_flask_server():
        sys.exit(1)

if __name__ == "__main__":
    main()
