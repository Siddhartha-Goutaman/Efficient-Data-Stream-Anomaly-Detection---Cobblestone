# Efficient-Data-Stream-Anomaly-Detection---Cobblestone
Research project by Siddhartha Goutaman as part of job application to Cobblestone.

The project demanded the development of a Python script for anomaly detection in continuously streamed data - simulating real-time sequences of financial transactions or system metrics.

The project was successfully completed using 3 different algorithms and 2 methods for statistical calculations. 
The algorithms used in anomaly detection are:
  a. Z-score based detection
  b. EWMA (Exponentially Weight Moving Average) 
  c. ARIMA (Auto-Regressive Integrated Moving Average)

A more detailed explanation of the different methods is as follows
## Z-score based detection
This method makes use of the z-score which is a statistical measure that describes how far a particular data point is from the mean of the data, measured in standard deviations. It is calculated as: 

$`\frac{x-μ}{σ}`$

If the z-score is very high (or very low), it may indicate an anomaly, because the point is far from the expected normal range. Hence, using this method, we flag (or print) the data points that have deviation higher than a particular threshold (3σ) in the script provided.

## EWMA based detection
Unlike z-score, EWMA or Exponentially Weight Moving Average detects anomalies by giving higher weight on more recent data points, instead of relying on the mean or standard deviation directly. Thus this method works better in cases of recent changes. 

EWMA uses a smoothing factor α to control how much weight is given to recent observations vs. older observations. A lower α gives more weight to past values, while a higher α focuses more on recent values. 
EWMA is calculated with the formula:

$`EWMA = α * data + (1-α) EWMA(t-1)`$ , where EWMA(t-1) denotes the previous EWMA value.

Using this method, an anomaly if flagged(printed) if | EWMA - data | is greater than a set threshold.

### Why EWMA?

EWMA places more weight on recent data points, which makes it more adaptive to concept drift or changes in the data stream over time. Furthermore, it helps smooth out the random noise in the data, making it easier to detect significant deviations.

##


