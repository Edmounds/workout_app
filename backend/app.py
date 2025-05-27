from flask import Flask, jsonify
from flask_cors import CORS
import os

from routes.user_routes import user_bp
from routes.workout_routes import workout_bp
from routes.health_routes import health_bp
from routes.progress_routes import progress_bp
from routes.nutrition_routes import nutrition_bp
from routes.ai_routes import ai_bp
from routes.feedback_routes import feedback_bp
from routes.time_capsule_routes import time_capsule_bp

# 创建Flask应用
app = Flask(__name__)

# 配置密钥
app.secret_key = os.environ.get("SECRET_KEY", "workout_app_secret_key_2025")

# 启用CORS，允许前端跨域请求
CORS(app)

# 注册各个路由蓝图
app.register_blueprint(user_bp)
app.register_blueprint(workout_bp)
app.register_blueprint(health_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(nutrition_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(time_capsule_bp)

@app.route('/')
def index():
    return {'message': 'Health & Fitness API Server Running'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
