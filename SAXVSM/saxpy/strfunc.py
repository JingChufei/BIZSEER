"""Convert a normlized timeseries to SAX symbols."""


def idx2letter(idx):
    """Convert a numerical index to a char. 将数字索引转化为字母 0 a, 1 b ..."""
    if 0 <= idx < 20:
        return chr(97 + idx)
    else:
        raise ValueError('A wrong idx value supplied.')