import numpy as np
import pandas as pd
from scipy.optimize import minimize
from ez_diffusion import ez_diffusion_model  # This function needs to be implemented
import sys

# Define the recovery function using the EZ diffusion model
def recover_parameters(data):
    """
    Recover parameters (a, v, t) using a fitting procedure.
    data: DataFrame containing simulated data (response times and accuracy)
    """
    def negative_log_likelihood(params):
        """
        Compute negative log-likelihood for the EZ diffusion model given parameters.
        params: [a, v, t] - model parameters
        """
        a, v, t = params
        
        # Ensure parameters are within a reasonable range
        if not (0.5 <= a <= 2) or not (0.5 <= v <= 2) or not (0.1 <= t <= 0.5):
            return np.inf  # Penalize invalid parameters
        
        # Simulate model prediction for response time and accuracy using EZ model
        simulated_data = ez_diffusion_model(a, v, t, data['N'])
        
        # Calculate the negative log likelihood based on simulated vs actual data
        likelihood = -np.sum(np.log(simulated_data))
        return likelihood

    # Initialize parameter guesses
    initial_guess = [1.0, 1.0, 0.3]  # a, v, t (based on given ranges)

    # Perform the optimization to recover parameters
    result = minimize(negative_log_likelihood, initial_guess, bounds=[(0.5, 2), (0.5, 2), (0.1, 0.5)])

    # If the optimization is successful, return the estimated parameters
    if result.success:
        return result.x  # The recovered parameters [a, v, t]
    else:
        raise ValueError("Parameter recovery failed!")

def main(input_file, output_file):
    """
    Main function to read the input simulated data, recover parameters, and save the results.
    input_file: Path to the CSV file containing the simulated data
    output_file: Path to save the recovered parameters
    """
    # Load the simulated data
    try:
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        sys.exit(f"Error: The file {input_file} was not found.")
    
    recovered_params = []

    # Recover parameters for each simulation in the dataset
    for index, row in data.iterrows():
        try:
            params = recover_parameters(row)
            recovered_params.append(params)
        except ValueError:
            recovered_params.append([np.nan, np.nan, np.nan])  # In case recovery fails

    # Save the recovered parameters to a new CSV file
    recovered_df = pd.DataFrame(recovered_params, columns=["a_recovered", "v_recovered", "t_recovered"])
    recovered_df.to_csv(output_file, index=False)
    print(f"Recovered parameters saved to {output_file}")

if __name__ == "__main__":
    # Command line interface: provide input and output file paths
    if len(sys.argv) != 3:
        print("Usage: python recover.py <input_file.csv> <output_file.csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
