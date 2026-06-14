@echo off
set "GIT=C:\Program Files\Git\bin\git.exe"
set "ROOT=%~dp0"
cd /d "%ROOT%"

echo Pushing videos with Git LFS...
"%GIT%" lfs install
"%GIT%" add .gitattributes assets/videos scripts/sync-videos.py scripts/sync-videos.ps1 sync-videos.bat videos/ index.html
"%GIT%" diff --cached --quiet
if errorlevel 1 "%GIT%" commit -m "Add portfolio videos from desktop via Git LFS"
"%GIT%" push origin main
"%GIT%" lfs push origin main --all
echo Done.
