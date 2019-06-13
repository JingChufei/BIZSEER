## Distribution

- ignore time-ordering

### Mean 均值

### Var 方差

### fits to distribution types

- e.g. Gaussian

### outliers


## Entropy

### spectral entropy 谱熵

<img src="http://chart.googleapis.com/chart?cht=tx&chl=F_{1}=-\int_{-\pi}^{\pi} \hat{f}_{x}(\lambda) \log \hat{f}_{x}(\lambda) d \lambda" style="border:none;">

- 时间序列 x_t 的谱密度 f_x(lambda) 的 香农熵估计
- 评估信号的复杂度, 衡量一个time series的可预测性
- F1越大, 表明未来更多的不确定性, time series更难预测

## stationary

- fixed and constant parameters throughout the recording 
- probability distributions over parameters that do not vary across the recording
- Measures of stationarity capture how temporal dependences vary over time

### StatAv

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/StatAv)

- a measure of mean stationarity
- the standard deviation is taken across the set of means computed in m non-overlapping windows of the time series, each of length w.
- 值越大 越平稳

## First order of autocorrelation

<img src="http://chart.googleapis.com/chart?cht=tx&chl=F_{5}=\operatorname{Corr}\left(x_{t}, x_{t-1}\right)" style="border:none;">

- 衡量 x_t 和 x_(t-1) 的线性相关性, x_(t-1) one-step lagged series, 例如 10:00-11:00 与 10:01-11:01
- 值越大, 表明 x_t越依赖过去的值, 表明time series的可预测性越大
- https://blog.csdn.net/huangfei711/article/details/78456165

## Fourier transform 傅立叶变换

- allows a time series to be represented as a linear combination of frequency components
- each component given by:

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Fourier%20transform)

## wavelet decompositions

- wavelet basis set under variations in temporal scaling and translation
- to capture changes in, e.g., frequency content through time (using a Morlet wavelet)

## Trend 趋势

<img src="http://chart.googleapis.com/chart?cht=tx&chl=F_{2}=1-\frac{\operatorname{var}\left(R_{t}\right)}{\operatorname{var}\left(x_{t}-S_{t}\right)}" style="border:none;">

- Strength of trend
- STL decomposition STL分解 将time series x_t 分解为 trend T_t, season S_t, remainder R_t
- 衡量1个time series的均值水平长期变化的程度
- 值越大, 表明1个time series的均值水平从长远来看会有越大的变化

## Season 周期性

### Strength of seasonality 周期性强度
<img src="http://chart.googleapis.com/chart?cht=tx&chl=F_{3}=1-\frac{\operatorname{var}\left(R_{t}\right)}{\operatorname{var}\left(x_{t}-T_{t}\right)}" style="border:none;">

- 衡量1个time series受周期性因素影响的程度

### Seasonal period 周期

- 衡量1个time series的周期性长度
- 月数据: F4 = 12
- 季度数据: F4 = 4
- 年数据: F4 = 1

## Linearity
线性度

## Curvature
曲率

## Peak
峰 数量和位置

## Trough
谷 数量和位置



## Lumpiness
结块性 块度 (将一个series分为24个观测block 消除daily seasonality, 先计算每个block的方差, 接着计算这些方差的方差)

## Spikiness
尖度 除了前两个principal component之外的components的交叉验证方差的方差 the variance of the leave-one-out variances of the remainder component.

## Lshift
level shift 连续24个观测block的最大均值差 the maximum difference in mean between consecutive blocks of 24 observations.

## Vchange
variance change 类似方差?

## Fspots
flat spot 把1个time series分为10个等宽区间 计算各区间的最大行程 dividing the sample space of a time series into ten equal-sized intervals, and computing the maximum run length within any single interval.

## Cpoints
crossing points 1个time series与平均线相交的次数

## KLscore
连续48个观测block的KL散度的最大差 the maximum difference in KL divergence (measured using kernel density estimation) between consecutive blocks of 48 observations.

## Change.idx
KL score的最大索引

## Optimal Box-Cox transformation parameter ?
![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Optimal%20Box-Cox%20transformation%20parameter.png)
- lambda值 (0, 1)
- 一个好的lambda值, 使1个time series在整个series中变化为常数
- 衡量1个time series的变化程度
