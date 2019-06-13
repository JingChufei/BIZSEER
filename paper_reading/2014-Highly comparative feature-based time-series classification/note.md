# Abstract

# Keywords

# 1.Introduction

- Two main challenges of time-series classification are typically: 
  - (i) selecting an appropriate **representation** of the time series, and 
  - (ii) selecting a suitable measure of dissimilarity or **distance** between time series
  
- categories
  - instance-based
    - time series encode meaningful patterns that need to be compared, new time series can be classified by matching them to similar instances of time series with a known classification
  - feature-based
    - transforming time-series objects of any length into short vectors
    
![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Differences%20between%20instance-based%20and%20feature-based.png)
    
- highly comparative
  - automate the selection of features by computing thousands of features, and then selecting those with the best performance. 
  - The classifier is thus selected according to the **structure of the data**, with different features selected for different types of problems
  
# 2.Data and Method

# 2.1 Data

- 20 data sets from UCR [15] 
- each data set are of **labeled**, **univariate** time series and all time series in each data set have the **same length**
- without any preprocessing and using the specified partitions of each data set into training and test portions

# 2.2 Feature Vector Representation

- operation
  - input: a time seires x = (x1, x2, ..., xn)
  - output: a feature value
  
### over 9,000 operations developed in previous work [4]

- basic statistics of the distribution of time series values 
  - (e.g., location, spread, Gaussianity, outlier properties)
- linear correlations 
  - (e.g., autocorrelations, features of the power spectrum)
- stationarity 
  - (e.g., StatAv, sliding window measures, prediction errors)
- information theoretic and entropy/complexity measures 
  - (e.g., automutual information, Approximate Entropy, Lempel-Ziv complexity)
- methods from the physical nonlinear time series analysis literature 
  - (e.g., correlation dimension, Lyapunov exponent estimates, surrogate data analysis)
- linear and nonlinear model fits 
  - [e.g., goodness of fit estimates and parameter values from autoregressive moving average (ARMA), Gaussian Process, and generalized autoregressive conditional heteroskedasticity (GARCH) models]
- others 
  - (e.g., wavelet methods, properties of networks derived from time series, etc.)
  
many groups of operations result from using **different input parameters** to the same type of time series method

The Matlab code for all the operations used in this work can be explored and downloaded at **www.compengine.org/timeseries**.




