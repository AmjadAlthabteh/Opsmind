@echo off
echo ========================================
echo AI Incident Commander - Setup Script
echo ========================================
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11 or higher.
    exit /b 1
)
echo [OK] Python detected

REM Check Node.js
echo.
echo Checking Node.js version...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 18 or higher.
    exit /b 1
)
echo [OK] Node.js detected

REM Setup backend
echo.
echo Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate and install
echo Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Create .env
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo [WARNING] Edit backend\.env and add your OPENAI_API_KEY
    echo           (Optional - AI features work in demo mode without it)
)

cd ..

REM Setup frontend
echo.
echo Setting up frontend...
cd frontend

echo Installing Node.js dependencies...
call npm install

cd ..

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. (Optional) Add your OpenAI API key to backend\.env
echo    Without it, the system runs with demo AI responses
echo.
echo 2. Load demo data:
echo    cd backend
echo    python seed_data.py
echo.
echo 3. Start the servers (in separate command prompts):
echo    Terminal 1: cd backend ^&^& python run.py
echo    Terminal 2: cd frontend ^&^& npm run dev
echo.
echo 4. Open http://localhost:3000 in your browser
echo.
echo For more info, see README.md
echo.
pause
