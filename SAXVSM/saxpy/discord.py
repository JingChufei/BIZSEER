"""Discord discovery routines. 发现 与其他子序列相似性最小的子序列 (两子序列不能有重复部分且不相邻)"""

# 问题: 边界条件问题 +1 -1

import numpy as np
from saxpy.visit_registry import VisitRegistry
from saxpy.distance import early_abandoned_dist
from saxpy.znorm import znorm

"""
暴力寻找 best discord
"""
def find_best_discord_brute_force(series, win_size, global_registry,
                                  z_threshold=0.01):
    """Early-abandoned distance-based discord discovery."""
    best_so_far_distance = -1.0
    best_so_far_index = -1

    outerRegistry = global_registry.clone()

    # 随机找到一个未看过的index
    outer_idx = outerRegistry.get_next_unvisited()

    # 若 outer_idx 不是nan值 则进入循环 ~按位取反
    while ~np.isnan(outer_idx):

        # 标记看过outer_idx
        outerRegistry.mark_visited(outer_idx)

        # 标准化候选子序列 开始索引outer_indx 结束索引outer_idx+win_size-1
        candidate_seq = znorm(series[outer_idx:(outer_idx+win_size)],
                              z_threshold)

        # 与candidate_seq的开始索引相距不小于窗口大小的 开始索引所代表的子序列 与其的最小距离 (两子序列形状相似)
        nnDistance = np.inf

        # 为什么不是 len(series) - win_size + 1 ???
        innerRegistry = VisitRegistry(len(series) - win_size)

        inner_idx = innerRegistry.get_next_unvisited()

        # 遍历所有开始索引 在两子序列距离大于窗口大小的条件下 找到与candidate_seq的最近距离nnDistance
        while ~np.isnan(inner_idx):
            innerRegistry.mark_visited(inner_idx)

            # 若 inner_indx 与 outer_idx 距离 大于 窗口大小 即两子序列不能有重复部分且不相邻
            if abs(inner_idx - outer_idx) > win_size:

                curr_seq = znorm(series[inner_idx:(inner_idx+win_size)],
                                 z_threshold)

                # 计算 标准化后两序列的欧式距离
                dist = early_abandoned_dist(candidate_seq,
                                            curr_seq, nnDistance)

                # 更新 nnDistance 使其逐渐变小
                if (~np.isnan(dist)) and (dist < nnDistance):
                    nnDistance = dist

            inner_idx = innerRegistry.get_next_unvisited()

        # 更新 best_so_far_distance 和 best_so_far_index
        """ 
        best_so_far_distance
            相似性最小的子序列 与 距离最近的子序列 的距离
        
        best_so_far_index
            最能代表当前时间序列的子序列 开始索引
            这段子序列在当前时间序列中与其他子序列的相似性是最小的
        """
        if ~(np.inf == nnDistance) and (nnDistance > best_so_far_distance):
            best_so_far_distance = nnDistance
            best_so_far_index = outer_idx

        outer_idx = outerRegistry.get_next_unvisited()

    return (best_so_far_index, best_so_far_distance)


def find_discords_brute_force(series, win_size, num_discords=2,
                              z_threshold=0.01):
    """Early-abandoned distance-based discord discovery. 找 num_discords 个 最具代表性的子序列"""
    discords = list()

    globalRegistry = VisitRegistry(len(series))

    # 为什么不是 len(series) - win_size + 1 ???
    globalRegistry.mark_visited_range(len(series) - win_size, len(series))

    while (len(discords) < num_discords):

        bestDiscord = find_best_discord_brute_force(series, win_size,
                                                    globalRegistry,
                                                    z_threshold)

        if -1 == bestDiscord[0]:
            break

        discords.append(bestDiscord)

        # 为什么不是 bestDiscord[0] - win_size + 1 ???
        mark_start = bestDiscord[0] - win_size
        if 0 > mark_start:
            mark_start = 0

        mark_end = bestDiscord[0] + win_size
        '''if len(series) < mark_end:
            mark_end = len(series)'''

        globalRegistry.mark_visited_range(mark_start, mark_end)

    return discords