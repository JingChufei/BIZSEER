

# Abstract
- M3 data 是一个 time series 集合
- 本文计算每个time series的6个特征, 并用PCA降维, 使得每个time series投影到2维实例空间(PC1, PC2)

# Keywords
M3-Competition; Time series visualisation; Time series generation; Forecasting algorithm comparison.

# 1 Introduction
- M3 data
  - time series数据, all positive
  - domains: demography, finance, business and economics
  - length: [14, 126]
  - frequencies: observed annually, quarterly, monthly
  
- 计算每个time series的"features"
  - 每个feature都是规定的数值计算
  - time series 转化为 静态数据, 即1个time series转化为高维特征空间中的1个点
  - 应用PCA降维, 将 高维空间 转化为 二维空间
  - 这可以被用来 1.分类 2.聚类 3.识别异常time series 4.探索给定time series集合的属性
  
# 2 Time series features
## Spectral entropy F1 谱熵
<img src="http://chart.googleapis.com/chart?cht=tx&chl=F_{1}=-\int_{-\pi}^{\pi} \hat{f}_{x}(\lambda) \log \hat{f}_{x}(\lambda) d \lambda" style="border:none;">

- 时间序列 x_t 的谱密度 f_x(lambda) 的 香农熵估计
- 评估信号的复杂度, 衡量一个time series的可预测性
- F1越大, 表明未来更多的不确定性, time series更难预测

## Strength of trend F2 趋势强度
<img src="http://chart.googleapis.com/chart?cht=tx&chl=F_{2}=1-\frac{\operatorname{var}\left(R_{t}\right)}{\operatorname{var}\left(x_{t}-S_{t}\right)}" style="border:none;">

- STL decomposition STL分解 将time series x_t 分解为 trend T_t, season S_t, remainder R_t
- 衡量1个time series的均值水平长期变化的程度
- F2越大
