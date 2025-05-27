from flask import Blueprint, request, jsonify
from db import get_db_connection

workout_bp = Blueprint('workout', __name__)

@workout_bp.route('/api/workout/upload', methods=['POST'])
def upload_workout():
    """上传运动数据"""
    data = request.json
    
    required_fields = ['user_id', 'workout_type', 'start_time', 'duration', 'distance']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required parameter: {field}'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE id = %s", (data['user_id'],))
        if not cursor.fetchone():
            return jsonify({'error': 'User not found'}), 404
        
        # 构建插入语句
        fields = []
        placeholders = []
        values = []
        
        # 添加所有可能的字段
        field_mapping = {
            'user_id': 'user_id',
            'workout_type': 'workout_type',
            'start_time': 'start_time',
            'end_time': 'end_time',
            'duration': 'duration',
            'distance': 'distance',
            'avg_pace': 'avg_pace',
            'best_pace': 'best_pace',
            'avg_heart_rate': 'avg_heart_rate',
            'max_heart_rate': 'max_heart_rate',
            'avg_step_rate': 'avg_step_rate',
            'calories': 'calories',
            'elevation_gain': 'elevation_gain',
            'weather': 'weather',
            'temperature': 'temperature',
            'notes': 'notes'
        }
        
        for api_field, db_field in field_mapping.items():
            if api_field in data:
                fields.append(db_field)
                placeholders.append("%s")
                values.append(data[api_field])
        
        # 构建SQL语句
        sql = f"""
        INSERT INTO running_records ({', '.join(fields)}) 
        VALUES ({', '.join(placeholders)})
        """
        
        print(f"DEBUG - SQL: {sql}")
        print(f"DEBUG - Values: {values}")
        
        cursor.execute(sql, values)
        conn.commit()
        
        # 获取新记录ID
        workout_id = cursor.lastrowid
        
        return jsonify({'message': 'Workout data uploaded successfully', 'workout_id': workout_id}), 200
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': f'Failed to upload workout data: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@workout_bp.route('/api/user/running_records', methods=['GET'])
def get_running_records():
    """获取运动记录列表"""
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not user_id:
        return jsonify({'error': 'Missing user ID parameter'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 构建查询条件
        conditions = ["user_id = %s"]
        params = [user_id]
        
        if start_date:
            conditions.append("DATE(start_time) >= %s")
            params.append(start_date)
        
        if end_date:
            conditions.append("DATE(start_time) <= %s")
            params.append(end_date)
        
        # 构建SQL语句
        sql = """
        SELECT * FROM running_records 
        WHERE {} 
        ORDER BY start_time DESC
        """.format(" AND ".join(conditions))
        
        cursor.execute(sql, params)
        records = cursor.fetchall()
        
        return jsonify({'message': 'Records retrieved successfully', 'data': records}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve workout records: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
