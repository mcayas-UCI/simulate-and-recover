import numpy as np
import pandas as pd
from scipy.optimize import minimize

import numpy as np

def ez_diffusion_model(a, v, t, N):
    """
    Simulates data for the EZ diffusion model.
    
    Parameters:
    - a: boundary separation (a float between 0.5 and 2)
    - v: drift rate (a float between 0.5 and 2)
    - t: nondecision time (a float between 0.1 and 0.5)
    - N: number of trials (int, the sample size)

    Returns:
    - response_times: Simulated response times
    - accuracies: Simulated accuracies (correct or incorrect responses)
    """
    # Simulate the response times and accuracies for N trials
    response_times = []
    accuracies = []

    for _ in range(N):
        # Generate random drift rate for each trial
        drift = np.random.normal(v, 0.2)  # assuming a small variability around v
        
        # Simulate response time: crossing the boundary a
        time_to_boundary = a / drift
        
        # Simulate non-decision time
        response_time = time_to_boundary + t
        
        # Simulate whether the response was correct or incorrect
        # A simple model: if drift rate is positive, the response is correct
        accuracy = 1 if drift > 0 else 0
        
        response_times.append(response_time)
        accuracies.append(accuracy)
    
    return np.array(response_times), np.array(accuracies)

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
