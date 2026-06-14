@echo off
chcp 65001 >nul
set "GIT=C:\Program Files\Git\bin\git.exe"
set "ROOT=%~dp0"
cd /d "%ROOT%"

echo ========================================
echo  个人主页 · 一键部署
echo  仓库: https://github.com/RonaQyr810/portfolio
echo  官网: https://ronaqyr810.github.io/portfolio/
echo ========================================
echo.

"%GIT%" branch -M main 2>nul

"%GIT%" remote get-url origin >nul 2>&1
if errorlevel 1 (
  "%GIT%" remote add origin https://github.com/RonaQyr810/portfolio.git
) else (
  "%GIT%" remote set-url origin https://github.com/RonaQyr810/portfolio.git
)

echo [1/4] 检测 GitHub 网络...
ping -n 1 github.com >nul 2>&1
if errorlevel 1 (
  echo [警告] 无法解析 github.com，请换手机热点或开 VPN 后重试。
  echo.
  pause
  exit /b 1
)

echo [2/4] 提交本地更改...
"%GIT%" add -A
"%GIT%" diff --cached --quiet
if errorlevel 1 (
  "%GIT%" commit -m "Deploy portfolio site"
  echo 已创建新提交。
) else (
  echo 没有新的更改需要提交。
)

echo [3/4] 推送到 GitHub（含视频 LFS，可能较慢）...
echo 若弹出登录窗口，请用 Apple 账号登录 GitHub。
echo.

set PUSH_OK=0
"%GIT%" -c http.version=HTTP/1.1 push -u origin main
if not errorlevel 1 set PUSH_OK=1

if "%PUSH_OK%"=="0" (
  echo.
  echo 直连失败，尝试镜像加速...
  "%GIT%" remote set-url origin https://ghfast.top/https://github.com/RonaQyr810/portfolio.git
  "%GIT%" -c http.version=HTTP/1.1 push -u origin main
  if not errorlevel 1 set PUSH_OK=1
  "%GIT%" remote set-url origin https://github.com/RonaQyr810/portfolio.git
)

if "%PUSH_OK%"=="0" (
  echo.
  echo [失败] 推送未成功。常见原因：
  echo   - 无法连接 GitHub（请开 VPN 或手机热点）
  echo   - 未登录 GitHub（重新运行并登录）
  echo   - Git LFS 视频上传超时（多试几次或换网络）
  echo.
  pause
  exit /b 1
)

echo.
echo [4/4] 触发 GitHub Pages 部署...
echo.
echo [成功] 代码已推送到 GitHub！
echo.
echo --- 首次部署请确认（只需做一次）---
echo 1. 打开 https://github.com/RonaQyr810/portfolio/settings/pages
echo 2. Build and deployment → Source 选「GitHub Actions」
echo 3. 打开 https://github.com/RonaQyr810/portfolio/actions
echo    等待「Deploy to GitHub Pages」出现绿色勾
echo 4. 访问官网: https://ronaqyr810.github.io/portfolio/
echo.
start "" "https://github.com/RonaQyr810/portfolio/actions"
pause
