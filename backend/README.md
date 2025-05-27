# 健康运动API服务器

这是一个基于Flask的健康运动应用后端API服务器，为移动应用提供完整的数据管理功能。

## 功能模块

- **用户数据管理**：注册、登录、个人信息管理
- **健康数据可视化**：运动记录查询、健康统计数据
- **个性化训练计划**：进度目标设置、查询与管理
- **营养与恢复建议**：营养提示、AI健康建议
- **用户反馈与交互**：收集用户反馈
- **健康数据时间胶囊**：创建和查看健康目标时间胶囊

## 技术栈

- Python 3.9+
- Flask 2.2+
- MySQL 8.0+
- flask-cors
- mysql-connector-python

## 安装与设置

1. 克隆仓库到本地

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 数据库设置:
   - 创建名为`workout_app`的MySQL数据库
   - 使用`workout_app.sql`导入数据库结构
```bash
mysql -u username -p workout_app < workout_app.sql
```

4. 配置数据库连接:
   - 编辑`.env`文件中的数据库连接信息

## 运行服务器

### 开发环境

```bash
cd /path/to/backend
python app.py
```

### 生产环境

使用uwsgi运行:

```bash
uwsgi --ini uwsgi.ini
```

## API端点

请参阅`服务器后端API更新版.openapi.3.0.json`文件获取完整API文档

### 主要端点概览

- 用户相关
  - `POST /api/users/login` - 用户登录
  - `POST /api/user/register` - 用户注册
  - `GET /api/users/profile` - 获取用户信息
  - `PUT /api/user/update` - 更新用户信息

- 运动数据
  - `POST /api/workout/upload` - 上传运动数据
  - `GET /api/user/running_records` - 获取运动记录列表

- 健康统计
  - `GET /api/health/stats` - 获取健康统计数据

- 进度目标
  - `GET /api/progress/goals` - 获取进度目标
  - `POST /api/progress/goals` - 创建进度目标
  - `PUT /api/progress/goals/{id}` - 更新进度目标
  - `DELETE /api/progress/goals/{id}` - 删除进度目标

- 营养与AI建议
  - `GET /api/nutrition/tips` - 获取营养提示
  - `GET /api/ai/advice` - 获取AI建议

- 用户反馈
  - `POST /api/user/feedback` - 提交用户反馈

- 时间胶囊
  - `POST /api/time_capsule` - 创建时间胶囊
  - `GET /api/time_capsule` - 获取时间胶囊

## 数据初始化

可以使用`populate_db.py`脚本生成测试数据:

```bash
python populate_db.py
```

## 开发说明

- 所有API遵循RESTful设计原则
- 响应格式为JSON，包含状态码、消息和数据字段
- 数据库操作使用连接池以提高性能
- 错误处理遵循一致的格式
