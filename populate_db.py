# 重要: 运行此脚本前，请确保已安装 mysql-connector-python 包。
# 您可以使用命令: pip install mysql-connector-python
import mysql.connector
from faker import Faker
import random
import json
from datetime import datetime, timedelta

# --- 配置 ---
DB_CONFIG = {
    'host': '113.45.220.0',
    'port': 3306,
    'user': 'cxr',
    'password': 'Chenqichen666',
    'database': 'workout_app'
}

NUM_USERS = 20  # 要创建的用户数量
RECORDS_PER_USER = 5  # 每个用户相关的记录数量 (例如跑步记录、目标等)
NUM_NUTRITION_TIPS = 30
NUM_USER_FEEDBACKS = 15

fake = Faker('zh_CN') # 使用中文数据生成器

# --- 辅助函数 ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"数据库连接错误: {err}")
        return None

# --- 数据生成函数 ---

def create_users(cursor, num_users):
    users_data = []
    inserted_user_ids = []
    for _ in range(num_users):
        #确保 openid 和 email 的唯一性
        while True:
            openid = fake.uuid4()
            email = fake.unique.email()
            query_check = "SELECT id FROM users WHERE openid = %s OR email = %s"
            cursor.execute(query_check, (openid, email))
            if cursor.fetchone() is None:
                fake.unique.clear() # 清除已生成的 email, 以便下次可以重新生成
                break
            fake.unique.clear()


        user = (
            openid,
            fake.user_name(),
            random.choice([0, 1, 2]),  # gender
            random.randint(18, 60),  # age
            round(random.uniform(150.0, 200.0), 2),  # height
            round(random.uniform(50.0, 100.0), 2),  # weight
            random.choice(['beginner', 'intermediate', 'advanced']),  # level
            0, # total_workouts
            0, # total_duration
            0.00, # total_distance
            fake.password(length=12), # password
            email
        )
        users_data.append(user)

    query = """
    INSERT INTO users (openid, username, gender, age, height, weight, level, 
                       total_workouts, total_duration, total_distance, password, email)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        for user_data_single in users_data: # executemany 可能因 unique constraint 失败，逐条插入并获取id
            cursor.execute(query, user_data_single)
            inserted_user_ids.append(cursor.lastrowid)
        print(f"成功插入 {len(inserted_user_ids)} 条用户数据。")
        return inserted_user_ids
    except mysql.connector.Error as err:
        print(f"插入用户数据时出错: {err}")
        return []


def create_ai_advice(cursor, user_ids, records_per_user):
    advice_data = []
    for user_id in user_ids:
        for _ in range(random.randint(1, records_per_user)):
            advice = (
                user_id,
                fake.paragraph(nb_sentences=3),
                random.choice(['训练', '恢复', '营养', '心态', '装备'])
            )
            advice_data.append(advice)
    query = "INSERT INTO ai_advice (user_id, advice_content, category) VALUES (%s, %s, %s)"
    try:
        cursor.executemany(query, advice_data)
        print(f"成功插入 {len(advice_data)} 条 AI 建议数据。")
    except mysql.connector.Error as err:
        print(f"插入 AI 建议数据时出错: {err}")

def create_nutrition_tips(cursor, num_tips):
    tips_data = []
    for _ in range(num_tips):
        tip = (
            fake.sentence(nb_words=10),
            random.choice(['赛前', '赛后', '日常', '补水', '恢复']),
            random.randint(1, 5) # importance
        )
        tips_data.append(tip)
    query = "INSERT INTO nutrition_tips (tip, category, importance) VALUES (%s, %s, %s)"
    try:
        cursor.executemany(query, tips_data)
        print(f"成功插入 {len(tips_data)} 条营养提示数据。")
    except mysql.connector.Error as err:
        print(f"插入营养提示数据时出错: {err}")

def create_physical_stats(cursor, user_ids, records_per_user):
    stats_data = []
    for user_id in user_ids:
        for _ in range(random.randint(1, records_per_user)):
            stat = (
                user_id,
                fake.date_between(start_date='-2y', end_date='today'),
                random.randint(70, 150),  # avg_heart_rate
                random.randint(60, 180),  # current_heart_rate
                random.randint(45, 80),   # resting_heart_rate
                random.randint(160, 200), # max_heart_rate
                random.randint(120, 180), # current_step_rate
                random.randint(130, 170), # avg_step_rate
                round(random.uniform(95.0, 99.9), 1), # avg_blood_oxygen
                f"{random.randint(4,8)}'{random.randint(0,59):02d}\"", # current_pace
                random.randint(50, 95),   # health_index
                random.randint(10, 80),   # stress_index
                random.randint(60, 90),   # sleep_quality
                random.randint(300, 540), # sleep_duration (minutes)
                random.randint(30, 70),   # aerobic_capacity
                round(random.uniform(5.0, 70.0), 2), # weekly_distance (km)
                random.randint(100, 5000) # total_distance (km, int as per schema)
            )
            stats_data.append(stat)
    query = """
    INSERT INTO physical_stats (user_id, date, avg_heart_rate, current_heart_rate, resting_heart_rate,
                                max_heart_rate, current_step_rate, avg_step_rate, avg_blood_oxygen,
                                current_pace, health_index, stress_index, sleep_quality, sleep_duration,
                                aerobic_capacity, weekly_distance, total_distance)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(query, stats_data)
        print(f"成功插入 {len(stats_data)} 条身体状态数据。")
    except mysql.connector.Error as err:
        print(f"插入身体状态数据时出错: {err}")

