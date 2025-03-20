#!/bin/bash

# Get the absolute path to the project root
PROJECT_ROOT=$(pwd)

# Add the project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# Create output directories if they don't exist
mkdir -p results
mkdir -p figures

echo "Starting simulation and recovery process..."

# Configuration parameters
N=3000  # Number of iterations/samples
SIMULATION_OUTPUT="results/simulation_data.npz"  # Output file for simulation results
RECOVERY_OUTPUT="results/recovered_parameters.csv"  # Output file for recovery results
SEED=42  # Random seed for reproducibility

# Step 1: Run simulation with required arguments
echo "Running simulation with N=$N..."
python $PROJECT_ROOT/simulate.py -N $N -o $SIMULATION_OUTPUT -s $SEED
simulate_exit_code=$?

if [ $simulate_exit_code -ne 0 ]; then
    echo "Simulation failed with exit code $simulate_exit_code. Aborting."
    exit 1
fi

echo "Simulation completed successfully. Results saved to $OUTPUT"

# Step 2: Run recovery
# Assuming recover.py may need the simulation output as input
echo "Running parameter recovery..."
python $PROJECT_ROOT/recover.py $SIMULATION_OUTPUT $RECOVERY_OUTPUT
recover_exit_code=$?

if [ $recover_exit_code -ne 0 ]; then
    echo "Recovery failed with exit code $recover_exit_code. Aborting."
    exit 1
fi

echo "Recovery completed successfully."

echo "Simulation and recovery process finished successfully."
exit 0