@echo off
chcp 65001 >nul
set "ROOT=%~dp0..\..\"
cd /d "%ROOT%"
set PORT=8080
set "URL=http://127.0.0.1:8080/projects/rikxiniao/app/"

powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing -Uri '%URL%' -TimeoutSec 2).StatusCode } catch { '0' }" > "%TEMP%\portfolio-serve-check.txt"
set /p SERVE_OK=<"%TEMP%\portfolio-serve-check.txt"
if "%SERVE_OK%"=="200" (
  start "" "%URL%"
  exit /b 0
)

echo 正在启动本地预览服务...
start "个人主页预览" /D "%ROOT%" cmd /k "npx --yes serve -l %PORT%"
timeout /t 4 /nobreak >nul
start "" "%URL%"
