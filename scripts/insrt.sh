#!/bin/bash

# Set base directories
BASE_DIR=/opt/apps/insrt
VENV_DIR=$BASE_DIR/venv
LOGS_DIR=$BASE_DIR/resources/logs
SCRIPT_DIR=$BASE_DIR/scripts
SCRIPT_NAME=insrt.py

# Set environment variables
export VENV=$VENV_DIR
export LOGS_DIR=$LOGS_DIR

# Activate the virtual environment
if [ -f "$VENV/bin/activate" ]; then
    source "$VENV/bin/activate"
else
    echo "Virtual environment activation script not found."
    exit 1
fi

# Set PYTHONPATH
export PYTHONPATH=$BASE_DIR

# Change to the directory containing the Python script
cd "$BASE_DIR" || { echo "Directory not found."; exit 1; }

# Run the Python script
if command -v python &> /dev/null; then
    python "$SCRIPT_DIR/$SCRIPT_NAME" "$@"
else
    echo "Python command not found."
    exit 1
fi