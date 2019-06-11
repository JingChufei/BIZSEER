# Abstract

- SAX-VSM 识别时间序列的特征, 基于Symbolic Aggregate approXimation和Vector Space Model
- SAX-VSM 通过 时间序列pattern 对class的重要性, 自动识别并排序 pattern, 这有利于分类和解释
- SAX-VSM 学习过程相对耗时

# Keywords

- time series analysis
- classification algorithms

# 3.Background

- SAX
  - 将 time series 转化为 SAX词 或 SAX词的字典
    - sax_by_chunk: 转化为字符串
    - sax_via_window: 字符串的字典
      - key: word str
      - value: 窗口索引组成的列表 list
      
- VSM
  - 运用 tf*idf权重, 将 字符串的字典 转化为 class特征权重向量
  - 接着 基于 余弦相似性 做分类
  
- DIRECT dividing rectangles algorithm
  - 运用 DIRECT 选择 SAX参数 
    - P: the number of PAA segments per window 在每个window中运用PAA降维
    - A: alphabet size 字母表大小
    
## 3.1 Symbolic Aggregate approXimation (SAX)

- SAX 将time series转化为字符串, 可以对time series进行降维
- 参数
  - word size 转化为字符串的长度
  - alphabet size 字符串中可选字符的个数
- 步骤
  - Z-normalization
  - PAA降维 将time series长度减小到word size (均值)
  - 降维后的time series中每一个数值 在字母表中找对应字母, 从而将time series转化为字符串 (标准正态分布)
  
## 3.2 Bag of words representation of time series

- SAX 可以用来发现time series的 motifs 模式 和 discords 噪音
- 运用 sliding window
  - T is a time seires, length is n
  - sliding window length is l
  - 将每一个窗口所框起来的子时间序列转化为一个字符串
  - 将 time series 转化为 m 个字符串, 其中 m = n - l + 1
  - 得到 bag of words, 表示原始时间序列T (分类的情况下, a bag == a class)
  
## 3.3 Vector Space Model (VSM) adapation

- 定义
  - *term*: a single SAX word
  - *bag of words*: word字典 代表一个class
    - key: word
    - value: 词频 或其他
  - *corpus*: a set of bags 所有class
  - *weight matrix*: 在corpus中定义所有word的权重
    - 行: word
    - 列: class
    
- 算法描述
  - 给定训练集, 用 sliding window 和 SAX 处理每一个 time series, 为每一个class建立一个bag of SAX words
  - 所有 bags 组合成 corpus
    - 行 代表word (所有class中找到的)
    - 列 代表class
    - 每一个元素表示 在一个class中一个word的观测频率 (corpus通常是稀疏的)
  - 用 tf*idf 将频率转化为权重系数
    - https://zh.wikipedia.org/wiki/Tf-idf
    - tf 定义不同于wikipedia 见paper
  - weight matrix 中的列 被作为 class term weight vectors 用于分类 (余弦相似性)
    - https://zh.wikipedia.org/wiki/%E4%BD%99%E5%BC%A6%E7%9B%B8%E4%BC%BC%E6%80%A7
    
# 4.SAX-VSM classification algorithm

- two phases - training and classification

## 4.1 Training phase

- 给定三个参数 
  - W: the sliding window length 
  - P: the number of PAA segments per window
  - A: SAX alphabet size
- 将 带标签的time series 转化为 SAX代表
- 每个子时间序列运用PAA之前, 对其进行Z标准化, 若标准差低于阈值, 则不用标准化
- 在N个class的所有时间序列上运用算法生成N个bag的corpus, 接着运用tf*idf生成N个class weight vector
- 所有数据集都要被训练, 时间复杂度O(nm), 但训练完后只保留N个weight vector, 无需保留corpus

## 4.2 Classification

- unlabeled time series 转化为 term frequency vector
  - 对于一个给定的 unlabeled time series
  - SAX-VSM用与训练集相同的sliding window和SAX参数
  - 将其转化为terms frequency vector
- classification
  - 计算 term frequency vector 与 N个 tf*idf weight vector 的余弦相似性
  - 选择最大的作为其分类

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/An%20overview%20of%20SAX-VSM%20algorithm.png)

## 4.3 Sliding window size and SAX parameters selection

- 用 交叉验证 和 DIRECT最佳化方案 调参(W P A)
- DIRECT 迭代两个过程 1.划分搜索域 2.识别最佳超矩形
  - 首先将搜索域缩放为3维立方体，这被认为是潜在的最佳
  - 然后在该立方体的中心评估误差函数
  - 接下来，在所有坐标方向上距离中心的距离的三分之一处创建其他点
  - 然后将超立方体分成较小的矩形，这些矩形由它们的中心点和它们的误差函数值识别
  - 该过程以交互方式继续，直到误差函数收敛
  
![image](https://github.com/JingChufei/BIZSEER/blob/master/images/DIRECT.png)
  
## 4.4 Intuition behind SAX-VSM

- SAX-VSM 捕获capture和概括generalize训练集的类内可变性
- SAX-VSM 捕获和识别 由噪声或信号丢失造成失真和破坏的时间序列中的 具有代表性的子序列, 通过标准化子序列和丢弃原始顺序
- tf*idf 提高了分类的选择性selectivity 通过降低class中都出现word的权重 提高可以定义class的word的权重
- 一个未知时间序列 通过比较 其子序列 与 在整个class中发现的已知判别模式 的相似性 来进行分类
