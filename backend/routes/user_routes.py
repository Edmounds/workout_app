from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/users/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # 登录成功，返回用户信息，不包括密码
        user.pop('password', None)
        return jsonify({'message': 'Login successful', 'data': user}), 200
        
    except Exception as e:
        return jsonify({'error': f'登录失败: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@user_bp.route('/api/user/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password or not email:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    gender = data.get('gender')
    age = data.get('age')
    height = data.get('height')
    weight = data.get('weight')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 检查用户名是否已存在
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'error': 'Username already exists'}), 400
            
        # 检查邮箱是否已存在
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'error': 'Email already registered'}), 400
        
        # 密码加密
        hashed_password = generate_password_hash(password)
        
        # 插入用户数据
        sql = """
        INSERT INTO users (username, password, email, gender, age, height, weight, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(sql, (username, hashed_password, email, gender, age, height, weight))
        conn.commit()
        
        # 获取新用户ID
        user_id = cursor.lastrowid
        
        return jsonify({'message': 'Registration successful', 'user_id': user_id}), 201
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@user_bp.route('/api/users/profile', methods=['GET'])
def get_profile():
    """获取用户信息"""
    user_id = request.args.get('id')
    
    if not user_id:
        return jsonify({'error': 'Missing user ID parameter'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
        SELECT id, username, email, gender, age, height, weight, level, created_at, updated_at
        FROM users WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({'message': 'Success', 'data': user}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取用户信息失败: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@user_bp.route('/api/user/update', methods=['PUT'])
def update_user():
    """更新用户信息"""
    data = request.json
    user_id = data.get('id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID参数'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({'error': '用户不存在'}), 404
        
        # 构建更新语句
        update_fields = []
        params = []
        
        if 'username' in data:
            update_fields.append("username = %s")
            params.append(data['username'])
            
        if 'gender' in data:
            update_fields.append("gender = %s")
            params.append(data['gender'])
            
        if 'age' in data:
            update_fields.append("age = %s")
            params.append(data['age'])
            
        if 'height' in data:
            update_fields.append("height = %s")
            params.append(data['height'])
            
        if 'weight' in data:
            update_fields.append("weight = %s")
            params.append(data['weight'])
            
        if 'level' in data:
            update_fields.append("level = %s")
            params.append(data['level'])
        
        if not update_fields:
            return jsonify({'message': '没有数据需要更新'}), 200
        
        # 添加最后更新时间
        update_fields.append("updated_at = NOW()")
        
        # 构建SQL语句
        sql = "UPDATE users SET " + ", ".join(update_fields) + " WHERE id = %s"
        params.append(user_id)
        
        cursor.execute(sql, params)
        conn.commit()
        
        # 检查是否有记录被更新
        if cursor.rowcount > 0:
            return jsonify({'message': '用户信息更新成功'}), 200
        else:
            return jsonify({'message': '没有数据被更新'}), 200
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': f'更新用户信息失败: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
