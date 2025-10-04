@echo off
echo 🩺 Fixing Railway Health Check Issues
echo =====================================
echo.

echo 📋 The issue: Railway health checks are failing
echo 💡 The solution: Fix port binding and startup errors
echo.

echo 🔧 Applying fixes...

echo ✅ 1. Updated Dockerfile for better port handling
echo ✅ 2. Enhanced main.py with error handling
echo ✅ 3. Simplified railway.toml configuration
echo ✅ 4. Added debug endpoints

echo.
echo 📤 Next steps:
echo 1. Commit these fixes: git add . && git commit -m "Fix health check issues"
echo 2. Push to GitHub: git push
echo 3. Redeploy on Railway
echo.

echo 🔍 What was fixed:
echo   • Port binding uses Railway's PORT environment variable
echo   • Health endpoint has better error handling
echo   • Startup doesn't crash if model fails to load
echo   • More verbose logging for debugging
echo.

echo 📊 Expected result:
echo   • Build time: ~2-3 minutes ✅
echo   • Health check: Should pass ✅
echo   • API endpoints: All working ✅
echo.

echo 🆘 If health checks still fail:
echo   1. Check Railway logs for specific errors
echo   2. Try the debug configuration (Dockerfile.debug)
echo   3. Use debug_app.py for minimal testing
echo.

pause