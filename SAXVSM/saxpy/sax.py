"""Converts a normlized timeseries to SAX symbols."""
from collections import defaultdict
from saxpy.strfunc import idx2letter
from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.alphabet import cuts_for_asize

# 将time series转化为字符串
def ts_to_string(series, cuts):
    """A straightforward num-to-string conversion."""

    # - series中的一个时刻的数值 num, 在alphabet cuts中找对应的位置, 根据其位置转化为字母

    a_size = len(cuts)
    sax = list()
    for i in range(0, len(series)):
        num = series[i]
        
        # num >= 0 从后往前找对应字母 j = a_size - 1
        if(num >= 0):
            j = a_size - 1
            while ((j > 0) and (cuts[j] >= num)):
                j = j - 1
            sax.append(idx2letter(j))
            
        # num < 0 从前往后找对应字母 j = 1
        else:
            j = 1
            while (j < a_size and cuts[j] <= num):
                j = j + 1
            sax.append(idx2letter(j-1))
    return ''.join(sax)


def is_mindist_zero(a, b):
    """Check mindist."""
    if len(a) != len(b):
        return 0
    else:
        for i in range(0, len(b)):
            if abs(ord(a[i]) - ord(b[i])) > 1:
                return 0
    return 1


"""
sax_by_chunking

    1.PAA 对time series降维
    2.定义 alphabet cuts
    3.将降维的time series转化为字符串
"""
def sax_by_chunking(series, paa_size, alphabet_size=3, z_threshold=0.01):
    """Simple chunking conversion implementation."""
    paa_rep = paa(znorm(series, z_threshold), paa_size)
    cuts = cuts_for_asize(alphabet_size)
    return ts_to_string(paa_rep, cuts)


"""
sax_via_window

    将一个 time series 转化为 SAX字典 (key: 字符串, value: 窗口索引组成的列表)
"""
def sax_via_window(series, win_size, paa_size, alphabet_size=3,
                   nr_strategy='exact', z_threshold=0.01):
    """Simple via window conversion implementation."""
    
    # 生成指定size的alphabet cuts
    cuts = cuts_for_asize(alphabet_size)
    # 初始化sax
    sax = defaultdict(list)

    prev_word = ''

    for i in range(0, len(series) - win_size):
        
        # series被当前窗口所围住的子部分
        sub_section = series[i:(i+win_size)]
        
        # 标准化
        zn = znorm(sub_section, z_threshold)
        
        # PAA分段聚合 将子部分降维到paa_size维
        paa_rep = paa(zn, paa_size)

        # PAA后的序列转化为字符串
        curr_word = ts_to_string(paa_rep, cuts)

        # 
        if '' != prev_word:
            if 'exact' == nr_strategy and prev_word == curr_word:
                continue
            elif 'mindist' == nr_strategy and\
                    is_mindist_zero(prev_word, curr_word):
                continue

        prev_word = curr_word

        sax[curr_word].append(i)

    return sax
