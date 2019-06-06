# 摘要
- 识别异常(unusual or anomalous)的time series
- 构造 每个time series 的特征向量(包括lag correlation, strength of seasonality, spectral entropy等)
- 用 PCA(principal component decomposition) 对特征进行降维, 在前两个 principal component 上用 基于α-hulls的二变量异常识别算法 识别异常
# 关键字
- Feature Space
- Time Series Characteristics
- Multivariate Anomaly Detection
- Outliers
# Approach
- 在 m 个 time series 上提取 n 个特征, 接着用 PCA 识别模式(principal components), 前两个 PC 被用于 二维异常检测算法, 从而发现top k 个异常值
- PCA 是一个降维的手段.
  - 一个 principal component 是原始变量经过线性变换后的组合
  - 越靠前的 principal component 解释(captures)的方差(variation)越多
  
# Features

- Mean: 均值
- Var: 方差
- ACF1: First order of autocorrelation ?
- Trend: Strength of trend [22]
- Linearity: 线性度
- Curvature: 曲率
- Season: Seasonality 季 [22]
- Peak: 峰 数量和位置
- Trough: 谷 数量和位置
- Entropy: spectral entropy 谱熵 [5]
- Lumpiness: 结块性 块度 (将一个series分为24个观测block 消除daily seasonality, 先计算每个block的方差, 接着计算这些方差的方差)
- Spikiness: 尖度 除了前两个principal component之外的components的交叉验证方差的方差 the variance of the leave-one-out variances of the remainder component.
- Lshift: level shift 连续24个观测block的最大均值差 the maximum difference in mean between consecutive blocks of 24 observations.
- Vchange: variance change 类似方差?
- Fspots: flat spot 把1个time series分为10个等宽
