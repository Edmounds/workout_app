from flask import Blueprint, request, jsonify
from db import get_db_connection

health_bp = Blueprint('health', __name__)

@health_bp.route('/api/health/stats', methods=['GET'])
def get_health_stats():
    """获取健康统计数据"""
    user_id = request.args.get('user_id')
    date = request.args.get('date')
    
    if not user_id:
        return jsonify({'error': 'Missing user ID parameter'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 获取用户基本信息
        cursor.execute("""
        SELECT id, username, height, weight, age, gender, level
        FROM users WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # 构建查询条件
        conditions = ["user_id = %s"]
        params = [user_id]
        
        if date:
            conditions.append("DATE(start_time) = %s")
            params.append(date)
        else:
            # 默认查询最近一周的数据
            conditions.append("start_time >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)")
        
        # 获取运动数据
        sql = """
        SELECT 
            workout_type,
            SUM(duration) as total_duration,
            SUM(distance) as total_distance,
            AVG(avg_heart_rate) as avg_heart_rate,
            MAX(max_heart_rate) as max_heart_rate,
            SUM(calories) as total_calories
        FROM running_records 
        WHERE {} 
        GROUP BY workout_type
        """.format(" AND ".join(conditions))
        
        cursor.execute(sql, params)
        workout_stats = cursor.fetchall()
        
        # 获取总体健康指标
        cursor.execute("""
        SELECT 
            COUNT(*) as workout_count,
            SUM(duration) as total_duration,
            SUM(distance) as total_distance,
            SUM(calories) as total_calories
        FROM running_records 
        WHERE {}
        """.format(" AND ".join(conditions)), params)
        
        overall_stats = cursor.fetchone()
        
        # 组合结果
        result = {
            'user_info': user,
            'workout_stats': workout_stats,
            'overall_stats': overall_stats
        }
        
        return jsonify({'message': 'Data retrieved successfully', 'data': result}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve health statistics: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
