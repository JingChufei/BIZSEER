
# 1. Building

- pip install saxpy

# 2. Simple time series to SAX conversion

- To convert a time series of an arbitrary length to SAX we need to define the alphabet cuts. Saxpy retrieves cuts for a normal alphabet (we use size 3 here) via `cuts_for_asize` function
- 要将任意长度的时间序列转换为SAX, 我们需要定义字母切割. Saxpy通过`cuts_for_asize`函数检索正常字母表的切割, 这里用3


```python
from saxpy.alphabet import cuts_for_asize
cuts_for_asize(3)
```




    array([      -inf, -0.4307273,  0.4307273])



- To convert a time series to letters with SAX we use `ts_to_string` function but not forgetting to z-normalize the input time series (we use Normal alphabet)
- 要使用SAX将时间序列转换为字母, 我们使用`ts_to_string`函数, 但不要忘记对输入时间序列进行z标准化, 我们使用Normal字母表


```python
import numpy as np
from saxpy.znorm import znorm
from saxpy.sax import ts_to_string
# 参数 1. Z-norm后的time series 2. 字母切割
# -inf < -2 < -0.430 所以将 -2 转化为 a
ts_to_string(znorm(np.array([-2, 0, 2, 0, -1])), cuts_for_asize(3))
```




    'abcba'



# 3. Time series to SAX conversion with PAA aggregation (i.e., by "chunking")

- In order to reduce dimensionality further, the PAA (Piecewise Aggregate Approximation) is usually applied prior to SAX
- 为了进一步降低维数, PAA（分段聚合近似）通常在SAX之前应用


```python
import numpy as np
from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.sax import ts_to_string

dat = np.array([-2, 0, 2, 0, -1])
dat_znorm = znorm(dat) # array([-1.35680105,  0.15075567,  1.6583124 ,  0.15075567, -0.60302269])
# 参数 1. Z-norm后的time series 2. PAA超参数 分段数
# 返回 PAA处理后 将time series降维到 3维
dat_paa_3 = paa(dat_znorm, 3) # array([-0.75377836,  1.05528971, -0.30151134])

ts_to_string(dat_paa_3, cuts_for_asize(3))
```




    'acb'



# 4. Time series to SAX conversion via sliding window

- Typically, in order to investigate the input time series structure in order to discover anomalous (i.e., discords) and recurrent (i.e., motifs) patterns we employ time series to SAX conversion via sliding window. Saxpy implements this workflow
- 为了研究输入时间序列结构以发现异常discords和重复motifs模式, 我们通过滑动窗口使得时间序列进行SAX转换.

- `sax_via_window` is parameterised with a sliding window size, desired PAA aggregation, alphabet size, z-normalization threshold, and a numerosity reduction strategy as follows:
- `sax_via_window`参数: 滑动窗口大小, PAA聚合维数, 字母表大小, z标准化阈值和数字减少策略

```python3
def sax_via_window(series, win_size, paa_size, alphabet_size=3, nr_strategy='exact', z_threshold=0.01)
```


```python
import numpy as np
from saxpy.sax import sax_via_window

dat = np.array([0., 0., 0., 0., 0., -0.270340178359072, -0.367828308500142,
            0.666980581124872, 1.87088147328446, 2.14548907684624,
            -0.480859313143032, -0.72911654245842, -0.490308602315934,
            -0.66152028906509, -0.221049033806403, 0.367003418871239,
            0.631073992586373, 0.0487728723414486, 0.762655178750436,
            0.78574757843331, 0.338239686422963, 0.784206454089066,
            -2.14265084073625, 2.11325193044223, 0.186018356196443,
            0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.519132472499234,
            -2.604783141655, -0.244519550114012, -1.6570790528784,
            3.34184602886343, 2.10361226260999, 1.9796808733979,
            -0.822247322003058, 1.06850578033292, -0.678811824405992,
            0.804225748913681, 0.57363964388698, 0.437113583759113,
            0.437208643628268, 0.989892093383503, 1.76545983424176,
            0.119483882364649, -0.222311941138971, -0.74669456611669,
            -0.0663660879732063, 0., 0., 0., 0., 0.,])

sax1 = sax_via_window(dat, 6, 3, 3, "none", 0.01)

sax1
```




    defaultdict(list,
                {'aac': [4, 10, 11, 30, 35],
                 'abc': [12, 14, 36, 44],
                 'acb': [5, 16, 21, 37, 43],
                 'acc': [13, 52, 53],
                 'bac': [3, 19, 34, 45, 51],
                 'bba': [31],
                 'bbb': [15, 18, 20, 22, 25, 26, 27, 28, 29, 41, 42, 46],
                 'bbc': [2],
                 'bca': [6, 17, 32, 38, 47, 48],
                 'caa': [8, 23, 24, 40],
                 'cab': [9, 50],
                 'cba': [7, 39, 49],
                 'cbb': [33],
                 'cca': [0, 1]})



# 5. Time series discord discovery with HOT-SAX

- Saxpy implements HOT-SAX discord discovery algorithm in `find_discords_hotsax` function which can be used as follows:
- Saxpy在`find_discords_hotsax`函数中实现了HOT-SAX discord异常发现算法

- The function has a similar parameterization: sliding window size, PAA and alphabet sizes, z-normalization threshold, and a parameter specifying how many discords are desired to be found:
- 参数: 滑动窗口大小, PAA降维大小和字母表大小, z标准化阈值, 指定需要找到异常个数

```
def find_discords_hotsax(series, win_size=100, num_discords=2, a_size=3, paa_size=3, z_threshold=0.01)
```


```python
import numpy as np
from saxpy.hotsax import find_discords_hotsax
from numpy import genfromtxt
dd = genfromtxt("data/ecg0606_1.csv", delimiter=',')  
discords = find_discords_hotsax(dd)
discords
```




    [(430, 5.279080006171839), (318, 4.175756357308695)]


