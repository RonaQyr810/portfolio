@echo off
chcp 65001 >nul
set "GIT=C:\Program Files\Git\bin\git.exe"
set "ROOT=%~dp0"
cd /d "%ROOT%"

echo ========================================
echo  个人主页 → GitHub 推送脚本
echo  账号: RonaQyr810
echo  仓库: https://github.com/RonaQyr810/portfolio
echo ========================================
echo.

"%GIT%" branch -M main 2>nul

"%GIT%" remote get-url origin >nul 2>&1
if errorlevel 1 (
  "%GIT%" remote add origin https://github.com/RonaQyr810/portfolio.git
  echo 已添加远程仓库 origin
) else (
  "%GIT%" remote set-url origin https://github.com/RonaQyr810/portfolio.git
  echo 已更新远程仓库地址
)

echo.
echo 正在提交并推送到 GitHub...
echo 若弹出登录窗口，请用 RonaQyr810 账号登录（不要用 Queen-qyr）。
echo.

"%GIT%" add -A
"%GIT%" diff --cached --quiet
if errorlevel 1 (
  "%GIT%" commit -m "Update portfolio site"
)

"%GIT%" push -u origin main

if errorlevel 1 (
  echo.
  echo [失败] 推送未成功。请开 VPN 或手机热点后重试。
  echo 常见原因：无法连接 github.com
  pause
  exit /b 1
)

echo.
echo [成功] 代码已推送到 GitHub！
echo 仓库: https://github.com/RonaQyr810/portfolio
echo.
echo --- 开启公网访问（只需做一次）---
echo 1. 打开 https://github.com/RonaQyr810/portfolio/settings/pages
echo 2. Source 选 GitHub Actions
echo 3. 打开 https://github.com/RonaQyr810/portfolio/actions 等待绿色勾
echo 4. 访问官网: https://ronaqyr810.github.io/portfolio/
echo.
pause
