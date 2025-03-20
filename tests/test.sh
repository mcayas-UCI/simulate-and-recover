#!/bin/bash

echo "Running test_simulate.py..."
python test_simulate.py
simulate_exit_code=$?

echo -e "\nRunning test_recover.py..."
python test_recover.py
recover_exit_code=$?

# Check if any tests failed
if [ $simulate_exit_code -ne 0 ] || [ $recover_exit_code -ne 0 ]; then
    echo -e "\nOne or more tests failed!"
    exit 1
else
    echo -e "\nAll tests passed successfully!"
    exit 0
fi