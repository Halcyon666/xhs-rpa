@echo off
chcp 65001 >nul
echo 正在启动专用浏览器...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="E:\gemini-lifesync\xhs-rpa\chrome-profile"
echo ========================================================
echo [重要] 请在打开的浏览器中登录小红书账号
echo 登录成功后，请保持浏览器开启，不要关闭！
echo ========================================================
pause