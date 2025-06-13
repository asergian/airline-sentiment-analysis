#!/bin/bash

# Exit on error
set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "OPENAI_API_KEY=" > .env
    echo "Please add your OpenAI API key to the .env file before running the experiment."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Run the experiment
echo "Running experiment..."
python experiment_runner.py \
    --experiment combined_v1 \
    --batch_size 1 \
    --test

# Deactivate virtual environment
deactivate

echo "Experiment completed!" 