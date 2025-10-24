

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
    Certainly! The function `modp` computes \(2^n \mod p\) using Python's built-in `pow` function, which is efficient and handles large numbers well. Here's the complete function:
