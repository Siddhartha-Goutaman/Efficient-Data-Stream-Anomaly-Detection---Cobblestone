import numpy as np
import time
import matplotlib.pyplot as plt
from collections import deque

def generate_data_stream(n=1000, noise_level=0.1, anomaly_prob=0.01):
    # seasonality in data is simulated here using a sine wave
    base_pattern = np.sin(np.linspace(0, 20 * np.pi, n))
    
    # random noise
    noisy_pattern = base_pattern + noise_level * np.random.randn(n)
    
    # anomalies are introduced randomly
    for i in range(n):
        if np.random.rand() < anomaly_prob:
            noisy_pattern[i] += np.random.uniform(-5, 5)  # Random anomaly spikes
    
    return noisy_pattern

# simulate real-time streaming
def stream_data(data, delay=0.1):
    for value in data:
        yield value
        time.sleep(delay)  # to simulate a delay


def detect_anomalies(data_stream, window_size=50, threshold=3):
    window = deque(maxlen=window_size)
    for data_point in data_stream:
        window.append(data_point)
        if len(window) == window_size:
            mean = np.mean(window)
            std = np.std(window)
            if std != 0:
                z_score = (data_point - mean) / std
            else:
                z_score = 0
            if abs(z_score) > threshold: #if datapoint is > 3*standard deviation, flag anomaly (print it)
                print(f"Anomaly Detected: {data_point}")
            yield data_point, mean, std, z_score

def live_plot(data_stream):
    plt.ion()  
    fig, ax = plt.subplots()
    data_points = []
    for data, mean, std, z_score in data_stream:
        data_points.append(data)
        ax.clear()
        ax.plot(data_points, label='Data Stream')
        ax.axhline(mean, color='green', label='Mean')
        ax.fill_between(range(len(data_points)), mean-3*std, mean+3*std, color='red', alpha=0.3) #what is considered as non-anomaly data
        plt.draw()
        plt.pause(0.01)  # pausing for update

def detect_anomalies_ewma(data_stream, alpha=0.1, threshold=2):
    ewma = None
    for data_point in data_stream:
        if ewma is None:
            ewma = data_point  # Initialize EWMA with the first data point
        else:
            ewma = alpha * data_point + (1 - alpha) * ewma  

        deviation = abs(data_point - ewma)
        
        # flag (print) anomaly if deviation is more than threshold
        if deviation > threshold:
            print(f"Anomaly Detected: {data_point} (Deviation: {deviation})")

        yield data_point, ewma, deviation


def live_plot_ewma(data_stream):
    plt.ion()
    fig, ax = plt.subplots()
    data_points = []
    
    line, = ax.plot([], [], label='Data Stream')
    ewma_line, = ax.plot([], [], color='green', label='EWMA (Smoothed)')
    ax.legend()
    
    for data, ewma, deviation in data_stream:
        data_points.append(data)
        ax.set_xlim(0, len(data_points))
        ax.set_ylim(min(data_points) - 1, max(data_points) + 1)

        
        line.set_data(range(len(data_points)), data_points)
        ewma_line.set_data(range(len(data_points)), [ewma for _ in data_points])
        
        plt.draw()
        plt.pause(0.01)  # pausing for update


live_plot_ewma(detect_anomalies_ewma(stream_data(generate_data_stream()))) #

# live_plot(detect_anomalies(stream_data(generate_data_stream())))
# UNCOMMENT THE ABOVE LINE TO VIEW PLOT WITH Z-SCORE METHOD OF ANOMALY DETECTION
