# Efficient Data Stream Anomaly Detection-Cobblestone
Research project by Siddhartha Goutaman as part of job application to Cobblestone.

The project demanded the development of a Python script for anomaly detection in continuously streamed data - simulating real-time sequences of financial transactions or system metrics.

The project was successfully completed using 3 different algorithms and 2 methods for statistical calculations. 
The algorithms used in anomaly detection are:
  1. Z-score based detection
  2. EWMA (Exponentially Weight Moving Average) 
  3. ARIMA (Auto-Regressive Integrated Moving Average)

A more detailed explanation of the different algorithms is as follows:

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

These two methods can be found in the ewma&z_score.py file. Please note that you have to comment out a line to see the z-score method in action.

### Why EWMA?

EWMA places more weight on recent data points, which makes it more adaptive to concept drift or changes in the data stream over time. Furthermore, it helps smooth out the random noise in the data, making it easier to detect significant deviations.

## ARIMA based detection

An Autoregressive Integrated Moving Average, or ARIMA, is a statistical analysis model that uses time series data to either better understand the data set or to predict future trends. A statistical model is autoregressive if it predicts future values based on past values. 
We train the ARIMA model as new data is streamed, and then make a prediction about what the next data should look like, based on the past trends. Then, this predicted value is compared with the streamed data point, and if it is over a particular threshold it is flagged (printed).

### Why ARIMA?

The ARIMA method is better in anomaly detection of time-series data due to its ability to handle temporal patterns and trends. The ARIMA method also makes use of a moving average, which captures the error in previous observations to forecast future values, which is beneficial for easily finding out deviations.

This comes with the cost of being computationally expensive, and hence the ARIMA method may not be as ideal as EWMA or Z-score in cases where real-time application of the identified data is crucial. Moreover, the parameters of the ARIMA model have to be tuned to perfection to fit a particular type of data stream.

This model can be found in the arima.py file.


## Statistical calculations

### Traditional calculation of mean and standard deviation of data

In this method, the mean and standard deviations are calculated each time for the data using the default mean and standard deviation functions in the numpy library of Python.

### Welford's method

Welford's algorithm is an algorithm used to compute mean and standard deviation in a single pass, in an incremental manner.
This makes the process more efficient than computing the mean and standard deviation each time for a particular set of data.

In the Welford's method, a recurrence relation is required between the quantities.
The recurrence relations for mean and variance are given as shown below:

$`\bar{x}_{n} = \bar{x}_{n-1} +\frac{x_{n}-\bar{x}_{n-1}}{n}`$

$`\sigma_{n}^{2} = \sigma_{n-1}^{2} + \frac{(x_{n}-\bar{x}_{n-1})(x_{n}-\bar{x}_{n})-\sigma^{2}_{n-1}}{n}`$

## Requirements

The scripts use minimum external libraries. Only a total of at most 5 libraries are used in the scripts, of which only 3 are external libraries which are - NumPy for calculation of statistical values, Matplotlib for visualisation of data and statsmodel for integration of ARIMA model in the anomaly detection. 

The libraries may be already installed in the system, since they are basic libraries used in data visualisation. In case they are not present, do install the libraries using the requirements.txt file by typing in the following command in your terminal.

``` pip install -r requirements.txt ```


