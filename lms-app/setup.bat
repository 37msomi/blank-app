@echo off
REM LMS Setup Script for Windows

echo.
echo 🚀 Leave Management System - Setup Script
echo ==========================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✓ Node.js version:
node --version
echo ✓ npm version:
npm --version
echo.

REM Backend Setup
echo 📦 Setting up Backend...
cd backend

if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
)

echo Installing backend dependencies...
call npm install

echo ✓ Backend setup complete!
echo.

REM Frontend Setup
echo 📦 Setting up Frontend...
cd ..\frontend

if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
)

echo Installing frontend dependencies...
call npm install

echo ✓ Frontend setup complete!
echo.

REM Summary
echo.
echo ==========================================
echo ✅ Setup Complete!
echo ==========================================
echo.
echo 📝 Next Steps:
echo.
echo 1. Start PostgreSQL (Docker):
echo    docker-compose up -d
echo.
echo 2. Start Backend (from backend/ directory):
echo    npm run dev
echo.
echo 3. Start Frontend (from frontend/ directory):
echo    npm start
echo.
echo 4. Open browser and navigate to:
echo    http://localhost:3000
echo.
echo Demo Credentials:
echo   Employee: emp@test.com
echo   Manager:  mgr@test.com
echo   Admin:    admin@test.com
echo   Password: password (all accounts)
echo.
pause
