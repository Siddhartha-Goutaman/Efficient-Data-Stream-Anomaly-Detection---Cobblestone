import numpy as np
import time
import matplotlib.pyplot as plt
from collections import deque
from statsmodels.tsa.arima.model import ARIMA

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
        time.sleep(delay)  

# using ARIMA to detect anomalies
def detect_anomalies_arima(data_stream, window_size=50, order=(1,1,1), threshold=2):
    window = deque(maxlen=window_size)
    
    for data_point in data_stream:
        window.append(data_point)
        
        if len(window) == window_size:
            # fitting the ARIMA model to the window
            window_array = np.array(window)
            try:
                model = ARIMA(window_array, order=order)
                model_fit = model.fit()  
                predicted_value = model_fit.forecast()[0]  # predict next value
                
                # calculate difference of predicted and actual value
                diff = abs(data_point - predicted_value)
                
                # flag(print) anomaly if difference is more than the threshold
                if diff > threshold:
                    print(f"Anomaly Detected: {data_point} (Residual: {diff})")
                
                yield data_point, predicted_value, diff
            except Exception as e:
                print(f"Error fitting ARIMA model: {e}")
                yield data_point, None, None

def live_plot_arima(data_stream):
    plt.ion()
    fig, ax = plt.subplots()
    data_points = []
    
    line, = ax.plot([], [], label='Data Stream')
    pred_line, = ax.plot([], [], color='green', label='ARIMA Prediction')
    ax.legend()
    
    for data, predicted, residual in data_stream:
        data_points.append(data)
        
        ax.set_xlim(0, len(data_points))
        ax.set_ylim(min(data_points) - 1, max(data_points) + 1)
        
        line.set_data(range(len(data_points)), data_points)
        
        if predicted is not None: # the predicted line is updated only if there is a valid prediction
            pred_line.set_data(range(len(data_points)), [predicted for _ in data_points])
        
        plt.draw()
        plt.pause(0.01)  # pausing for update

live_plot_arima(detect_anomalies_arima(stream_data(generate_data_stream())))