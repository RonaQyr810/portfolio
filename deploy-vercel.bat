@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo  个人主页 · Vercel 部署（不依赖 GitHub）
echo ========================================
echo.
echo 步骤 1：浏览器会打开 Vercel 登录页，用邮箱注册/登录即可。
echo 步骤 2：登录成功后，本窗口会自动上传并发布网站。
echo.

where node >nul 2>&1
if errorlevel 1 (
  echo [错误] 未检测到 Node.js，请先安装：https://nodejs.org
  pause
  exit /b 1
)

echo 正在启动 Vercel 登录...
call npx vercel login
if errorlevel 1 (
  echo [失败] Vercel 登录未完成，请重试。
  pause
  exit /b 1
)

echo.
echo 正在部署到生产环境（含视频等大文件，可能需要几分钟）...
call npx vercel deploy --prod --yes

if errorlevel 1 (
  echo.
  echo [失败] 部署未成功，请检查网络后重试。
  pause
  exit /b 1
)

echo.
echo [成功] 部署完成！请查看上方输出的 Production 网址。
echo.
pause
