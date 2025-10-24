

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
    if l[0] > l[1]:
        return False
    if l[0] < l[1]:
        return True
    for i in range(1, len(l)):
        if l[i] > l[i-1]:
            return False
        if l[i] < l[i-1]:
            return True
    return True
