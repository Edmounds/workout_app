import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取数据库配置
# 处理主机地址和端口号
db_host = os.getenv('DB_HOST', 'localhost')
if ':' in db_host:  # 如果主机地址包含端口号
    host_parts = db_host.split(':')
    host = host_parts[0]
    port = int(host_parts[1])
else:
    host = db_host
    port = 3306  # 默认MySQL端口

db_config = {
    'pool_name': "workout_pool",
    'pool_size': 5,
    'host': host,
    'port': port,
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'workout_app')
}

# 创建连接池
try:
    db_pool = pooling.MySQLConnectionPool(**db_config)
    print("数据库连接池初始化成功")
except Exception as e:
    print(f"数据库连接池初始化失败: {e}")
    db_pool = None

def get_db_connection():
    """获取数据库连接"""
    try:
        if db_pool:
            conn = db_pool.get_connection()
            return conn
        else:
            # 如果连接池创建失败，尝试直接创建连接
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'workout_app')
            )
            return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        raise
