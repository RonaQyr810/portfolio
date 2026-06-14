@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在同步桌面项目到 projects/ ...
python scripts\sync-desktop-projects.py
echo.
echo 正在同步设计截图到 assets/portfolio/ ...
python sync_portfolio_assets.py
echo.
echo 正在同步项目卡片封面 ...
python scripts\sync-project-covers.py
echo.
echo 正在同步视频到 assets/videos/ ...
python scripts\sync-videos.py
echo.
echo 完成。请运行 start-site.bat 本地预览，或 deploy-vercel.bat 部署。
pause
