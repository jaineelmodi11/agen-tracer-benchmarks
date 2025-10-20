

def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
    for divisor in range(n - 1, 0, -1):
        if n % divisor == 0:
            return divisor


    # Test cases to verify the correctness of the function
    assert largest_divisor(15) == 5, "Test case 1 failed"
    assert largest_divisor(8) == 4, "Test case 2 failed"
    assert largest_divisor(7) == 1, "Test case 3 failed"

    print("All test cases passed!")import math
