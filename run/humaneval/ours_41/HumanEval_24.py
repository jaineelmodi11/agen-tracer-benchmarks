

def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
    if n % divisor == 0:
        return divisor
    return 1  # If no divisor is found, return 1 (since 1 is a divisor of every number)
