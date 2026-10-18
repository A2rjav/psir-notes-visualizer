@echo off
title PSIR Notes Visualizer Web App
echo ===================================================
echo   Starting PSIR 6-Volume Digital Web App...
echo ===================================================
echo.
cd /d "%~dp0app"
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)
echo Launching Vite development server on http://localhost:5173 ...
echo.
start http://localhost:5173
npx vite --host 127.0.0.1 --port 5173
pause
