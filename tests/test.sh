#!/bin/bash

# Navigate to the directory where the tests are located (adjust the path if needed)
cd "$(dirname "$0")"

# Run pytest to execute the tests in the test_simulate.py file
pytest tests/test_simulate.py --maxfail=1 --disable-warnings -q
