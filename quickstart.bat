@echo off
echo ========================================
echo AI Incident Commander - Quick Start
echo ========================================
echo.

REM Check if setup was run
if not exist "backend\venv" (
    echo [WARNING] Setup not detected. Running setup first...
    echo.
    call setup.bat
    if errorlevel 1 (
        echo [ERROR] Setup failed. Please check the errors above.
        pause
        exit /b 1
    )
    echo.
)

REM Load demo data
echo Checking demo data...
cd backend
call venv\Scripts\activate.bat
python seed_data.py 2>nul
cd ..

echo.
echo ========================================
echo Starting AI Incident Commander...
echo ========================================
echo.
echo This will open 2 command windows:
echo   1. Backend API server (http://localhost:8000)
echo   2. Frontend web app (http://localhost:3000)
echo.
echo Close both windows to stop the application
echo.
timeout /t 3 >nul

REM Start backend in new window
echo Starting backend...
start "AI Commander - Backend" cmd /k "cd backend && venv\Scripts\activate && python run.py"

REM Wait for backend
echo Waiting for backend to start...
timeout /t 5 >nul

REM Start frontend in new window
echo Starting frontend...
start "AI Commander - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo AI Incident Commander is running!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/api/docs
echo.
echo Close the command windows to stop
echo.
pause
