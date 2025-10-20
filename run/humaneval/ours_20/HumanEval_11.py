from typing import List


def string_xor(a: str, b: str) -> str:
    """ Input are two strings a and b consisting only of 1s and 0s.
    Perform binary XOR on these inputs and return result also as a string.
    >>> string_xor('010', '110')
    '100'
    """
    # If characters at the same position in both strings are different, add 1 to the result
    if a[i] != b[i]:
        xor_result += '1'
    else:
        xor_result += '0'

    # Return the resulting string
    return xor_result
