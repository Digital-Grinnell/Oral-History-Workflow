#!/bin/bash
# Run script for Oral History Workflow App
# This script automatically sets up the virtual environment if needed and runs the app

# Change to the script's directory
cd "$(dirname "$0")"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating .venv..."
    echo ""
    
    python3 -m venv .venv
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
    
    echo "Installing dependencies..."
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
    
    echo ""
    echo "Setup complete!"
    echo ""
fi

# Check if requirements are up to date
if [ requirements.txt -nt .venv/bin/activate ]; then
    echo "Dependencies may be outdated. Installing/updating..."
    .venv/bin/pip install --upgrade -r requirements.txt
    echo ""
fi

# Run the app
echo "Starting Oral History Workflow App..."
echo ""
.venv/bin/python main.py
