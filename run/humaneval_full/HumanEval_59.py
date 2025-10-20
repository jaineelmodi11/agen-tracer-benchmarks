

def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    # If n is less than or equal to 1, return -1 since there are no prime numbers greater than 1
    if n <= 1:
    return -1

    # Initialize the largest prime factor as 1
    largest_prime = 1

    # Divide n by 2 until it becomes odd
    while n % 2 == 0:
    largest_prime =
