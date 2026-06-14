@echo off
chcp 65001 >nul
cd /d "%~dp0..\moyan-app"
if not exist server.js (
  echo [错误] 找不到 moyan-app，请确认项目文件完整
  pause
  exit /b 1
)
where node >nul 2>&1
if errorlevel 1 (
  echo [错误] 未检测到 Node.js，请先安装：https://nodejs.org
  pause
  exit /b 1
)
set PORT=3010
set HOSTNAME=127.0.0.1
set LLM_PROVIDER=mock
echo 正在启动墨演演示服务...
echo 启动完成后访问：http://127.0.0.1:3010
echo 按 Ctrl+C 可停止服务
node server.js
if errorlevel 1 pause
