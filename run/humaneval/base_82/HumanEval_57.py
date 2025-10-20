

def monotonic(l: list):
    """Return True is list elements are monotonically increasing or decreasing.
    >>> monotonic([1, 2, 4, 20])
    True
    >>> monotonic([1, 20, 4, 10])
    False
    >>> monotonic([4, 1, 0, -10])
    True
    """
    if l == []:
        return True
    elif l[0] > l[-1]:
        return all(monotonic(sublist) for sublist in l[1:-1])
    else:
        return any(monotonic(sublist) for sublist in l[:-1])

    # Test cases to verify the correctness of the function
