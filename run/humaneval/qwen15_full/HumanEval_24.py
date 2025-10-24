

def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
    if n % i == 0:
        return i
    return 1  # If no divisor is found, return 1 (since 1 is the smallest divisor)
