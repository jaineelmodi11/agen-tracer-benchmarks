

def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    Certainly! To find the largest prime factor of a given number `n`, we can follow these steps:

    1. Start by dividing `n` by the smallest prime number, which is 2.
    2. Continue dividing `n` by 2 until it is no longer divisible by 2.
    3. Move on to the next smallest prime number, which is 3, and repeat the process.
    4. Continue this process until `n` is reduced to 1. The last number that divides `n` without leaving a remainder is the largest prime factor.

    Here's the implementation of the function:
