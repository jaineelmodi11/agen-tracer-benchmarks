from typing import List


def string_xor(a: str, b: str) -> str:
    """ Input are two strings a and b consisting only of 1s and 0s.
    Perform binary XOR on these inputs and return result also as a string.
    >>> string_xor('010', '110')
    '100'
    """
    xor = ''
    for i in range(len(a)):
        if a[i] == b[i]:
            xor += '0'
        else:
            xor += '1'
    return xor[::-1]
