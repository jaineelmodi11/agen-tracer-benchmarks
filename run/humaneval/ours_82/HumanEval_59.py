

def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    # Initialize the largest prime factor to 1
    largest_prime = 1

    # Divide n by 2 to remove all even factors
    while n % 2 == 0:
    largest_prime = 2
    n //= 2

    # Now n must be odd, so we can skip one element (Note i = i + 2)
    for i in range(3, int(n**0.5) + 1, 2):
    while n % i == 0:
        largest_prime = i
        n //= i

    # This condition is to handle the case when n is a prime number greater than 2
    if n > 2:
    largest_prime = n

    return largest_prime
