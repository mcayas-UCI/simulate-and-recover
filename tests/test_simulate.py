import sys
import os
import pytest
import numpy as np
import pandas as pd

# Add src/ to the Python path so that we can import simulate.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(simulate.py), '../src')))

from simulate import simulate_ez_diffusion

def test_output_format():
    """Test that the function returns a DataFrame with correct columns."""
    df = simulate_ez_diffusion(N=10, seed=42)
    expected_columns = {"RT", "Accuracy", "True_a", "True_v", "True_t"}
    assert isinstance(df, pd.DataFrame)
    assert expected_columns.issubset(df.columns)

def test_positive_rt():
    """Test that all reaction times (RT) are non-negative."""
    df = simulate_ez_diffusion(N=100, seed=42)
    assert (df["RT"] >= 0).all()

def test_accuracy_values():
    """Test that accuracy values are binary (0 or 1)."""
    df = simulate_ez_diffusion(N=100, seed=42)
    assert set(df["Accuracy"].unique()).issubset({0, 1})

def test_random_seed_reproducibility():
    """Test that using the same random seed produces identical outputs."""
    df1 = simulate_ez_diffusion(N=50, seed=123)
    df2 = simulate_ez_diffusion(N=50, seed=123)
    pd.testing.assert_frame_equal(df1, df2)

def test_different_seeds():
    """Test that different seeds produce different results."""
    df1 = simulate_ez_diffusion(N=50, seed=123)
    df2 = simulate_ez_diffusion(N=50, seed=456)
    assert not df1.equals(df2)

if __name__ == "__main__":
    pytest.main()

