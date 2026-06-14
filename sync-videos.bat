@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "DESKTOP=%USERPROFILE%\Desktop"
set "DST=%ROOT%\assets\videos"

for /d %%D in ("%DESKTOP%\*") do (
  if exist "%%D\梨园之韵" set "PORTFOLIO=%%D"
)

if not defined PORTFOLIO (
  echo ERROR: 未找到桌面作品集文件夹
  exit /b 1
)

set "REC=%PORTFOLIO%\01-视频动画"
echo 作品集: %PORTFOLIO%
echo 目标: %DST%

call :copy "%REC%\2220048 秦艺榕 作品展示视频（用户端）.mp4" "xishixiaozhan" "user-demo.mp4"
call :copy "%REC%\2220048 秦艺榕 作品展示视频（管理端）.mp4" "xishixiaozhan" "admin-demo.mp4"
call :copy "%PORTFOLIO%\梨园之韵\梨园之韵 最终成品.mp4" "peking-opera" "final.mp4"
call :copy "%PORTFOLIO%\信息可视化\京剧1.mp4" "peking-opera" "opera-1.mp4"
call :copy "%PORTFOLIO%\信息可视化\京剧2.mp4" "peking-opera" "opera-2.mp4"
call :copy "%PORTFOLIO%\信息可视化\京剧3.mp4" "peking-opera" "opera-3.mp4"
call :copy "%PORTFOLIO%\京剧修改后.mp4" "peking-opera" "revised-full.mp4"
call :copy "%PORTFOLIO%\京剧修改后_1.mp4" "peking-opera" "revised-short.mp4"
call :copy "%REC%\2220048 秦艺榕 剧本视频.mp4" "campus-media" "script-video.mp4"
call :copy "%PORTFOLIO%\梨园.mp4" "campus-media" "liyuan-short.mp4"
call :copy "%REC%\2220048 秦艺榕 滚动的水滴_1.mp4" "c4d" "water-roll.mp4"
call :copy "%REC%\2220048 秦艺榕 钟摆_1.mp4" "c4d" "pendulum.mp4"
call :copy "%REC%\2220048 秦艺榕时钟.mp4" "c4d" "clock.mp4"
call :copy "%REC%\2220048 秦艺榕 路径动画_1.mp4" "c4d" "path-motion.mp4"
call :copy "%REC%\2220048 秦艺榕 小球变形_1.mp4" "c4d" "ball-morph.mp4"
call :copy "%REC%\2220048 秦艺榕 水滴滴落.mp4" "c4d" "water-drop.mp4"
call :copy "%REC%\2220048 秦艺榕 生长动画.mp4" "c4d" "growth.mp4"

echo.
echo 同步完成
dir /s /b "%DST%\*.mp4"
exit /b 0

:copy
if not exist "%~1" (
  echo SKIP %~3
  goto :eof
)
if not exist "%DST%\%~2" mkdir "%DST%\%~2"
copy /Y "%~1" "%DST%\%~2\%~3" >nul
echo OK %~2\%~3
goto :eof
