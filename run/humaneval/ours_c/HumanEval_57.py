

def monotonic(l: list):
    """Return True is list elements are monotonically increasing or decreasing.
    >>> monotonic([1, 2, 4, 20])
    True
    >>> monotonic([1, 20, 4, 10])
    False
    >>> monotonic([4, 1, 0, -10])
    True
    """
    if not l:
        return True
    for i in range(1, len(l)):
        if l[i] > l[i-1]:
            return False
    return True


    # Test cases to verify the correctness of the function
