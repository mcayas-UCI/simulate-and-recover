import numpy as np
import pandas as pd
import argparse

#Disclaimer: Code in this file was produced with the assistance of ChatGPT and ClaudeAI

# Function to simulate RTs and accuracy using the EZ diffusion model
def simulate_ez_diffusion(N, seed=None):
    """
    Simulates reaction time (RT) and accuracy data based on the EZ diffusion model.

    Parameters:
        N (int): Number of trials (sample size)
        seed (int, optional): Random seed for reproducibility

    Returns:
        pd.DataFrame: Simulated data containing RTs and accuracy
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Randomly sample parameters within given ranges
    a = np.random.uniform(0.5, 2)     # Boundary separation
    v = np.random.uniform(0.5, 2)     # Drift rate
    t = np.random.uniform(0.1, 0.5)   # Non-decision time
    
    # Compute mean RT and accuracy based on EZ diffusion equations
    expected_rt = a / v + t
    accuracy = 1 / (1 + np.exp(-2 * a * v))  # Sigmoid function for accuracy
    
    # Generate N reaction times with some variability
    rt_variability = np.random.normal(loc=0, scale=0.1, size=N)  # Small variability
    rts = np.clip(expected_rt + rt_variability, a_min=0, a_max=None)  # Ensure RT >= 0
    
    # Generate binary accuracy values (1=correct, 0=error) based on probability
    accuracies = np.random.binomial(1, accuracy, size=N)
    
    # Store results in a DataFrame
    df = pd.DataFrame({
        "RT": rts,
        "Accuracy": accuracies,
        "True_a": a,
        "True_v": v,
        "True_t": t
    })
    
    return df

# Main function to handle command-line execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate EZ diffusion model data.")
    parser.add_argument("-N", type=int, required=True, help="Sample size (number of trials)")
    parser.add_argument("-o", "--output", type=str, default="results/simulated_data.csv", help="Output CSV file")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Random seed for reproducibility")

    args = parser.parse_args()

    # Run simulation
    simulated_data = simulate_ez_diffusion(N=args.N, seed=args.seed)

    # Save to CSV
    simulated_data.to_csv(args.output, index=False)
    
    print(f"Simulated data (N={args.N}) saved to {args.output}")
