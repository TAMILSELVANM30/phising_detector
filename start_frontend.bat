@echo off
echo Starting Cyber Safety Platform Frontend on http://localhost:8000 ...
cd frontend
start http://localhost:8000/index.html
python -m http.server 8000
pause
