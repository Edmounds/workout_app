from flask import Blueprint, request, jsonify
from db import get_db_connection

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/api/user/feedback', methods=['POST'])
def submit_feedback():
    """提交用户反馈"""
    data = request.json
    
    required_fields = ['feedback_type', 'feedback_content']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必要参数: {field}'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 构建插入语句
        fields = ['feedback_type', 'feedback_content']
        values = [data['feedback_type'], data['feedback_content']]
        
        # 添加可选字段
        if 'contact' in data:
            fields.append('contact')
            values.append(data['contact'])
            
        if 'user_id' in data:
            fields.append('user_id')
            values.append(data['user_id'])
            
            # 检查用户是否存在
            if data['user_id']:
                cursor.execute("SELECT id FROM users WHERE id = %s", (data['user_id'],))
                if not cursor.fetchone():
                    return jsonify({'error': '用户不存在'}), 404
        
        # 添加创建时间
        fields.append('created_at')
        placeholders = ['%s'] * len(values) + ['NOW()']
        
        # 构建SQL语句
        sql = f"""
        INSERT INTO user_feedback ({', '.join(fields)})
        VALUES ({', '.join(placeholders)})
        """
        
        cursor.execute(sql, values)
        conn.commit()
        
        # 获取新记录ID
        feedback_id = cursor.lastrowid
        
        return jsonify({'message': '反馈提交成功', 'feedback_id': feedback_id}), 201
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': f'提交反馈失败: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
