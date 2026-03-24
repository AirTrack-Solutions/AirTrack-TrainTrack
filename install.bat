@echo off
echo.
echo  ================================================
echo   AirTrack Solutions - First Time Setup
echo   TrainTrack
echo  ================================================
echo.
echo  This will build and start TrainTrack for the first time.
echo  This may take several minutes. Please be patient.
echo.
pause
echo.
echo  Building TrainTrack...
docker compose -f docker-compose.client.yml up --build -d
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Setup failed.
    echo  Make sure Docker Desktop is installed and running, then try again.
    echo.
    pause
    exit /b 1
)
echo.
echo  ================================================
echo   Setup complete! TrainTrack is running.
echo   Open your browser and go to:
echo   http://localhost:5001
echo  ================================================
echo.
start http://localhost:5001
pause
