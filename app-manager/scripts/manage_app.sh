#!/bin/bash

# Configuration
APP_FILE="todo_app.py"
PORT=5000
WORKSPACE_DIR="/data/data/com.termux/files/home/todo-budget-manager"

cd "$WORKSPACE_DIR"

# Define taskkill equivalent for Linux/Termux
taskkill() {
    echo "Using taskkill (kill) on PID: $1"
    kill -9 "$1" > /dev/null 2>&1
}

case "$1" in
    start)
        echo "Starting application..."
        python "$APP_FILE" > /dev/null 2>&1 &
        echo "Application started in background."
        ;;
    stop)
        echo "Stopping application using netstat and taskkill logic..."
        # Use netstat to find PID (if possible) or fallback to ps
        PID=$(netstat -antp 2>/dev/null | grep ":$PORT" | grep "LISTEN" | awk '{print $7}' | cut -d'/' -f1)
        
        if [ -z "$PID" ]; then
            PID=$(ps aux | grep "$APP_FILE" | grep -v grep | awk '{print $2}')
        fi

        if [ ! -z "$PID" ]; then
            taskkill "$PID"
            echo "Application stopped."
        else
            echo "No process found on port $PORT or for $APP_FILE."
        fi
        ;;
    restart)
        echo "Restarting application..."
        $0 stop
        $0 start
        echo "Application restarted."
        ;;
    status)
        PID=$(ps aux | grep "$APP_FILE" | grep -v grep | awk '{print $2}')
        if [ ! -z "$PID" ]; then
            echo "Application is running (PID: $PID)."
        else
            echo "Application is not running."
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
