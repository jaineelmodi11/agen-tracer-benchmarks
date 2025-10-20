

def prime_fib(n: int):
    """
    prime_fib returns n-th number that is a Fibonacci number and it's also prime.
    >>> prime_fib(1)
    2
    >>> prime_fib(2)
    3
    >>> prime_fib(3)
    5
    >>> prime_fib(4)
    13
    >>> prime_fib(5)
    89
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    # The first two numbers in the sequence are 0 and 1, which are not prime.
    # We need to check for primes up to sqrt(2) (which is approximately 1.414).
    if n <= 2:
        return n

    # Initialize variables
    a = 0
    b = 1
    c = 0

    while True:
        c = a + b
        a = b
        b = c

        # Check if c is prime
        if c > 1 and all(c % i != 0 for i in range(2, int(c**0.5) + 1)):
