

def fizz_buzz(n: int):
    """Return the number of times the digit 7 appears in integers less than n which are divisible by 11 or 13.
    >>> fizz_buzz(50)
    0
    >>> fizz_buzz(78)
    2
    >>> fizz_buzz(79)
    3
    """
    if i % 11 == 0 or i % 13 == 0:
        num_str = str(i)
        count += sum(1 for digit in num_str if digit == '7')
    return count
