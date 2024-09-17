import numpy as np
import time
from collections import deque
import matplotlib.pyplot as plt

# generating the data stream
def generate_data_stream(n=1000, noise_level=0.1, anomaly_prob=0.01, noise_mean=0, noise_std=0.2):
    # seasonality in data is simulated here using a sine wave
    base_pattern = np.sin(np.linspace(0, 20 * np.pi, n))

    # random noise + added gaussian noise
    noisy_pattern = base_pattern + noise_level * np.random.randn(n) + np.random.normal(noise_mean,noise_std,n)

    # anomalies are introduced randomly
    for i in range(n):
        if np.random.rand() < anomaly_prob:
            noisy_pattern[i] += np.random.uniform(-5, 5) 
    return noisy_pattern

# simulate real-time streaming
def stream_data(data, delay=0.1):
    for value in data:
        yield value
        time.sleep(delay)  # to simulate a delay

# Welford's method - more optimised than calculating mean and sd in each step
class RollingStatistics:
    def __init__(self):
        self.n = 0
        self.mean = 0
        self.M2 = 0
    
    def update(self, new_value):
        self.n += 1
        delta = new_value - self.mean
        self.mean += delta / self.n
        delta2 = new_value - self.mean
        self.M2 += delta * delta2
    
    def get_mean(self):
        return self.mean
    
    def get_std(self):
        return np.sqrt(self.M2 / self.n) if self.n > 1 else 0


def detect_anomalies(data_stream, window_size=50, threshold=2):
    window = deque(maxlen=window_size)
    rolling_stats = RollingStatistics()
    
    for data_point in data_stream:
        window.append(data_point)
        rolling_stats.update(data_point)
        
        if len(window) == window_size:
            mean = rolling_stats.get_mean()
            std = rolling_stats.get_std()

            if std != 0:
                z_score = (data_point - mean) / std
            else:
                z_score = 0
            
            if abs(z_score) > threshold:
                print(f"Anomaly Detected: {data_point}") # if datapoint is > 2*standard deviation, flag anomaly (print it)
            yield data_point, mean, std, z_score


def live_plot(data_stream):
    plt.ion()
    fig, ax = plt.subplots()
    data_points = []
    
    line, = ax.plot([], [], label='Data Stream')
    mean_line = ax.axhline(0, color='green', label='Mean')
    fill = None
    ax.legend()

    for data, mean, std, z_score in data_stream:
        data_points.append(data)
        ax.set_xlim(0, len(data_points))
        ax.set_ylim(min(data_points) - 1, max(data_points) + 1)

        line.set_data(range(len(data_points)), data_points)
        mean_line.set_ydata(mean)
        
        if len(data_points) > 1:
            if fill:
                fill.remove()
            fill = ax.fill_between(range(len(data_points)), mean-2*std, mean+2*std, color='red', alpha=0.3) #what is considered as non-anomaly(normal) data
        
        plt.draw()
        plt.pause(0.01)  # pausing for update


live_plot(detect_anomalies(stream_data(generate_data_stream())))
