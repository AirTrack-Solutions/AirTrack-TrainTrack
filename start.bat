@echo off
echo.
echo  ================================================
echo   AirTrack Solutions - Starting TrainTrack
echo  ================================================
echo.
echo  Please wait while TrainTrack starts up...
echo.
docker compose -f docker-compose.client.yml up -d
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: TrainTrack failed to start.
    echo  Make sure Docker Desktop is running and try again.
    echo.
    pause
    exit /b 1
)
echo.
echo  ================================================
echo   TrainTrack is running!
echo   Open your browser and go to:
echo   http://localhost:5001
echo  ================================================
echo.
start http://localhost:5001
pause
