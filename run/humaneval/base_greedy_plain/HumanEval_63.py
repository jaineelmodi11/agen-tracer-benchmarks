

def fibfib(n: int):
    """The FibFib number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:
    fibfib(0) == 0
    fibfib(1) == 0
    fibfib(2) == 1
    fibfib(n) == fibfib(n-1) + fibfib(n-2) + fibfib(n-3).
    Please write a function to efficiently compute the n-th element of the fibfib number sequence.
    >>> fibfib(1)
    0
    >>> fibfib(5)
    4
    >>> fibfib(8)
    24
    """
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 0
    elif n == 3:
        return 1
    else:
        return fibfib(n-1) + fibfib(n-2) + fibfib(n-3)

    # Test cases
    assert fibfib(1) == 0
    assert fibfib(5) == 4
    assert fibfib(8) == 24
    assert fibfib(10) == 104
    assert fibfib(15) == 149

    # Check if the function works correctly
