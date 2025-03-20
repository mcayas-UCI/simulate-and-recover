import numpy as np
import pandas as pd
import sys
from scipy.optimize import minimize

#Disclaimer: Code in this file was produced with the assistance of ChatGPT and ClaudeAI

def recover_parameters(data):
    """
    Recover parameters (a, v, t) using a fitting procedure.
    :param data: DataFrame containing simulated data (RTs and accuracy)
    :return: Recovered parameter estimates [a, v, t]
    """

    def negative_log_likelihood(params):
        a, v, t = params
        if not (0.5 <= a <= 2) or not (0.5 <= v <= 2) or not (0.1 <= t <= 0.5):
            return np.inf  # Penalize invalid parameters
        
        # Compute predicted RT and accuracy
        expected_rt = a / v + t
        predicted_acc = 1 / (1 + np.exp(-2 * a * v))

        # Compute likelihood based on squared error
        rt_error = np.mean((data["RT"] - expected_rt) ** 2)
        acc_error = np.mean((data["Accuracy"] - predicted_acc) ** 2)
        
        return rt_error + acc_error  # Minimize error

    # Initial guesses for a, v, t
    initial_guess = [1.0, 1.0, 0.3]

    # Optimize parameters
    result = minimize(negative_log_likelihood, initial_guess, bounds=[(0.5, 2), (0.5, 2), (0.1, 0.5)])

    if result.success:
        return result.x  # The recovered parameters [a, v, t]
    else:
        raise ValueError("Parameter recovery failed!")

def main(input_file, output_file):
    """
    Reads the simulated data, recovers parameters, and saves the results.
    :param input_file: Path to the CSV file containing the simulated data
    :param output_file: Path to save the recovered parameters
    """
    try:
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        sys.exit(f"Error: The file {input_file} was not found.")
    
    try:
        recovered_params = recover_parameters(data)
        recovered_df = pd.DataFrame([recovered_params], columns=["a_recovered", "v_recovered", "t_recovered"])
    except ValueError:
        recovered_df = pd.DataFrame([[np.nan, np.nan, np.nan]], columns=["a_recovered", "v_recovered", "t_recovered"])

    # Save results
    recovered_df.to_csv(output_file, index=False)
    print(f"Recovered parameters saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python recover.py <input_file.csv> <output_file.csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
