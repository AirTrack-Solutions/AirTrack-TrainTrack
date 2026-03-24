@echo off
echo.
echo  ================================================
echo   AirTrack Solutions - Stopping TrainTrack
echo  ================================================
echo.
docker compose -f docker-compose.client.yml down
echo.
echo  TrainTrack has been stopped.
echo.
pause
