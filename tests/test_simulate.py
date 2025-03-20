import pytest
import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.simulate import simulate_ez_diffusion

#Disclaimer: Code in this file was produced with the assistance of ChatGPT and ClaudeAI

# Test 1: Check if simulate_ez_diffusion runs without errors and returns a DataFrame
def test_simulate_ez_diffusion_basic():
    N = 100
    df = simulate_ez_diffusion(N)
    
    # Check if the returned result is a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Check if the DataFrame has the expected columns
    assert "RT" in df.columns
    assert "Accuracy" in df.columns

# Test 2: Check if the function handles a small sample size (e.g., N=1)
def test_simulate_ez_diffusion_small_sample():
    N = 1
    df = simulate_ez_diffusion(N)
    
    # Check that the returned result is still a DataFrame with 1 row
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1

# Test 3: Check if simulate_ez_diffusion works with a fixed random seed for reproducibility
def test_simulate_ez_diffusion_reproducibility():
    N = 100
    seed = 42
    df1 = simulate_ez_diffusion(N, seed)
    df2 = simulate_ez_diffusion(N, seed)
    
    # Check if the two outputs are the same when using the same seed
    pd.testing.assert_frame_equal(df1, df2)