def create_progress_goals(cursor, user_ids, records_per_user):
    goals_data = []
    for user_id in user_ids:
        for _ in range(random.randint(1, records_per_user)):
            current_val = round(random.uniform(1.0, 500.0), 2)
            target_val = round(current_val + random.uniform(10.0, 500.0), 2)
            goal = (
                user_id,
                fake.sentence(nb_words=5), # title
                current_val,
                target_val,
                random.choice(['距离', '配速', '时长', '体重', '跑量']), # category
                fake.date_between(start_date='today', end_date='+1y') # deadline
            )
            goals_data.append(goal)
    query = """
    INSERT INTO progress_goals (user_id, title, current_value, target_value, category, deadline)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(query, goals_data)
        print(f"成功插入 {len(goals_data)} 条进度目标数据。")
    except mysql.connector.Error as err:
        print(f"插入进度目标数据时出错: {err}")

def create_running_records(cursor, user_ids, records_per_user):
    records_data = []
    for user_id in user_ids:
        for _ in range(random.randint(1, records_per_user)):
            start_time = fake.date_time_between(start_date='-2y', end_date='now', tzinfo=None)
            duration_seconds = random.randint(600, 7200) # 10 min to 2 hours
            end_time = start_time + timedelta(seconds=duration_seconds)
            
            # 修改 distance_meters 的生成范围以符合 DECIMAL(6,2) 的约束 (最大 9999.99)
            # 原来: random.uniform(1000.0, 21097.5) 可能超出 DECIMAL(6,2)
            distance_meters = round(random.uniform(1000.0, 9999.99), 2) # 1km to ~10km

            avg_pace_seconds_km = 0
            if distance_meters > 0:
                avg_pace_seconds_km = int(duration_seconds / (distance_meters / 1000.0))
            
            best_pace_seconds_km = 0
            if avg_pace_seconds_km > 0 :
                 best_pace_seconds_km = max(60, avg_pace_seconds_km - random.randint(5, 60))


            record = (
                user_id,
                random.choice(['跑步', '越野跑', '操场跑', '间歇跑', '恢复跑']), # workout_type
                start_time,
                end_time,
                duration_seconds,
                distance_meters, # distance (meters)
                avg_pace_seconds_km if distance_meters > 0 else 0, # avg_pace (s/km)
                best_pace_seconds_km if distance_meters > 0 else 0, # best_pace (s/km)
                random.randint(100, 170), # avg_heart_rate
                random.randint(150, 190), # max_heart_rate
                random.randint(150, 180), # avg_step_rate
                int(distance_meters / 1000 * 60), # calories (approx)
                round(random.uniform(0.0, 300.0), 2), # elevation_gain
                random.choice(['晴朗', '多云', '小雨', '阴天', '有风']), # weather
                round(random.uniform(-5.0, 35.0), 1), # temperature
                fake.sentence(nb_words=8) # notes
            )
            records_data.append(record)
    query = """
    INSERT INTO running_records (user_id, workout_type, start_time, end_time, duration, distance,
                                 avg_pace, best_pace, avg_heart_rate, max_heart_rate, avg_step_rate,
                                 calories, elevation_gain, weather, temperature, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(query, records_data)
        print(f"成功插入 {len(records_data)} 条跑步记录数据。")
    except mysql.connector.Error as err:
        print(f"插入跑步记录数据时出错: {err}")

def create_time_capsules(cursor, user_ids, records_per_user):
    capsules_data = []
    for user_id in user_ids:
        for _ in range(random.randint(0, records_per_user // 2)): # Not every user might have one
            metrics = {
                "goal_distance_km": random.randint(5, 42),
                "goal_pace_min_km": f"{random.randint(4,7)}:{random.randint(0,59):02d}",
                "target_weight_kg": round(random.uniform(50.0, 80.0), 1)
            }
            capsule = (
                user_id,
                random.choice([1, 3, 6, 12]), # target_months
                json.dumps(metrics), # metrics (JSON string)
                random.choice(['weekly', 'monthly', 'quarterly']) # reminder_freq
            )
            capsules_data.append(capsule)
    if not capsules_data:
        print("没有时间胶囊数据生成。")
        return

    query = """
    INSERT INTO time_capsule (user_id, target_months, metrics, reminder_freq)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.executemany(query, capsules_data)
        print(f"成功插入 {len(capsules_data)} 条时间胶囊数据。")
    except mysql.connector.Error as err:
        print(f"插入时间胶囊数据时出错: {err}")

def create_user_feedback(cursor, num_feedbacks):
    feedbacks_data = []
    for _ in range(num_feedbacks):
        feedback = (
            random.choice(['bug反馈', '功能建议', '体验赞扬', '其他问题']), # feedback_type
            fake.paragraph(nb_sentences=4), # feedback_content
            fake.email() if random.choice([True, False]) else fake.phone_number(), # contact
            '' # admin_remark
        )
        feedbacks_data.append(feedback)
    query = """
    INSERT INTO user_feedback (feedback_type, feedback_content, contact, admin_remark)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.executemany(query, feedbacks_data)
        print(f"成功插入 {len(feedbacks_data)} 条用户反馈数据。")
    except mysql.connector.Error as err:
        print(f"插入用户反馈数据时出错: {err}")


# --- 主执行逻辑 ---
def main():
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()

    try:
        print("开始填充数据库...")

        # 1. 创建用户并获取 ID
        user_ids = create_users(cursor, NUM_USERS)
        if not user_ids:
            print("未能创建用户，终止填充。")
            return

        # 2. 创建依赖于用户的数据
        create_ai_advice(cursor, user_ids, RECORDS_PER_USER)
        create_physical_stats(cursor, user_ids, RECORDS_PER_USER)
        create_progress_goals(cursor, user_ids, RECORDS_PER_USER)
        create_running_records(cursor, user_ids, RECORDS_PER_USER)
        create_time_capsules(cursor, user_ids, RECORDS_PER_USER)

        # 3. 创建独立数据
        create_nutrition_tips(cursor, NUM_NUTRITION_TIPS)
        create_user_feedback(cursor, NUM_USER_FEEDBACKS)

        conn.commit()
        print("数据库填充成功完成！")

    except mysql.connector.Error as err:
        print(f"数据库操作期间发生错误: {err}")
        conn.rollback()
    except Exception as e:
        print(f"发生意外错误: {e}")
        conn.rollback()
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("数据库连接已关闭。")

if __name__ == '__main__':
    main()
