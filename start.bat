@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 小红书自动发布工具 - Dry-run 测试
echo ========================================

REM 检查是否已经登录过
if not exist "chrome-profile\Default" (
    echo [警告] 首次使用，数据目录尚未创建
    echo 请先运行 "启动浏览器.bat" 并登录小红书！
    pause
    exit /b
)

REM 激活虚拟环境 (如果存在)
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM 运行发布脚本
echo 正在连接浏览器...
python src\publisher.py

pause
