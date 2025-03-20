#!/bin/bash

# Get the absolute path to the project root
PROJECT_ROOT=$(pwd)

# Add the project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# Create output directories if they don't exist
mkdir -p results
mkdir -p figures

echo "Starting simulation and recovery process..."

# Step 1: Run simulation
echo "Running simulation..."
python $PROJECT_ROOT/simulate.py
simulate_exit_code=$?

if [ $simulate_exit_code -ne 0 ]; then
    echo "Simulation failed with exit code $simulate_exit_code. Aborting."
    exit 1
fi

echo "Simulation completed successfully."

# Step 2: Run recovery
echo "Running parameter recovery..."
python $PROJECT_ROOT/recover.py
recover_exit_code=$?

if [ $recover_exit_code -ne 0 ]; then
    echo "Recovery failed with exit code $recover_exit_code. Aborting."
    exit 1
fi

echo "Recovery completed successfully."

echo "Simulation and recovery process finished successfully."
exit 0