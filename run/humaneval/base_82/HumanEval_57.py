

def monotonic(l: list):
    """Return True is list elements are monotonically increasing or decreasing.
    >>> monotonic([1, 2, 4, 20])
    True
    >>> monotonic([1, 20, 4, 10])
    False
    >>> monotonic([4, 1, 0, -10])
    True
    """
    """Return True if list elements are monotonically increasing or decreasing.
    >>> monotonic([1, 2, 4, 20])
    True
    >>> monotonic([1, 20, 4, 10])
    False
    >>> monotonic([4, 1, 0, -10])
    True
    """
    # Check if the list is empty or has only one element
    if len(l) <= 1:
    return True

    # Compare each element with the next one
    for i in range(len(l) - 1):
    if l[i] < l[i + 1]:
        return False
    elif l[i] > l[i + 1]:
        return True

    # If we reach here, the list is monotonically increasing
    return True
