"""Implements VSM."""

import math
import numpy as np
from saxpy.sax import sax_via_window


def series_to_wordbag(series, win_size, paa_size, alphabet_size=3,
                      nr_strategy='exact', z_threshold=0.01):
    """VSM implementation."""
    sax = sax_via_window(series, win_size, paa_size, alphabet_size,
                         nr_strategy, z_threshold)

    # convert the dict to a wordbag
    frequencies = {}
    # v 是list
    for k, v in sax.items():
        frequencies[k] = len(v)

    # key: 字符串 # value: 词频
    return frequencies


def manyseries_to_wordbag(series_npmatrix, win_size, paa_size, alphabet_size=3,
                          nr_strategy='exact', z_threshold=0.01):
    """VSM implementation."""
    # 将多个series转化为wordbag

    frequencies = {}

    # series_npmatrix每一行是一个series
    for row in series_npmatrix:
    	# asarray同array 不占内存
    	# squeeze 删除单维 shape(1, 2) 变为 shape(2, )
        tmp_freq = series_to_wordbag(np.squeeze(np.asarray(row)),
                                     win_size, paa_size, alphabet_size,
                                     nr_strategy, z_threshold)
        for k, v in tmp_freq.items():
            if k in frequencies:
                frequencies[k] += v
            else:
                frequencies[k] = v

    # key: 字符串 value: 在series_npmatrix出现频率
    return frequencies

# a bag == a class
# a class 中有很多 series

# bags_dict: key: class_name str; value: wordbag dict
def bags_to_tfidf(bags_dict):
    """VSM implementation."""

    # classes
    count_size = len(bags_dict)
    # 将字典拆开 只显示key
    classes = [*bags_dict.copy()]

    # word occurrence frequency counts
    # key: word字符串 str value: 列表 元素为对应class的词频
    counts = {}

    # compute frequencies

    # idx 表示当前的class
    idx = 0
    
    # name 当前class
    for name in classes:
        for word, count in bags_dict[name].items():
            if word in counts:
                counts[word][idx] = count
                
            # word 在counts中不存在
            else:
            	# 添加 key: word; value: list 长度为count_size 即class的个数
                counts[word] = [0] * count_size
                counts[word][idx] = count
        idx = idx + 1

    # compute tf*idf
    tfidf = {}  # the resulting vectors dictionary
    idx = 0

    # freqs 是列表 元素为对应class的词频
    for word, freqs in counts.items():

        # document frequency
        # df_counter: 包含word的class个数
        df_counter = 0

        for i in freqs:
            if i > 0:
                df_counter = df_counter + 1

        # if the word is everywhere, dismiss it
        # 如果某一word在每个class中都出现了, 那么忽略这个word
        if df_counter == len(freqs):
            continue

        # tf*idf vector
        tf_idf = [0.0] * len(freqs)

        # 当前class
        i_idx = 0

        for i in freqs:
            if i != 0:
                tf = np.log(1 + i)
                idf = np.log(len(freqs) / df_counter)
                tf_idf[i_idx] = tf * idf
            i_idx = i_idx + 1

        tfidf[word] = tf_idf

        idx = idx + 1

    return {"vectors": tfidf, "classes": classes}


# 返回vector_label所代表class的tfidf向量
def tfidf_to_vector(tfidf, vector_label):
    """VSM implementation."""
    if vector_label in tfidf['classes']:
    	
    	# 找出vector_label第一个匹配项的索引位置, 即找到vector_label是第几个class
        idx = tfidf['classes'].index(vector_label)

        """
		key: word
		value: tfidf值
        """
        weight_vec = {}

        """
		tfidf['vectors'] 是一个dict
			key: word
			value: 列表
				元素为对应class的tfidf值
        """
        for word, weights in tfidf['vectors'].items():
        	# 找到 当前word 指定class 即idx 的tfidf值
            weight_vec[word] = weights[idx]

        return weight_vec
    else:
        return []


# test_bag 与 weight_vec(某个class的word权重向量) 的余弦相似性
def cosine_measure(weight_vec, test_bag):
    """VSM implementation."""
    sumxx, sumxy, sumyy = 0, 0, 0

    # set union 取并集
    for word in set([*weight_vec.copy()]).union([*test_bag.copy()]):
    	"""
		x: word在weight_vec中的tfidf值
		y: word在test_bag中的tfidf值?
    	"""
        x, y = 0, 0
        if word in weight_vec.keys():
            x = weight_vec[word]
        if word in test_bag.keys():
            y = test_bag[word]

        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    return sumxy / math.sqrt(sumxx * sumyy)



def cosine_similarity(tfidf, test_bag):
    """VSM implementation."""

    """
	key: class
	value: 1 - 余弦相似性
    """
    res = {}

    for cls in tfidf['classes']:
    	# 为什么要用 1 - 余弦相似性
        res[cls] = 1. - cosine_measure(tfidf_to_vector(tfidf, cls), test_bag)

    return res


def class_for_bag(similarity_dict):
    # do i need to take care about equal values?
    # 找到 similarity_dict 中最小 value 的 key
    return min(similarity_dict, key=lambda x: similarity_dict[x])

