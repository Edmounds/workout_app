"""
数据库初始化脚本
用于初始化数据库，创建必要的表和基础数据
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import json

# 加载环境变量
load_dotenv()

# 处理主机地址和端口号
db_host = os.getenv('DB_HOST', 'localhost')
if ':' in db_host:  # 如果主机地址包含端口号
    host_parts = db_host.split(':')
    host = host_parts[0]
    port = int(host_parts[1])
else:
    host = db_host
    port = 3306  # 默认MySQL端口

DB_CONFIG = {
    'host': host,
    'port': port,
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'workout_app')
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"数据库连接错误: {e}")
        return None

def create_tables(cursor):
    """创建必要的数据库表"""
    
    # 用户表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        openid VARCHAR(50) UNIQUE,
        username VARCHAR(50),
        gender TINYINT COMMENT '0:未知, 1:男, 2:女',
        age INT,
        height DECIMAL(5,2) COMMENT '身高(cm)',
        weight DECIMAL(5,2) COMMENT '体重(kg)',
        level VARCHAR(20) COMMENT '跑步水平:beginner/intermediate/advanced',
        total_workouts INT DEFAULT 0,
        total_duration INT DEFAULT 0 COMMENT '总运动时长(分钟)',
        total_distance DECIMAL(10,2) DEFAULT 0.00 COMMENT '总运动距离(km)',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)
    
    # 运动记录表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS running_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        workout_type VARCHAR(50) COMMENT '训练类型（跑步/力量/...）',
        start_time DATETIME,
        end_time DATETIME,
        duration INT COMMENT '持续时间(秒)',
        distance DECIMAL(6,2) COMMENT '距离(米)',
        avg_pace INT COMMENT '平均配速(秒/公里)',
        best_pace INT COMMENT '最佳配速(秒/公里)',
        avg_heart_rate INT COMMENT '平均心率',
        max_heart_rate INT COMMENT '最大心率',
        avg_step_rate INT COMMENT '平均步频',
        calories INT COMMENT '消耗卡路里',
        elevation_gain DECIMAL(6,2) COMMENT '累计爬升(米)',
        weather VARCHAR(50) COMMENT '天气情况',
        temperature DECIMAL(4,1) COMMENT '温度',
        notes TEXT COMMENT '备注内容',
        KEY user_id_idx (user_id, start_time),
        CONSTRAINT running_records_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)
    
    # 进度目标表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress_goals (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        title VARCHAR(100) COMMENT '目标标题',
        current_value DECIMAL(8,2) COMMENT '当前值',
        target_value DECIMAL(8,2) COMMENT '目标值',
        category VARCHAR(30) COMMENT '目标类别',
        deadline DATE COMMENT '截止日期',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        completed BOOLEAN DEFAULT FALSE,
        KEY user_id_idx (user_id),
        CONSTRAINT progress_goals_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)
    
    # 营养提示表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nutrition_tips (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tip TEXT COMMENT '提示内容',
        category VARCHAR(50) COMMENT '类别（赛前/赛后/日常等）',
        importance INT COMMENT '重要性排序'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)
    
    # AI建议表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_advice (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        advice_content TEXT COMMENT '建议内容',
        category VARCHAR(50) COMMENT '类别（训练/恢复/营养等）',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        KEY user_id_idx (user_id),
        CONSTRAINT ai_advice_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)
    
    # 用户反馈表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_feedback (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        feedback_type VARCHAR(20) NOT NULL,
        feedback_content TEXT NOT NULL,
        contact VARCHAR(100),
        submit_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        admin_remark VARCHAR(255) DEFAULT ''
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)
    
    # 时间胶囊表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS time_capsule (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        target_months INT,
        metrics JSON,
        reminder_freq VARCHAR(20),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        target_date DATETIME,
        opened BOOLEAN DEFAULT FALSE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)
    
    # 身体数据表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS physical_stats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        date DATE,
        avg_heart_rate INT,
        current_heart_rate INT,
        resting_heart_rate INT,
        max_heart_rate INT,
        current_step_rate INT,
        avg_step_rate INT,
        avg_blood_oxygen DECIMAL(4,1),
        current_pace VARCHAR(10),
        health_index INT COMMENT '健康指数(0-100)',
        stress_index INT COMMENT '压力指数(0-100)',
        sleep_quality INT COMMENT '睡眠质量分数(0-100)',
        sleep_duration INT COMMENT '睡眠时长(分钟)',
        aerobic_capacity INT COMMENT '有氧能力评估(0-100)',
        weekly_distance DECIMAL(5,2) COMMENT '本周跑量(km)',
        total_distance INT NOT NULL,
        KEY user_date_idx (user_id, date),
        CONSTRAINT physical_stats_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """)

def insert_sample_data(cursor):
    """插入示例数据"""
    
    # 检查用户表是否为空
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        # 添加一个测试用户
        hashed_password = generate_password_hash("test123")
        cursor.execute("""
        INSERT INTO users (username, password, email, gender, age, height, weight, level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, ("test_user", hashed_password, "test@example.com", 1, 30, 175.5, 70.2, "intermediate"))
        
        print("已添加测试用户: test_user / test123")
    
    # 检查营养提示表是否为空
    cursor.execute("SELECT COUNT(*) FROM nutrition_tips")
    tips_count = cursor.fetchone()[0]
    
    if tips_count == 0:
        # 添加一些营养提示
        tips = [
            ("跑步前2小时摄入含复合碳水化合物的食物，如全麦面包或燕麦", "赛前", 5),
            ("训练后30分钟内补充蛋白质，促进肌肉恢复", "赛后", 5),
            ("每天保持充足的水分摄入，成人每天至少需要2升水", "日常", 4),
            ("长距离跑步时每小时补充30-60克碳水化合物", "训练中", 4),
            ("摄入富含抗氧化剂的食物如浆果和绿叶蔬菜，可以减轻运动引起的炎症", "日常", 3)
        ]
        
        cursor.executemany("""
        INSERT INTO nutrition_tips (tip, category, importance)
        VALUES (%s, %s, %s)
        """, tips)
        
        print(f"已添加{len(tips)}条营养提示")

def main():
    conn = get_db_connection()
    if not conn:
        print("无法连接到数据库，请检查配置")
        return
    
    try:
        cursor = conn.cursor()
        
        # 创建表结构
        create_tables(cursor)
        print("数据库表结构已创建")
        
        # 插入示例数据
        insert_sample_data(cursor)
        
        conn.commit()
        print("数据库初始化完成")
        
    except Error as e:
        print(f"数据库操作错误: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    main()
