#!/bin/bash

# Log file path
LOG_FILE="/home/pi/gui_startup.log"

# Start logging
echo "Script started at $(date)" > $LOG_FILE

# Navigate to the backend project directory
echo "Navigating to backend directory" >> $LOG_FILE
cd /home/pi/Documents/fpy/Final-Year-Project-Personalised-Learning-Device-Using-Generative-AI/App/Backend || { echo "Failed to navigate to backend directory" >> $LOG_FILE; exec $SHELL; }

# Activate the Python virtual environment if applicable
echo "Activating virtual environment" >> $LOG_FILE
source /home/pi/Documents/fpy/Final-Year-Project-Personalised-Learning-Device-Using-Generative-AI/fypvirtenv/bin/activate || { echo "Failed to activate virtual environment" >> $LOG_FILE; exec $SHELL; }

# Start the backend in the background
echo "Starting backend" >> $LOG_FILE
python3 main.py >> $LOG_FILE 2>&1 &
BACKEND_PID=$!

# Check if the backend started successfully
if ps -p $BACKEND_PID > /dev/null; then
    echo "Backend started successfully with PID $BACKEND_PID" >> $LOG_FILE
else
    echo "Backend failed to start" >> $LOG_FILE
    exec $SHELL
fi

# Navigate to the frontend project directory
echo "Navigating to frontend directory" >> $LOG_FILE
cd /home/pi/Documents/fpy/Final-Year-Project-Personalised-Learning-Device-Using-Generative-AI/App/GUI || { echo "Failed to navigate to frontend directory" >> $LOG_FILE; exec $SHELL; }

# Source the .bashrc or other relevant profile script to ensure environment variables are set
echo "Sourcing .bashrc" >> $LOG_FILE
source /home/pi/.bashrc

# Set the PATH explicitly for Node.js and npm
export PATH="/home/pi/.nvm/versions/node/v20.12.2/bin:$PATH"

# Print the node and npm versions to ensure they are available
echo "Node version: $(node -v)" >> $LOG_FILE
echo "NPM version: $(npm -v)" >> $LOG_FILE

# Run npm start and log output and errors
echo "Running npm start" >> $LOG_FILE
npm start >> $LOG_FILE 2>&1

# Check the status of npm start
if [ $? -ne 0 ]; then
    echo "npm start failed" >> $LOG_FILE
else
    echo "npm start succeeded" >> $LOG_FILE
fi

# Keep the terminal open
echo "Script ended at $(date)" >> $LOG_FILE
exec $SHELL