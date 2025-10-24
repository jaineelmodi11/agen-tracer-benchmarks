

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
    To complete the function `modp(n: int, p: int)`, you need to ensure that the input `n` is a non-negative integer less than `p`. If `n` is not within the valid range, the function should return `None`. Here's the complete implementation:

    ```python
