"""Implements znorm. 实现Z标准化"""
import numpy as np


def znorm(series, znorm_threshold=0.01):
    """Znorm implementation."""

    sd = np.std(series)

    # 标准差小于阈值 则不用标准化
    if (sd < znorm_threshold):
        return series

    mean = np.mean(series)
    
    return (series - mean) / sd