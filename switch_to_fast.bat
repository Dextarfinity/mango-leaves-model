@echo off
echo 🚀 Switching to Fast Railway Deployment Configuration
echo ====================================================
echo.

echo 📋 Backing up current files...
if exist Dockerfile (
    copy Dockerfile Dockerfile.original >nul
    echo ✅ Backed up Dockerfile to Dockerfile.original
)

if exist requirements.txt (
    copy requirements.txt requirements.original.txt >nul
    echo ✅ Backed up requirements.txt to requirements.original.txt
)

echo.
echo 🔄 Switching to fast configuration...

if exist Dockerfile.fast (
    copy Dockerfile.fast Dockerfile >nul
    echo ✅ Using Dockerfile.fast as Dockerfile
) else (
    echo ❌ Dockerfile.fast not found!
    pause
    exit /b 1
)

if exist requirements.fast.txt (
    copy requirements.fast.txt requirements.txt >nul
    echo ✅ Using requirements.fast.txt as requirements.txt
) else (
    echo ❌ requirements.fast.txt not found!
    pause
    exit /b 1
)

echo.
echo 🎉 Fast configuration activated!
echo.
echo 📝 What changed:
echo   • Dockerfile now uses ultralytics/ultralytics base image
echo   • requirements.txt has minimal dependencies
echo   • Build time should be 2-3 minutes instead of 10+ minutes
echo.
echo 📤 Next steps:
echo 1. Commit changes: git add . && git commit -m "Switch to fast build"
echo 2. Push to GitHub: git push
echo 3. Redeploy on Railway
echo.
echo 🔙 To revert: run revert_to_original.bat
echo.
pause