@echo off
echo.
echo ===================================
echo  E-Sport Analytics Platform Setup
echo ===================================
echo.

echo [1/5] Setting up Python backend...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo [2/5] Setting up Node.js frontend...
cd ..\frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo [3/5] Generating sample data...
cd ..\backend
python populate_data.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate sample data
    pause
    exit /b 1
)

echo [4/5] Testing backend API...
python test_api.py
if %errorlevel% neq 0 (
    echo WARNING: API test failed, but continuing...
)

echo [5/5] Setup complete!
echo.
echo ===================================
echo  🎮 Ready to run! 🎮
echo ===================================
echo.
echo To start the application:
echo   Backend:  cd backend ^&^& python run_server.py
echo   Frontend: cd frontend ^&^& npm start
echo.
echo Or use VS Code tasks for easier development!
echo.
pause
