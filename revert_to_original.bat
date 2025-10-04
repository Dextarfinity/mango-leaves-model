@echo off
echo 🔙 Reverting to Original Railway Configuration
echo ==============================================
echo.

if exist Dockerfile.original (
    copy Dockerfile.original Dockerfile >nul
    echo ✅ Restored original Dockerfile
) else (
    echo ⚠️  No Dockerfile.original found
)

if exist requirements.original.txt (
    copy requirements.original.txt requirements.txt >nul
    echo ✅ Restored original requirements.txt
) else (
    echo ⚠️  No requirements.original.txt found
)

echo.
echo ✅ Reverted to original configuration
echo.
echo 📝 You're now back to the full build configuration
echo   • Longer build time but more control
echo   • All original dependencies restored
echo.
pause