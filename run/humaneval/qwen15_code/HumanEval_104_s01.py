
def unique_digits(x):
    """Given a list of positive integers x. return a sorted list of all 
    elements that hasn't any even digit.

    Note: Returned list should be sorted in increasing order.
    
    For example:
    >>> unique_digits([15, 33, 1422, 1])
    [1, 15, 33]
    >>> unique_digits([152, 323, 1422, 10])
    []
    """
    while n > 0:
        if n % 2 == 0:
            return True
        n //= 10
    return False

    return sorted(set(filter(lambda num: not has_even_digit(num), x)))
