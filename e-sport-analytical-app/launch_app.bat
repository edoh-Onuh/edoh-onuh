@echo off
title E-Sport Analytics App Launcher

echo ========================================
echo  E-Sport Analytics App Launcher
echo ========================================
echo.

echo Killing existing processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1
echo Done.
echo.

echo Starting Backend Server...
cd /d "c:\Users\adanu\OneDrive\Desktop\edoh_onuh_projects\Edoh-Onuh_Projects\e-sport-analytical-app\backend"
start "Backend Server" cmd /k "echo Starting Backend... && C:/Users/adanu/AppData/Local/Programs/Python/Python313/python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Starting Frontend Server...
cd /d "c:\Users\adanu\OneDrive\Desktop\edoh_onuh_projects\Edoh-Onuh_Projects\e-sport-analytical-app\frontend"
start "Frontend Server" cmd /k "echo Starting Frontend... && npm start"

echo.
echo ========================================
echo  Both servers are starting...
echo ========================================
echo  Backend:  http://127.0.0.1:8000
echo  Frontend: http://localhost:3000
echo  API Docs: http://127.0.0.1:8000/docs
echo ========================================
echo.

timeout /t 5 >nul
echo Opening browser in 5 seconds...
start http://localhost:3000

pause
