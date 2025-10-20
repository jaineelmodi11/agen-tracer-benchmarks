

def greatest_common_divisor(a: int, b: int) -> int:
    """ Return a greatest common divisor of two integers a and b
    >>> greatest_common_divisor(3, 5)
    1
    >>> greatest_common_divisor(25, 15)
    5
    """
    while b != 0:
        a, b = b, a % b
    return a


    # Test cases
    assert greatest_common_divisor(3, 5) == 1
    assert greatest_common_divisor(25, 15) == 5
    assert greatest_common_divisor(7, 14) == 7
    assert greatest_common_divisor(8, 16) == 8
    assert greatest_common_divisor(10, 20) == 10
    assert greatest_common_divisor(100, 99) == 1
    assert greatest_common_divisor(100, 99) == 1
    assert greatest_common_divisor(100, 99) ==
