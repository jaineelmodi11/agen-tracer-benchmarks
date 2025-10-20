

def modp(n: int, p: int):
    """Return 2^n modulo p (be aware of numerics).
    >>> modp(3, 5)
    3
    >>> modp(1101, 101)
    2
    >>> modp(0, 101)
    1
    >>> modp(3, 11)
    8
    >>> modp(100, 101)
    1
    """
    raise ValueError("Both n and p must be integers.")

    # If n is zero, return 1 because any number raised to the power of 0 is 1.
    if n == 0:
    return 1

    #
