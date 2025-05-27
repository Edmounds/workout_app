from flask import Blueprint, request, jsonify
from db import get_db_connection
import json

time_capsule_bp = Blueprint('time_capsule', __name__)

@time_capsule_bp.route('/api/time_capsule', methods=['POST'])
def create_time_capsule():
    """创建时间胶囊"""
    data = request.json
    
    required_fields = ['user_id', 'target_months', 'metrics']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必要参数: {field}'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE id = %s", (data['user_id'],))
        if not cursor.fetchone():
            return jsonify({'error': '用户不存在'}), 404
        
        # 将metrics转换为JSON字符串
        metrics_json = json.dumps(data['metrics'])
        
        # 构建插入语句
        fields = ['user_id', 'target_months', 'metrics']
        values = [data['user_id'], data['target_months'], metrics_json]
        
        # 添加可选字段
        if 'reminder_freq' in data:
            fields.append('reminder_freq')
            values.append(data['reminder_freq'])
        
        # 添加创建时间和计算目标时间
        fields.extend(['created_at', 'target_date'])
        placeholders = ['%s'] * len(values) + ['NOW()', 'DATE_ADD(NOW(), INTERVAL %s MONTH)']
        values.append(data['target_months'])
        
        # 构建SQL语句
        sql = f"""
        INSERT INTO time_capsule ({', '.join(fields)})
        VALUES ({', '.join(placeholders)})
        """
        
        cursor.execute(sql, values)
        conn.commit()
        
        # 获取新记录ID
        capsule_id = cursor.lastrowid
        
        return jsonify({'message': '时间胶囊创建成功', 'capsule_id': capsule_id}), 201
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': f'创建时间胶囊失败: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@time_capsule_bp.route('/api/time_capsule', methods=['GET'])
def get_time_capsules():
    """获取时间胶囊"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID参数'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({'error': '用户不存在'}), 404
        
        # 获取用户的时间胶囊
        cursor.execute("""
        SELECT id, user_id, target_months, metrics, reminder_freq, 
               created_at, target_date, opened
        FROM time_capsule 
        WHERE user_id = %s
        ORDER BY target_date ASC
        """, (user_id,))
        
        capsules = cursor.fetchall()
        
        # 将metrics从JSON字符串转换为对象
        for capsule in capsules:
            if 'metrics' in capsule and capsule['metrics']:
                capsule['metrics'] = json.loads(capsule['metrics'])
        
        return jsonify({'message': '获取成功', 'data': capsules}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取时间胶囊失败: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
