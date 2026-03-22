@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Student Assistant

echo.
echo ============================================================
echo        Student Assistant - Starting...
echo ============================================================
echo.

if not exist ".venv" (
    echo ERROR: Run setup.bat first.
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo ERROR: Run setup.bat first.
    pause
    exit /b 1
)

echo Checking API key...
.venv\Scripts\python.exe check_key.py
if %errorlevel% neq 0 (
    pause
    exit /b 1
)

echo.
echo Starting backend...
start "Backend" cmd /k "%~dp0_run_backend.bat"

echo Waiting for backend...
:WAIT
.venv\Scripts\python.exe -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/documents', timeout=2)" >nul 2>&1
if %errorlevel% neq 0 (
    timeout /t 2 /nobreak >nul
    goto WAIT
)
echo Backend is ready.

echo Starting frontend...
start "Frontend" cmd /k "%~dp0_run_frontend.bat"

timeout /t 4 /nobreak >nul
echo.
echo App running at http://localhost:5173
echo.
start http://localhost:5173
