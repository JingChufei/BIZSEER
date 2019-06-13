# Abstract

- 提出一种ts分类算法 time series forest (TSF)
  - 在每个树节点随机选择特征, 只用一些简单的特征: mean, std, slope(斜率)
  - 具有时间序列长度的线性复杂度
  - 可用并行处理技术
- Entrance gain
  - entropy gain
  - distance measure
- temporal importance curve
  - 捕获 为时间序列分类提供有用信息的 时间特征

# Keywords

decision tree; ensemble; Entrance gain; interpretability; large margin; time series classification

# 1.Introduction

- NNEuclidean (one-nearest-neighbor with Euclidean distance)
  - 对时间轴变化敏感
- NNDTW (NN with dynamic time warping)
  - 对时间轴变化具有鲁棒性
  - 但难以提供解释性
- interval features 区间特征
  - 在时间序列区间上计算时间特征
  - 先前paper运用决策树 分裂节点用 entropy gain, 但很多分裂点具有相同的 entropy gain

# 2.Definition and Related Work

- 定义
  - 训练集: {e1, ..., ei, ..., eN}, 时间序列length为 M
  - label:  {y1, ..., yi, ..., yN}, where yi ∈ {1, 2, ..., C}

- ts 分类 可分为 1.instance-based 2.feature-based
  - instance-based 基于test实例与train实例的相似性
    - NNEuclidean
    - NNDTW
  - feature-based 1.定义时间特征 2.基于 定义的时间特征 训练分类器
    - [11] 仅捕获全局特征, 局部特征被忽略
    - [7] 对ts离散化后提取局部特征
    - [15] 区间特征 boosted binary stumps
    - [14] 决策树 SVM
    - [5] 考虑大量特征 虽然精确 但难以解释且计算昂贵
  - shapelets
    - 时间序列子序列
    - 某种程度上最大化代表一个class
    - 高可解释性
    
# 3. Interval Features

- interval features
  - ts区间上计算特征 如 时刻10与时刻30之间但区间
  - 倾向于选择 简单 且 可解释 但特征, 如 mean std slope
  
![image](https://github.com/JingChufei/BIZSEER/blob/master/images/interval%20feature.png)
  
本文用 随机森林但随机取样策略 将每个树节点的特征空间减少到O(M)

# 4.Time Series Forest Classifier

## 4.1 分类准则 splitting criterion

- <img src="http://chart.googleapis.com/chart?cht=tx&chl= f_{k}\left(t_{1}, t_{2}\right) \leq \tau" style="border:none;">
  
  - 满足上式的实例被分到左孩子节点 不满足则被分到右孩子节点

- <img src="http://chart.googleapis.com/chart?cht=tx&chl= f_{k}^{n}\left(t_{1}, t_{2}\right)" style="border:none;">

  - 表示 第n个训练实例 区间(t1, t2)的 第k个特征值
  - 对于一个node上所有训练实例(设为N个), 区间(t1, t2)的第k个特征值, 我们选择候选阈值, 使得将N个特征值分为等宽区间
  - 我们指定候选阈值的个数
  
- Entropy gain
  - Denote the proportions of instances corresponding to classes {1,2,...,C} at a tree node as {γ1,γ2,...,γC}, respectively. 
  
  - <img src="http://chart.googleapis.com/chart?cht=tx&chl= \text {Entropy }=-\Sigma_{c=1}^{C} \gamma_{c} \log \gamma_{c}" style="border:none;">

  - delta Entropy = (左孩子权重 * left Entropy + 右孩子权重 * right Entropy) - parent Entropy
    - 权重是实例个数占比
    - delta Entropy 在候选分裂过多时无法选出最佳分裂 (多个分裂delta Entropy相同)
    - 引入 Margin
    
- Margin
  - 计算 候选分裂阈值 与 其最近的特征值 之间的 distance距离
  
  - <img src="http://chart.googleapis.com/chart?cht=tx&chl= \text {Margin}=\min _{n=1,2, \ldots, N}\left|f_{k}^{n}\left(t_{1}, t_{2}\right)-\tau\right|" style="border:none;">

- Entrance (entropy and distance) gain
  - E = delta Entropy + alpha * Margin
  - Margin 对特征尺度scale 敏感, 可运用以下策略
    - 特征内选择阈值用 Entrance gain
    - 特征之间选择阈值用 delta Entropy
    
![image](https://github.com/JingChufei/BIZSEER/blob/master/images/entrance%20gain.png)
  
  倾向于选择 S3
    
## 4.2 Time Series Tree and Time Series Forest

### 4.2.1 随机取样策略

- 运用随机取样策略 将特征空间降低到 O(M), M为ts length

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/random%20sampling%20strategy.png)

### 4.2.2 ts tree 算法

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Time%20series%20tree.png)
  
### 4.2.3 ts forest TSF

- ts tree 的集合
- 根据所有 ts tree 的 votes 决定一个test instance 的分类

## 4.3 Computational Complexity

- 一个节点的计算复杂度为 O(nM) n为该节点的实例数 M为时间序列长度
- 一个ts tree 的复杂度 O(MNlogN)
- 有 nTree 个树的 ts forest (TSF) 复杂度 O(nTreeMNlogN) 这对于时间序列长度M来说是线性的

## 4.4 Temporal Importance Curve

- temporal importance curve
  - 为 ts 分类提供 解释力
  - 捕获 重要时间特征
  
- 特征k 时刻t 的重要性分数
  - SN 是 ts forest 的分裂节点集合
  - 求和项 是 节点v 特征(k, t1, t2) 的 entropy gain
  - 当该特征没有用于分裂节点v 那么该求和项为0

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Temporal%20Importance%20Curve.png)
  
![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Temporal%20Importance%20Curve%202.png)
  

  
  
  
  
  
  
