#!/bin/bash
# uwsgi服务控制脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UWSGI_INI="$SCRIPT_DIR/uwsgi.ini"
UWSGI_PID="$SCRIPT_DIR/uwsgi.pid"
LOGS_DIR="$SCRIPT_DIR/logs"

# 确保日志目录存在
mkdir -p "$LOGS_DIR"

# 检查uwsgi是否已安装
if ! command -v uwsgi &> /dev/null; then
    echo "错误: uwsgi 未安装. 请使用 'pip install uwsgi' 安装."
    exit 1
fi

# 显示帮助信息
show_help() {
    echo "用法: $0 {start|stop|restart|status|reload}"
    echo ""
    echo "控制uwsgi服务的运行:"
    echo "  start   - 启动服务"
    echo "  stop    - 停止服务"
    echo "  restart - 重启服务"
    echo "  reload  - 重新加载配置"
    echo "  status  - 查看服务状态"
}

# 检查服务状态
check_status() {
    if [ -f "$UWSGI_PID" ]; then
        PID=$(cat "$UWSGI_PID")
        if ps -p "$PID" > /dev/null; then
            echo "uwsgi 正在运行 (PID: $PID)"
            return 0
        else
            echo "uwsgi 未运行 (PID文件存在但进程已终止)"
            return 1
        fi
    else
        echo "uwsgi 未运行 (没有PID文件)"
        return 1
    fi
}

# 启动服务
start_service() {
    echo "正在启动 uwsgi 服务..."
    if [ -f "$UWSGI_PID" ]; then
        PID=$(cat "$UWSGI_PID")
        if ps -p "$PID" > /dev/null; then
            echo "uwsgi 已经在运行 (PID: $PID)"
            return 0
        else
            echo "移除过期的 PID 文件"
            rm -f "$UWSGI_PID"
        fi
    fi
    
    uwsgi --ini "$UWSGI_INI"
    sleep 2
    check_status
}

# 停止服务
stop_service() {
    echo "正在停止 uwsgi 服务..."
    if [ -f "$UWSGI_PID" ]; then
        uwsgi --stop "$UWSGI_PID"
        sleep 2
        
        # 再次检查是否成功停止
        if [ -f "$UWSGI_PID" ]; then
            PID=$(cat "$UWSGI_PID")
            if ps -p "$PID" > /dev/null; then
                echo "警告: uwsgi 未能正常停止, 尝试强制终止..."
                kill -9 "$PID" 2>/dev/null
                rm -f "$UWSGI_PID"
            else
                rm -f "$UWSGI_PID"
            fi
        fi
        
        echo "uwsgi 已停止"
    else
        echo "uwsgi 未运行 (没有PID文件)"
    fi
}

# 重新加载配置
reload_service() {
    echo "正在重新加载 uwsgi 配置..."
    if [ -f "$UWSGI_PID" ]; then
        uwsgi --reload "$UWSGI_PID"
        sleep 1
        echo "uwsgi 配置已重新加载"
    else
        echo "uwsgi 未运行, 无法重新加载"
        start_service
    fi
}

# 根据参数执行操作
case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        stop_service
        sleep 2
        start_service
        ;;
    reload)
        reload_service
        ;;
    status)
        check_status
        ;;
    *)
        show_help
        exit 1
        ;;
esac

exit 0
