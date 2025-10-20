

def fib(n: int):
    """Return n-th Fibonacci number.
    >>> fib(10)
    55
    >>> fib(1)
    1
    >>> fib(8)
    21
    """
    # Initialize the list with the first two Fibonacci numbers
    fib_sequence = [1, 1]

    # If n is less than 2, return the corresponding value from the list
    if n < 2:
    return fib_sequence[n-1]

    # Generate the rest of the sequence using a loop
    for i in range(2, n):
    next_fib = fib_sequence[-1] + fib_sequence[-2]
