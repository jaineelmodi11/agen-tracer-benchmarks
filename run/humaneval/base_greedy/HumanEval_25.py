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
    # While i divides n, append i and divide n
    while n % i == 0:
        factors.append(i)
        n //= i
    # This condition is to handle the case when n is a prime number greater than 2
    if n > 2:
    factors.append(n)
    return factors
