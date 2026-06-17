@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo  个人主页 · 部署到 GitHub Pages（810）
echo ========================================
echo.
echo 已停用 Vercel，请使用 GitHub Pages 官网：
echo   https://ronaqyr810.github.io/portfolio/
echo.
call "%~dp0deploy.bat"
