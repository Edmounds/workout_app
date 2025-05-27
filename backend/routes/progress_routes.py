from flask import Blueprint, request, jsonify
from db import get_db_connection

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/api/progress/goals', methods=['GET'])
def get_goals():
    """获取进度目标"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Missing user ID parameter'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'User not found'}), 404
        
        # 获取用户的进度目标
        cursor.execute("""
        SELECT id, user_id, title, current_value, target_value, category, deadline, 
               created_at
        FROM progress_goals 
        WHERE user_id = %s
        ORDER BY deadline ASC
        """, (user_id,))
        
        goals = cursor.fetchall()
        
        return jsonify({'message': 'Goals retrieved successfully', 'data': goals}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve progress goals: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@progress_bp.route('/api/progress/goals', methods=['POST'])
def create_goal():
    """创建进度目标"""
    data = request.json
    
    required_fields = ['user_id', 'title', 'target_value', 'category']
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
        fields = ['user_id', 'title', 'target_value', 'category']
        values = [data['user_id'], data['title'], data['target_value'], data['category']]
        
        # 添加可选字段
        if 'current_value' in data:
            fields.append('current_value')
            values.append(data['current_value'])
        else:
            fields.append('current_value')
            values.append(0)  # 默认值为0
            
        if 'deadline' in data:
            fields.append('deadline')
            values.append(data['deadline'])
        
        # 添加创建时间
        fields.append('created_at') # Only include created_at
        placeholders_for_values = ['%s'] * len(values)
        placeholders_for_functions = ['NOW()'] # Only for created_at
        
        all_placeholders_for_sql = placeholders_for_values + placeholders_for_functions
        
        # 构建SQL语句
        sql = f"""
        INSERT INTO progress_goals ({', '.join(fields)})
        VALUES ({', '.join(all_placeholders_for_sql)})
        """
        
        cursor.execute(sql, values)
        conn.commit()
        
        # 获取新记录ID
        goal_id = cursor.lastrowid
        
        return jsonify({'message': 'Progress goal created successfully', 'goal_id': goal_id}), 201
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': f'Failed to create progress goal: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@progress_bp.route('/api/progress/goals/<int:id>', methods=['PUT'])
def update_goal(id):
    """更新进度目标"""
    data = request.json
    
    if not id:
        return jsonify({'error': '缺少目标ID参数'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 检查目标是否存在
        cursor.execute("SELECT id, user_id FROM progress_goals WHERE id = %s", (id,))
        goal = cursor.fetchone()
        
        if not goal:
            return jsonify({'error': '目标不存在'}), 404
        
        # 构建更新语句
        update_fields = []
        params = []
        
        if 'current_value' in data:
            update_fields.append("current_value = %s")
            params.append(data['current_value'])
            
        if 'target_value' in data:
            update_fields.append("target_value = %s")
            params.append(data['target_value'])
            
        if 'title' in data:
            update_fields.append("title = %s")
            params.append(data['title'])
            
        if 'deadline' in data:
            update_fields.append("deadline = %s")
            params.append(data['deadline'])
            
        if 'completed' in data:
            update_fields.append("completed = %s")
            params.append(data['completed'])
        
        if not update_fields:
            return jsonify({'message': '没有数据需要更新'}), 200
        
        # 构建SQL语句
        sql = "UPDATE progress_goals SET " + ", ".join(update_fields) + " WHERE id = %s"
        params.append(id)
        
        cursor.execute(sql, params)
        conn.commit()
        
        # 检查是否有记录被更新
        if cursor.rowcount > 0:
            return jsonify({'message': '目标更新成功'}), 200
        else:
            return jsonify({'message': '没有数据被更新'}), 200
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': f'更新目标失败: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@progress_bp.route('/api/progress/goals/<int:id>', methods=['DELETE'])
def delete_goal(id):
    """删除进度目标"""
    if not id:
        return jsonify({'error': '缺少目标ID参数'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 检查目标是否存在
        cursor.execute("SELECT id FROM progress_goals WHERE id = %s", (id,))
        if not cursor.fetchone():
            return jsonify({'error': '目标不存在'}), 404
        
        # 删除目标
        cursor.execute("DELETE FROM progress_goals WHERE id = %s", (id,))
        conn.commit()
        
        # 检查是否有记录被删除
        if cursor.rowcount > 0:
            return jsonify({'message': '目标删除成功'}), 200
        else:
            return jsonify({'error': '删除失败，请稍后重试'}), 500
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': f'删除目标失败: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
