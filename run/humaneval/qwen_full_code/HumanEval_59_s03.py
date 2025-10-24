

def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    # Divide n by 2 to remove all even factors
    while n % 2 == 0:
        n //= 2

    # Now n must be odd, start checking from 3
    factor = 3
    while factor * factor <= n:
        # While factor divides n, divide n by factor
        while n % factor == 0:
            n //= factor
        # Increment factor by 2
        factor += 2

    # If n is a prime number greater than 2
    if n > 2:
        return n
