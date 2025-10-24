

def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
    for i in range(2, n):
        if n % i == 0:
            return i
    return n

    # Test cases
    assert largest_divisor(15) == 5
    assert largest_divisor(8) == 2
    assert largest_divisor(13) == 1
    assert largest_divisor(100) == 50
    assert largest_divisor(1) == 1
    assert largest_divisor(2) == 2
    assert largest_divisor(3) == 3
    assert largest_divisor(4) == 2
    assert largest_divisor(6) == 3
    assert largest_divisor(7) == 7
    assert largest_divisor(10) == 5
    assert largest_divisor(11) == 11
    assert largest_divisor(12) == 6
    assert largest_divisor(13) == 13
    assert largest_divisor(14) == 7
    assert largest_divisor(15) == 5
    assert largest_divisor(16) == 4
    assert largest_divisor(17) == 17
    assert largest_divisor(18) == 6
    assert largest_divisor(19) == 19
    assert largest_divisor(20) == 10
    assert largest_divisor(21) == 7
    assert largest_divisor(22) == 11
    assert largest_divisor(23) == 23
    assert largest_divisor(24) == 12
    assert largest_divisor(25) == 5
    assert largest_divisor(26) == 13
    assert largest_divisor(27) == 9
    assert largest_divisor(28) == 4
    assert largest_divisor(29) == 29
    assert largest_divisor(30) == 10
    assert largest_divisor(31) == 31
    assert largest_divisor(32) == 16
    assert largest_divisor(33) == 33
    assert largest_divisor(34) == 17
    assert largest_divisor(35) == 5
    assert largest_divisor(36) == 6
    assert largest_divisor(37) == 37
    assert largest_divisor(38) == 19
    assert
