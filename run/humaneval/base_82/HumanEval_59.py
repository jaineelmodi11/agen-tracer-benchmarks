

def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    # Initialize the smallest prime factor to 2 (the only even prime number)
    p = 2

    # Divide n by the current prime factor until it's no longer divisible
    while n % p == 0:
        n //= p

    # If n becomes 1, return the next prime number after p
    if n == 1:
        return p + 2
    else:
        return p

    # Check function to verify the correctness of the solution
