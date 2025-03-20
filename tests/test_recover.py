import pytest
import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.recover import recover_parameters

#Disclaimer: Code in this file was produced with the assistance of ChatGPT and ClaudeAI

# Test 1: Check if recover_parameters works with valid input
def test_recover_parameters_valid_input():
    # Simulate some data for testing
    simulated_data = pd.DataFrame({
        "RT": np.random.rand(10) + 0.5,  # Random response times
        "Accuracy": np.random.choice([0, 1], size=10),  # Random accuracy values
        "N": 10  # Example sample size
    })

    # Call the recovery function
    recovered_params = recover_parameters(simulated_data.iloc[0])

    # Check if the recovered parameters are within reasonable bounds
    assert 0.5 <= recovered_params[0] <= 2  # a (boundary separation)
    assert 0.5 <= recovered_params[1] <= 2  # v (drift rate)
    assert 0.1 <= recovered_params[2] <= 0.5  # t (non-decision time)

# Test 2: Check if recover_parameters handles invalid data (e.g., invalid parameters)
def test_recover_parameters_invalid_data():
    # Create invalid data with parameters out of bounds (e.g., RT < 0)
    invalid_data = pd.DataFrame({
        "RT": np.random.rand(10) - 1.0,  # Negative response times (invalid)
        "Accuracy": np.random.choice([0, 1], size=10),
        "N": 10
    })
    
    # Call the recovery function and check for NaN or failure
    try:
        recovered_params = recover_parameters(invalid_data.iloc[0])
        assert np.isnan(recovered_params[0])  # If recovery fails, return NaN
    except ValueError:
        pass  # Expecting an exception

# Test 3: Check if recover.py handles missing data correctly (returns NaN if recovery fails)
def test_recover_parameters_missing_data():
    # Simulate data with missing values in RT or Accuracy
    missing_data = pd.DataFrame({
        "RT": [np.nan] * 10,  # Missing RT values
        "Accuracy": [1] * 10,  # Valid accuracy
        "N": 10
    })

    # Call the recovery function and ensure NaN values are handled
    recovered_params = recover_parameters(missing_data.iloc[0])

    # Check if the recovery returns NaN for parameters when input data is missing
    assert np.isnan(recovered_params[0])  # Should be NaN if recovery fails

