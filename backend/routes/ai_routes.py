from flask import Blueprint, request, jsonify
from db import get_db_connection

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/ai/advice', methods=['GET'])
def get_ai_advice():
    """获取AI建议"""
    user_id = request.args.get('user_id')
    category = request.args.get('category')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID参数'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({'error': '用户不存在'}), 404
        
        # 构建查询条件
        conditions = ["user_id = %s"]
        params = [user_id]
        
        if category:
            conditions.append("category = %s")
            params.append(category)
        
        # 构建SQL语句
        sql = """
        SELECT id, user_id, advice_content as content, category, created_at
        FROM ai_advice
        WHERE {}
        ORDER BY created_at DESC
        """.format(" AND ".join(conditions))
        
        cursor.execute(sql, params)
        advice = cursor.fetchall()
        
        # 如果没有数据，生成一些基于用户信息的建议
        if not advice:
            # 获取用户信息
            cursor.execute("""
            SELECT id, username, gender, age, height, weight, level
            FROM users WHERE id = %s
            """, (user_id,))
            
            user = cursor.fetchone()
            
            # 获取用户运动数据
            cursor.execute("""
            SELECT COUNT(*) as workout_count, 
                   SUM(duration) as total_duration, 
                   SUM(distance) as total_distance
            FROM workouts 
            WHERE user_id = %s
            """, (user_id,))
            
            workout_stats = cursor.fetchone()
            
            # 根据用户信息和运动数据生成简单的建议
            default_advice = []
            
            if workout_stats and workout_stats['workout_count'] > 0:
                default_advice.append({
                    'id': None,
                    'user_id': user_id,
                    'content': f"根据您的运动记录，您已完成{workout_stats['workout_count']}次运动，总距离约{workout_stats['total_distance']/1000:.1f}公里。建议您继续保持运动习惯，提高心肺能力。",
                    'category': '训练建议',
                    'created_at': None
                })
            else:
                default_advice.append({
                    'id': None,
                    'user_id': user_id,
                    'content': "您目前还没有运动记录。建议您开始定期进行有氧运动，每周至少3次，每次30分钟以上。",
                    'category': '训练建议',
                    'created_at': None
                })
            
            default_advice.append({
                'id': None,
                'user_id': user_id,
                'content': "记得保持充分的水分补充，运动前后都要补充水分。成人每天应摄入约2升水。",
                'category': '营养建议',
                'created_at': None
            })
            
            if category:
                default_advice = [a for a in default_advice if a['category'] == category]
            
            return jsonify({'message': '获取成功', 'data': default_advice}), 200
        
        return jsonify({'message': '获取成功', 'data': advice}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取AI建议失败: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
