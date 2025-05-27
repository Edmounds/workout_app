# 健康运动API服务器 - 使用指南

## 项目介绍

健康运动API服务器是一个基于Flask的后端系统，旨在为健康运动应用提供完整的数据管理和API服务。系统包括用户管理、运动数据记录、健康统计、训练计划、营养建议等功能模块。

## 项目目录结构

```
backend/
  ├── app.py             # 主应用文件
  ├── db.py              # 数据库连接管理
  ├── init_db.py         # 数据库初始化脚本  
  ├── install.py         # 安装脚本
  ├── requirements.txt   # 依赖包列表
  ├── run.py             # 运行脚本
  ├── test_api.py        # API测试脚本
  ├── uwsgi.ini          # uwsgi配置文件
  ├── uwsgi.sh           # uwsgi服务管理脚本
  └── routes/            # API路由模块
      ├── user_routes.py         # 用户相关API
      ├── workout_routes.py      # 运动数据相关API
      ├── health_routes.py       # 健康统计相关API
      ├── progress_routes.py     # 进度目标相关API
      ├── nutrition_routes.py    # 营养提示相关API
      ├── ai_routes.py           # AI建议相关API
      ├── feedback_routes.py     # 用户反馈相关API
      └── time_capsule_routes.py # 时间胶囊相关API
```

## 安装步骤

1. 确保已安装Python 3.7+和MySQL 8.0+

2. 执行安装脚本:
```bash
cd /path/to/backend
python install.py
```
安装过程中会:
- 安装所需的Python依赖包
- 创建.env配置文件
- 创建数据库(如果尚未存在)

3. 初始化数据库:
```bash
python init_db.py
```
此步骤会创建必要的数据库表结构并添加基础数据

## 启动服务

### 开发环境

使用Flask内置服务器启动(推荐用于开发):
```bash
python run.py
```

### 生产环境

使用uwsgi启动(推荐用于生产):
```bash
./uwsgi.sh start
```

其他uwsgi命令:
- 停止服务: `./uwsgi.sh stop`
- 重启服务: `./uwsgi.sh restart`
- 重载配置: `./uwsgi.sh reload`
- 查看状态: `./uwsgi.sh status`

## API测试

运行API测试脚本检验服务是否正常运行:
```bash
python test_api.py
```

## 配置说明

通过编辑`.env`文件可以修改以下配置:

### 数据库配置
- `DB_HOST`: 数据库主机地址
- `DB_USER`: 数据库用户名
- `DB_PASSWORD`: 数据库密码
- `DB_NAME`: 数据库名称

### 服务器配置
- `SERVER_HOST`: 服务器监听地址
- `SERVER_PORT`: 服务器监听端口
- `DEBUG`: 是否启用调试模式(True/False)

## API文档

完整API文档请参阅`服务器后端API更新版.openapi.3.0.json`文件

## 常见问题

1. 数据库连接失败
   - 检查MySQL服务是否运行
   - 确认`.env`文件中的数据库配置正确
   - 确认数据库用户有足够权限

2. 端口占用冲突
   - 修改`.env`文件中的`SERVER_PORT`值
   - 确认没有其他程序占用该端口

3. 权限问题
   - 确保运行目录有足够的读写权限
   - 日志目录(`logs/`)需要可写权限

## 联系支持

如有任何问题，请通过提交用户反馈或直接联系开发团队获取支持。
