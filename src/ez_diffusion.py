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

