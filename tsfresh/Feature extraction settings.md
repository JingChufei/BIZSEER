- `tsfresh.extract_features()`调参 
  - default_fc_parameters
  - kind_to_fc_parameters
 
 ## set the parameters for all kind of time series
- `default_fc_parameters`: dict 字典
  - key: **feature calculator names 特征计算器名称** (`tsfresh.feature_extraction.feature_calculators`中的方法)
  - vaule: **a list of dicts 多个字典组成的列表**
    - dict
      - key: **parameter name 参数名称**
      - value: **parameters value 参数值**
 ### example
 ```python3
 fc_parameters = {
    "length": None,
    "large_standard_deviation": [{"r": 0.05}, {"r": 0.1}]
}
 ```
 将会生成3个特征
 - 1个特征: 调用`tsfresh.feature_extraction.feature_calculators.length()`没有参数
 - 2个特征: 调用`tsfresh.feature_extraction.feature_calculators.large_standard_deviation()`分别以 r=0.05 和 r=0.1 为参数
 如果不想生成length特征, 则
 ```python3
 del fc_parameters["length"]
 ```
 ### 预先定义的3个settings
 - `tsfresh.feature_extraction.settings.ComprehensiveFCParameters`: 包含所有特征的不同参数组合
 - `tsfresh.feature_extraction.settings.MinimalFCParameters`: 具有“minimal”属性的特征会被使用, 可用来quick test
 - `tsfresh.feature_extraction.settings.EfficientFCParameters`: 在comprehensive的基础上去掉具有“high_comp_cost”属性的特征, 加快速度
 ### 代码
 ```python3
from tsfresh.feature_extraction import ComprehensiveFCParameters
settings = ComprehensiveFCParameters()
# Set here the options of the settings object as shown in the paragraphs below
# ...
from tsfresh.feature_extraction import extract_features
extract_features(df, default_fc_parameters=settings)
 ```
  
 ## set the parameters for different type of time series
 - `kind_to_fc_parameters` = {“kind” : fc_parameters}
  - key: kind names (str)
  - value: *fc_parameters* 实例
### example
```python3
kind_to_fc_parameters = {
    "temperature": {"mean": None},
    "pressure": {"max": None, "min": None}
}
```
将生成3个特征
- 1个特征
  - 提取 temperature 的 mean 特征
- 2个特征:
  - 提取 pressure 的 max 特征
  - 提取 pressure 的 min 特征
### 注意
kind_to_fc_parameters 优先级 高于 default_fc_parameters

## 实战操作
- 先利用特征选择算法找出相关性较高的特征
- 再用`tsfresh.feature_extraction.settings.from_columns()`方法生成 kind_to_fc_parameters
  - 参数: 特征选择后的矩阵
  - 返回: 字典 即 kind_to_fc_parameters
```python3
# X_tsfresh containes the extracted tsfresh features
X_tsfresh = extract_features(...)

# which are now filtered to only contain relevant features
X_tsfresh_filtered = some_feature_selection(X_tsfresh, y, ....)

# we can easily construct the corresponding settings object
kind_to_fc_parameters = tsfresh.feature_extraction.settings.from_columns(X_tsfresh_filtered)
```
## 参考
https://tsfresh.readthedocs.io/en/latest/text/feature_extraction_settings.html
