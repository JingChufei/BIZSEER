"""Implements PAA."""

# 设置 paa_segments, 将series降维到 paa_segments维

import numpy as np


def paa(series, paa_segments):
    """PAA implementation."""
    series_len = len(series)

    # series长度 == PAA分段数, 则PAA后还是其本身
    if (series_len == paa_segments):
        return np.copy(series)
    else:
        
        # 初始化 res 元素个数为PAA分段数
        res = np.zeros(paa_segments)
        
        # series长度 整除 PAA分段数
        if (series_len % paa_segments == 0):
            
            # inc: series每一分段的长度
            inc = series_len // paa_segments
            
            # 将series中的每一时刻数值 累加到对应的分段中
            for i in range(0, series_len):
                idx = i // inc
                np.add.at(res, idx, series[i])
                # res[idx] = res[idx] + series[i]
                
            # 取均值
            return res / inc
        
        # 不能被整除
        else:
            # 将series长度扩充为 可以被整除的长度
            """
            例 series_len == 5 paa_segments == 3
            idx = 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2
            pos = 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4
            res[0] = series[0] + series[0] + series[0] + series[1] + series[1]
            res[1] = series[1] + series[2] + series[2] + series[2] + series[3]
            res[2] = series[3] + series[3] + series[4] + series[4] + series[4]
            """
            for i in range(0, paa_segments * series_len):
                idx = i // series_len
                pos = i // paa_segments
                np.add.at(res, idx, series[pos])
                # res[idx] = res[idx] + series[pos]
                
            # 取均值
            return res / series_len
