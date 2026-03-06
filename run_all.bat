@echo off
echo Starting Cyber Safety Platform

echo Starting Backend API...
start "Backend Server" cmd /c "cd backend && python app.py"

echo Starting Frontend Server...
start "Frontend Server" cmd /c "cd frontend && python -m http.server 8000"

echo Opening Browser...
timeout /t 2 >nul
start http://localhost:8000/index.html
