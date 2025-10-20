from typing import List


def factorize(n: int) -> List[int]:
    """ Return list of prime factors of given integer in the order from smallest to largest.
    Each of the factors should be listed number of times corresponding to how many times it appeares in factorization.
    Input number should be equal to the product of all factors
    >>> factorize(8)
    [2, 2, 2]
    >>> factorize(25)
    [5, 5]
    >>> factorize(70)
    [2, 5, 7]
    """
    To solve this problem, we need to find the prime factors of a given number `n` such that each prime factor appears as much as it does in the factorization of `n`. Here's a corrected version of your code:

    ```python
    from typing import List
