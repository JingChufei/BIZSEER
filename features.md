- global features
- subsequence features

# global

- 参考 https://hctsa-users.gitbook.io/hctsa-manual/list-of-included-code-files

## 0. description 描述性

- 几点上升 几点下降
- 上升持续时间
- 几点平稳 均值多少
- 不了解机器学习的人也能知道是什么意思

## 1.Distribution 每个特征加一些说明性的东西 变大代表什么 变小代表什么

- ignore time-ordering

### max min

- 时间序列value的最大值和最小值

### percentage 分位数

- 可能会有异常值
- 1%
- 99%

### range

- max - min
- 99% - 1%

### median 50%

### Mean

### Variance

### skewness 偏度

- 衡量数据分布的对称性
- 绝对值越大 表示偏态越严重
  - 0 正态分布
  - 小于 0 左偏 尾巴在左
    - 均值 小于 中位数
  - 大于 0 右偏 尾巴在右
    - 均值 大于 中位数
    
![image](https://github.com/JingChufei/BIZSEER/blob/master/images/skewness.svg) 

### kurtosis 峰度

- 衡量数据分布的平坦度
  - 3 正态分布的峰度值
  - 小于 3 低峰 
  - 大于 3 尖峰 
- 一般计算为 峰度值 - 3

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/kurtosis.png)


## 2.Correlation 相关性

## AR 的 调整R方
- first order of autocorrelation 效果可能不好 都为比较大的值

### First order of autocorrelation

<img src="http://chart.googleapis.com/chart?cht=tx&chl=F_{5}=\operatorname{Corr}\left(x_{t}, x_{t-1}\right)" style="border:none;">

- 衡量 x_t 和 x_(t-1) 的线性相关性, x_(t-1) one-step lagged series, 例如 10:00-11:00 与 10:01-11:01
- 值越大, 表明 x_t越依赖过去的值, 表明time series的可预测性越大
- https://blog.csdn.net/huangfei711/article/details/78456165


## 3.Entropy 不确定性

- 用这些熵的加权作为一个特征值
- 或者选用在数据上表现最好的一个熵

### spectral entropy 谱熵

<img src="http://chart.googleapis.com/chart?cht=tx&chl=F_{1}=-\int_{-\pi}^{\pi} \hat{f}_{x}(\lambda) \log \hat{f}_{x}(\lambda) d \lambda" style="border:none;">

- 时间序列 x_t 的谱密度 f_x(lambda) 的 香农熵估计
- 评估信号的复杂度, 衡量一个time series的可预测性
- F1越大, 表明未来更多的不确定性, time series更难预测

### KL score
- KL divergence 定义为：一个time series中任意两个相距window的子序列分布的最大相对熵，其值越小，表示相距一个window的两个子序列的分布越相似

### Binned Entropy

- 对时间序列进行分桶操作
  - 将 [min(ts}, max(ts)]等分为10个区间, 计算每个区间时间序列取值的数量
- 计算这个概率分布的熵
- 值大 表示时间序列取值均匀分布在 min(ts) 和 max(ts) 之间
- 值小 表示时间序列取值集中在某一段

### Approximate Entropy (ApEn)

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Approximate%20Entropy.png)

### Sample Entropy (SampEn)

### Permutation Entropy (PermEn)

## 4.Stationarity 平稳性

- fixed and constant parameters throughout the recording 
- probability distributions over parameters that do not vary across the recording
- Measures of stationarity capture how temporal dependences vary over time

### Peak
峰 数量和位置

### Trough
谷 数量和位置

### StatAv

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/StatAv)

- the degree of non-stationarity
- does not change under translation or uniform scale reduction or enlargement
- smaller values imply more stationary time series 值越小 越平稳
- quantifies the tendency of the mean to vary with time
- the standard deviation is taken across the set of means computed in m non-overlapping windows of the time series, each of length w.

### Varience change
- ts.rolling(288).var().diff(periods=288).max()

### Lumpiness
- 结块性 块度 (将一个series分为24(1 hour 1 value)个观测block 消除daily seasonality, 先计算每个block的方差, 接着计算这些方差的方差)
- the variance of the variances of each window
- ts.rolling(288).var().var()

### Flat spots
- flat spot 把1个time series分为10个等宽区间 计算各区间的最大游程 dividing the sample space of a time series into ten equal-sized intervals, and computing the maximum run length within any single interval.
- max_run_length(pd.cut(ts, 10, include_lowest=True))

### Crossing points 
- 1个time series与平均线相交的次数
- 平均线 定义为 均值
- 并且我们想知道 穿过均值的位置, 即在什么时间穿过
- 另外 可以分时间段进行分析, 采用分段均值 比如 早上时段 下午时段 晚上时段等

### Optimal Box-Cox transformation parameter
![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Optimal%20Box-Cox%20transformation%20parameter.png)
- lambda值 (0, 1)
- 极大似然估计
- 一个好的lambda值, 使1个time series在整个series中的方差为常数
- 衡量1个time series的方差变化的程度


### Scaling
- capture the power-law scaling of time-series fluctuations over different timescales, as would be produced by a self-affine or fractal process
- quantifies long-range power law scaling of time-series fluctuations
- A stationary time series with long-range correlations can be interpreted as increments of a diffusion-like process and integrated (as a cumulative sum through time) to form a self-similar time series
- i.e., a time series that statistically resembles itself through rescaling in time. 
- from 2017-Feature-based time-series analysis [39][45][46]

## 5.Periodicity 周期性

- isSeason 是否为周期
- 周期是多少
- 可信度
  - 周期性强度
  - 傅立叶变换的实数部分

### Fourier transform 傅立叶变换

- 和业务强相关 只会有几个固定值 如 1天 1周 1月等
- allows a time series to be represented as a linear combination of frequency components
- each component given by:

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Fourier%20transform)

- from 2017-Feature-based time-series analysis

### wavelet decompositions

- wavelet basis set under variations in temporal scaling and translation
- to capture changes in, e.g., frequency content through time (using a Morlet wavelet)

### Strength of seasonality 周期性强度
<img src="http://chart.googleapis.com/chart?cht=tx&chl=F_{3}=1-\frac{\operatorname{var}\left(R_{t}\right)}{\operatorname{var}\left(x_{t}-T_{t}\right)}" style="border:none;">

- 衡量1个time series受周期性因素影响的程度

### Seasonal period 周期

- 衡量1个time series的周期性长度
- 月数据: F4 = 12
- 季度数据: F4 = 4
- 年数据: F4 = 1


## 6.Trend 趋势

- isTrend 是否有趋势 (可用cusum）
- 变化多少

<img src="http://chart.googleapis.com/chart?cht=tx&chl=F_{2}=1-\frac{\operatorname{var}\left(R_{t}\right)}{\operatorname{var}\left(x_{t}-S_{t}\right)}" style="border:none;">

### Strength of trend
- STL decomposition STL分解 将time series x_t 分解为 trend T_t, season S_t, remainder R_t
- 衡量1个time series的均值水平长期变化的程度
- 值越大, 表明1个time series的均值水平从长远来看会有越大的变化

### Level shift
- 连续24个观测block的最大均值差 the maximum difference in mean between consecutive blocks of 24 observations.
- ts.rolling(288).mean().diff(periods=288).max()

## 7.Nonlinear time-series analysis 非线性分析

- irregular behavior in a linear time series must be attributed to a stochastic external drive to the system
- An alternative explanation is that the system displays nonlinearity; 
- deterministic nonlinear equations can produce irregular (chaotic) dynamics which can be quantified using methods from the physics-based nonlinear time-series analysis literature
- These algorithms are typically based on a **phase space** reconstruction of the time series
- e.g., using the method of delays, and include measures of the Lyapunov exponent, correlation dimension, correlation entropy, and others
- from 2017-Feature-based time-series analysis



## 8.Time-series model fitting 

- 模型拟合的偏差
  - 过去作为训练集
  - 预测今天的时间序列 将偏差作为特征

- Many different types of features can be extracted from time-series models
  - the model parameters (e.g., the optimal α of an exponential smoothing model)
  - goodness of fit measures (e.g., as the autocorrelation of residuals).
- from 2017-Feature-based time-series analysis [7][8][6]

### exponential smoothing models

- makes predictions about future values of a time series using a weighted sum of its past values

### autoregressive models

### moving average models

### Gaussian process models

### Linearity
线性度


# subsequence

- 对今天的时间序列进行分段, 作为 shapelets 
- 与历史数据作对比 衡量相似性

## 1.Interval features

- some time-series classification problems may involve class differences in time-series properties that are restricted to specific discriminative **time intervals**
- Interval classifiers seek to learn the **location** of **discriminative subsequences** and the features that separate different classes

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Interval%20features.png)

## 2.Shapelets

- subsequences that are highly predictive of class differences
- determining subsequences, s, that best distinguish different classes of time series by their distance to the shapelet, d(s,x)
- minimum Euclidean distance across translation of the subsequence across the time series
- d(s,x), can be thought of as the ‘feature’ extracted from the time series

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Shapelets.png)

## 3.Pattern dictionaries

- shapelets cannot capture how many **times** a given subsequence is represented across an extended time-series recording
- Learning these discriminative patterns, and then characterizing each time series by the frequency of each pattern across the recording, provides useful information about **the frequency of discriminative subsequences** between classes of time series
- capturing stereotypical dynamic motifs
- judge pairs of time series as similar that contain similar frequencies of subsequence patterns

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Pattern%20dictionaries.png)


