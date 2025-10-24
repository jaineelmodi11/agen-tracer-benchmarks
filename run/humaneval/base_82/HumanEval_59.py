

def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    """
    Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    # Initialize the largest prime factor to the smallest prime number
    largest_prime = 2

    # Divide n by the largest prime factor until it's no longer divisible
    while n % largest_prime == 0:
    n //= largest_prime

    # If n is still greater than 1, then the largest prime factor is the last largest prime factor found
    if n > 1:
    return largest_prime
    else:
    return n
