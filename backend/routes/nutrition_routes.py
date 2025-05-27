from flask import Blueprint, request, jsonify
from db import get_db_connection

nutrition_bp = Blueprint('nutrition', __name__)

@nutrition_bp.route('/api/nutrition/tips', methods=['GET'])
def get_nutrition_tips():
    """获取营养提示"""
    category = request.args.get('category')
    importance = request.args.get('importance')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 构建查询条件
        conditions = []
        params = []
        
        if category:
            conditions.append("category = %s")
            params.append(category)
        
        if importance:
            conditions.append("importance = %s")
            params.append(importance)
        
        # 构建SQL语句
        if conditions:
            sql = """
            SELECT id, tip as content, category, importance, NOW() as created_at
            FROM nutrition_tips
            WHERE {}
            ORDER BY importance DESC
            """.format(" AND ".join(conditions))
        else:
            sql = """
            SELECT id, tip as content, category, importance, NOW() as created_at
            FROM nutrition_tips
            ORDER BY importance DESC
            """
        
        cursor.execute(sql, params)
        tips = cursor.fetchall()
        
        return jsonify({'message': '获取成功', 'data': tips}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取营养提示失败: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
