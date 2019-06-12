"""Implements HOT-SAX (a time series anomaly (discord) discovery algorithm) """
import numpy as np
from saxpy.znorm import znorm
from saxpy.sax import sax_via_window
from saxpy.distance import euclidean

# 在time series中 找 num_discords 个 异常 discord
def find_discords_hotsax(series, win_size=100, num_discords=2, a_size=3,
                         paa_size=3, z_threshold=0.01):
    """HOT-SAX-driven discords discovery."""
    discords = list()

    globalRegistry = set()

    while (len(discords) < num_discords):

        bestDiscord = find_best_discord_hotsax(series, win_size, a_size,
                                               paa_size, z_threshold,
                                               globalRegistry)

        if -1 == bestDiscord[0]:
            break

        discords.append(bestDiscord)

        mark_start = bestDiscord[0] - win_size
        if 0 > mark_start:
            mark_start = 0

        mark_end = bestDiscord[0] + win_size
        '''if len(series) < mark_end:
            mark_end = len(series)'''

        for i in range(mark_start, mark_end):
            globalRegistry.add(i)

    return discords


"""
1. 与 find_best_discord_brute_force函数 类似, 都是寻找该时间序列的异常
2. 但是加速该过程, 通过
    2.1 先在相同单词之间寻找最小距离, 再随机寻找最小距离
    2.2 计算两窗口距离后, 如果该距离小于当前的bestSoFarDistance, 则不需要计算当前窗口与其他窗口的最小距离
"""
def find_best_discord_hotsax(series, win_size, a_size, paa_size,
                             znorm_threshold, globalRegistry): # noqa: C901
    """Find the best discord with hotsax."""

    """
    [1.0] get the sax data first
        将一个 time series 转化为 SAX字典 (key: 字符串, value: 窗口索引组成的列表)
    """
    sax_none = sax_via_window(series, win_size, a_size, paa_size, "none", 0.01)

    """
    [2.0] build the 'magic' array
        magic_array: a list of tuples
        (字符串, 窗口索引个数)
    """
    magic_array = list()
    for k, v in sax_none.items():
        magic_array.append((k, len(v)))

    """
    [2.1] sort it desc by the key
        按照 窗口索引个数降序 对 tuple 排序
    """
    m_arr = sorted(magic_array, key=lambda tup: tup[1])

    """
    [3.0] define the key vars

    bestSoFarPosition
        bestSoFarDistance对应的窗口开始索引
        这个窗口是该时间序列具有代表性的子序列

    bestSoFarDistance
        max(min(distance))
        对于每一个窗口, 我们求出它与其他窗口的最小距离
        对所有的最小距离取一个最大值
    """
    bestSoFarPosition = -1
    bestSoFarDistance = 0.

    distanceCalls = 0

    visit_array = np.zeros(len(series), dtype=np.int)

    """[4.0] and we are off iterating over the magic array entries"""
    for entry in m_arr:

        """[5.0] some moar of teh vars"""
        curr_word = entry[0]
        # occurrences 当前word 的窗口索引列表
        occurrences = sax_none[curr_word]

        """[6.0] jumping around by the same word occurrences makes it easier to
        nail down the possibly small distance value 通过在相同的单词之间 跳转, 使得更容易确定可能的小距离值
         -- so we can be efficient and all that..."""

        # curr_pos 当前窗口索引 开始索引
        for curr_pos in occurrences:

            # 若 已经在 globalRegistry 跳出本次循环
            if curr_pos in globalRegistry:
                continue

            """[7.0] we don't want an overlapping subsequence"""
            # 避免 重复的子序列
            mark_start = curr_pos - win_size
            mark_end = curr_pos + win_size

            # 我们要找到 与 当前窗口 相似性最大的(距离最小的)窗口, 而 visit_set 定义我们已经看过的窗口的开始索引
            visit_set = set(range(mark_start, mark_end))

            """[8.0] here is our subsequence in question"""
            # cur_seq 标准化的子序列
            cur_seq = znorm(series[curr_pos:(curr_pos + win_size)],
                            znorm_threshold)

            """[9.0] let's see what is NN distance"""
            # 定义 nn_dist 为: 当前窗口 与 其他窗口 的最小距离 (两窗口 不能有重复部分 且 不能相邻?)
            nn_dist = np.inf
            # 定义 bool 是否进行随机搜索
            do_random_search = 1

            """[10.0] ordered by occurrences search first"""
            # 通过在相同的单词之间 跳转, 使得更容易确定可能的小距离值
            for next_pos in occurrences:

                """[11.0] skip bad pos"""
                # 避免 重复子序列
                if next_pos in visit_set:
                    continue
                else:
                    visit_set.add(next_pos)

                """[12.0] distance we compute"""
                dist = euclidean(cur_seq, znorm(series[next_pos:(
                                 next_pos+win_size)], znorm_threshold))
                distanceCalls += 1

                """[13.0] keep the books up-to-date"""
                # 更新 nn_dist
                if dist < nn_dist:
                    nn_dist = dist
                if dist < bestSoFarDistance:
                    do_random_search = 0
                    break

            """[13.0] if not broken above,
            we shall proceed with random search"""
            # 上面循环正常结束 并没有提前跳出 那我们就要进行随机搜索

            if do_random_search:
                """[14.0] build that random visit order array"""
                curr_idx = 0
                for i in range(0, (len(series) - win_size)): # 为什么不是 len(series) - win_size + 1

                    # 当前窗口开始索引 在上面没有查看过
                    if not(i in visit_set):

                        # 将其添加到 visit_array 中
                        visit_array[curr_idx] = i
                        curr_idx += 1

                # 此时 curr_idx 为 在上面没查看过的窗口开始索引的个数

                # 打乱顺序
                it_order = np.random.permutation(visit_array[0:curr_idx])
                curr_idx -= 1

                """[15.0] and go random"""

                while curr_idx >= 0:

                    # 随机选择 窗口开始索引 it_order[curr_idx]
                    rand_pos = it_order[curr_idx]

                    curr_idx -= 1

                    dist = euclidean(cur_seq, znorm(series[rand_pos:(
                                     rand_pos + win_size)], znorm_threshold))
                    distanceCalls += 1

                    """[16.0] keep the books up-to-date again"""

                    # 更新 nn_dist
                    if dist < nn_dist:
                        nn_dist = dist

                    if dist < bestSoFarDistance:
                        nn_dist = dist
                        break

            """[17.0] and BIGGER books"""

            # 更新 bestSoFarDistance 和 bestSoFarPosition
            if (nn_dist > bestSoFarDistance) and (nn_dist < np.inf):
                bestSoFarDistance = nn_dist
                bestSoFarPosition = curr_pos

    return (bestSoFarPosition, bestSoFarDistance)
