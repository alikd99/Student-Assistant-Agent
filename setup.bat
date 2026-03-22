@echo off
chcp 65001 >nul
title Setup - Student Assistant
cd /d "%~dp0"

echo.
echo ============================================================
echo        Student Assistant - First Time Setup
echo ============================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found.
    echo Install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)
echo [OK] Python found.

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found.
    echo Install Node.js LTS from https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js found.

echo.
echo [0/4] Checking Tesseract OCR...
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Tesseract not found. Downloading installer...
    curl -L -o tesseract_installer.exe "https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe"
    echo Installing Tesseract silently (admin required)...
    tesseract_installer.exe /S "/D=C:\Program Files\Tesseract-OCR"
    del tesseract_installer.exe
    setx PATH "%PATH%;C:\Program Files\Tesseract-OCR" >nul 2>&1
    echo [OK] Tesseract installed. You may need to restart your PC if OCR fails.
) else (
    echo [OK] Tesseract found.
)

echo.
echo [1/4] Creating Python virtual environment...
if not exist ".venv" python -m venv .venv
echo [OK] Virtual environment ready.

echo.
echo [2/4] Installing Python dependencies (this may take a few minutes)...
.venv\Scripts\pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies.
    pause
    exit /b 1
)
echo [OK] Python dependencies installed.

echo.
echo [3/4] Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies.
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Frontend dependencies installed.

echo.
echo [4/4] Setting up configuration...
if not exist ".env" (
    echo API_BASE=http://localhost:8000 > .env
    echo LLM_PROVIDER=lmstudio >> .env
    echo LMSTUDIO_URL=https://api.groq.com/openai/v1 >> .env
    echo GROQ_API_KEY= >> .env
    echo LLM_MODEL=llama-3.3-70b-versatile >> .env
    echo [OK] .env file created.
) else (
    echo [OK] .env file already exists.
)

echo.
echo ============================================================
echo   Setup complete! Run start.bat to launch the app.
echo ============================================================
echo.
pause
