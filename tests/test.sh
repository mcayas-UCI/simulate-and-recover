#!/bin/bash

echo "Running all tests..."

# Run unit and integration tests using pytest
pytest test/test_simulate.py

# Check if simulate.py executes without crashing
echo "Testing simulate.py execution..."
python3 src/simulate.py --test-mode

if [ $? -ne 0 ]; then
    echo "simulate.py encountered an error!"
    exit 1
fi

echo "All tests passed!"
exit 0
