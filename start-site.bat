@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PORT=8080
set "URL=http://127.0.0.1:%PORT%/index.html#portfolio"

where node >nul 2>&1
if errorlevel 1 (
  echo [错误] 未检测到 Node.js，请先安装：https://nodejs.org
  pause
  exit /b 1
)

echo 正在检查本地预览服务...

powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:%PORT%/' -TimeoutSec 2).StatusCode } catch { '0' }" > "%TEMP%\portfolio-serve-check.txt"
set /p SERVE_OK=<"%TEMP%\portfolio-serve-check.txt"

if "%SERVE_OK%"=="200" (
  echo 服务已在运行，正在打开浏览器...
  start "" "%URL%"
  exit /b 0
)

echo.
echo 正在启动个人主页预览服务（端口 %PORT%）...
echo 请勿关闭此窗口，关闭后网站会停止。
echo.
start "个人主页预览" /D "%~dp0" cmd /k "npx --yes serve -l %PORT%"

echo 等待服务就绪...
set /n=0
:wait_loop
timeout /t 2 /nobreak >nul
powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:%PORT%/' -TimeoutSec 3).StatusCode } catch { '0' }" > "%TEMP%\portfolio-serve-check.txt"
set /p SERVE_OK=<"%TEMP%\portfolio-serve-check.txt"
if "%SERVE_OK%"=="200" goto open_browser
set /a n+=1
if %n% lss 15 goto wait_loop

echo.
echo [提示] 服务启动较慢，请稍后在浏览器手动打开：
echo   %URL%
echo 并确认标题为「个人主页预览」的窗口仍在运行。
pause
exit /b 1

:open_browser
echo 服务已就绪，正在打开浏览器...
start "" "%URL%"
echo.
echo 预览地址：%URL%
echo 按任意键可关闭本窗口（预览服务会继续在另一窗口运行）。
pause >nul
