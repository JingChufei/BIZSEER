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

# 5. Result

做了一些实验来证明SAX-VSM的性能并展示其为分类结果提供洞察的能力

## 5.1 Analysis of the classification

- 在来自UCR repository的45个datasets上评估算法
- 与其他分类算法进行比较, 定位SAX-VSM分类的准确性和解释性
  - 基于欧式距离的1NN分类器
  - 基于DTW的1NN分类器
  - 基于Fast-Shapelets技术的分类器
  - 基于BOP的分类器
  
## 5.2 Scalability analysis 可扩展性

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Scalability%20analysis.png)

- 图left: dataset size增大, SAX-VSM与1NN Euclidean无显著差异
- 图center: SAX-VSM训练好后可以丢弃训练集, 只保留weight vectors
- 随着训练集size增大, SAX-VSM的word数量逐渐趋于饱和, 这表明SAX-VSM高效学习大量数据集的能力

## 5.3 Robustness to noise

- 图right: 通过改变CPF模型中高斯噪音的标准差, SAX-VSM的误差率优于1-NN Euclidean
- fine tuning of smoothing: SAX sliding window size随着噪音水平成比例增大, SAX-VSM性能增强

## 5.4 Interpretable classification

- SAX-VSM一次性提取所有pattern并赋予权重, 是许多class问题的interpretable分类器的唯一选择
- 这里我们举几个挖掘子序列权重的例子

### 5.4.1 Heatmap-like visualization

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Heatmap-like%20visualization.png)

- 由于SAX-VSM输出从类中提取的所有子序列的tf * idf权重向量, 因此可以知道任意一个子序列的权重
- 该功能实现了一种新颖的热图式视觉化技术, 可以立即深入了解 “重要”类特征子序列 的布局
  - 对于Cylinder类, 重要的子序列 先陡峭上升, 然后平稳, 最后陡峭下降
  - 对于Bell类, 重要的子序列 逐渐上升
  - 对于Funnel类, 重要的子序列 先陡峭上升 然后逐渐下降
  
### 5.4.2 Gun Point dataset

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Gun%20Point%20dataset.png)

- GunPoint dataset
  - Gun class: 人拔枪的手部动作——从髋关节安装的枪套中取出复制枪时，将其指向目标一秒钟，并将枪返回枪套
  - Point class: 人假装拔枪的手部动作——将食指指向目标约一秒钟，然后将双手放回两侧
- SAX-VSM能够捕获所有distinguishing feature

### 5.4.3 OSU Leaf dataset

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/OSU%20Leaf%20dataset.png)

- OSU Leaf dataset
  - six classes
  - 通过彩色图像分割和六类数字化叶图像的边界提取获得的曲线组成
- DTW分类 准确率61% 但无法提供解释
- SAX-VSM为六类中的每一类产生了一组class-specific characteristic patterns类特定的特征模式, 如图所示. 89%准确率.
  
### 5.4.4 Coffee dataset

![image](https://github.com/JingChufei/BIZSEER/blob/master/images/Coffee%20dataset.png)

- 与基于PCA的先前工作类似，SAX-VSM在两类咖啡谱图中突出显示对应于绿原酸（最佳）和咖啡因（第二至最佳）的间隔
- 这两种化合物不仅已知是阿拉比卡咖啡和罗布斯塔咖啡风味差异的原因, 而且是之前提出用于即食咖啡的工业质量分析
# 6.Conclusion and Future work

- 我们提出了一种基于 特征模式发现 的时间序列分类的新颖可解释技术 SAX-VSM
- 我们证明了SAX-VSM在一组经典数据挖掘问题上与其他技术竞争或优于其他技术
- 我们描述了SAX-VSM相对于现有基于结构的相似性度量的几个优点, 强调了它 发现和排序短子序列 的能力
- 我们概述了SAX参数选择的有效解决方案 DIRECT
- 我们未来的工作
  - 优先考虑修改我们的算法用于可变长度的单词
  - 探索SAX-VSM对 多维时间序列 的适用性

### 5.4.4 Coffee 
