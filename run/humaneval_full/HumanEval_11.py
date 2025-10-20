from typing import List


def string_xor(a: str, b: str) -> str:
    """ Input are two strings a and b consisting only of 1s and 0s.
    Perform binary XOR on these inputs and return result also as a string.
    >>> string_xor('010', '110')
    '100'
    """
    # Perform bitwise XOR on the current characters
    xor_result += str(int(a[i]) ^ int(b[i]))

    return xor_result
