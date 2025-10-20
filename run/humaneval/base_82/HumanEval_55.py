

def fib(n: int):
    """Return n-th Fibonacci number.
    >>> fib(10)
    55
    >>> fib(1)
    1
    >>> fib(8)
    21
    """
    if n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

    # Test cases to verify the correctness of the function
    assert fib(10) == 55, "Test case for input 10 failed"
    assert fib(1) == 1, "Test case for input 1 failed"
    assert fib(8) == 21, "Test case for input 8 failed"

    print("All test cases passed!")import math
