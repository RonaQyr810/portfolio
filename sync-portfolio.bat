@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在从「作品集」同步图片到 assets/portfolio ...
python sync_portfolio_assets.py
echo.
echo 同步完成后，请运行 deploy-vercel.bat 部署到线上。
pause
