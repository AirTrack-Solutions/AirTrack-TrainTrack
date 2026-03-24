#!/bin/bash
echo ""
echo " ================================================"
echo "  AirTrack Solutions - First Time Setup"
echo "  TrainTrack"
echo " ================================================"
echo ""
echo " This will build and start TrainTrack for the first time."
echo " This may take several minutes. Please be patient."
echo ""
read -p " Press Enter to continue..."
echo ""
echo " Building TrainTrack..."
docker compose -f docker-compose.client.yml up --build -d
if [ $? -ne 0 ]; then
    echo ""
    echo " ERROR: Setup failed."
    echo " Make sure Docker is installed and running, then try again."
    echo ""
    exit 1
fi
echo ""
echo " ================================================"
echo "  Setup complete! TrainTrack is running."
echo "  Open your browser and go to:"
echo "  http://localhost:5001"
echo " ================================================"
echo ""
