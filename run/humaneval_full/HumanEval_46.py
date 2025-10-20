

def fib4(n: int):
    """The Fib4 number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:
    fib4(0) -> 0
    fib4(1) -> 0
    fib4(2) -> 2
    fib4(3) -> 0
    fib4(n) -> fib4(n-1) + fib4(n-2) + fib4(n-3) + fib4(n-4).
    Please write a function to efficiently compute the n-th element of the fib4 number sequence.  Do not use recursion.
    >>> fib4(5)
    4
    >>> fib4(6)
    8
    >>> fib4(7)
    14
    """
    # Initialize a list to store Fibonacci numbers up to n
    fib_sequence = [0] * (n + 1)

    # Base cases for the first four elements
    if n == 0:
    return 0
    elif n == 1:
    return 0
    elif n == 2:
    return 2

    # Fill the rest of the sequence
    for i in range(3, n + 1):
    fib_sequence[i] = fib_sequence[i - 1] +
