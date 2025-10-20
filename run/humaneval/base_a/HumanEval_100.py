
def make_a_pile(n):
    """
    Given a positive integer n, you have to make a pile of n levels of stones.
    The first level has n stones.
    The number of stones in the next level is:
        - the next odd number if n is odd.
        - the next even number if n is even.
    Return the number of stones in each level in a list, where element at index
    i represents the number of stones in the level (i+1).

    Examples:
    >>> make_a_pile(3)
    [3, 5, 7]
    """
    # Base case: if n is 0 or 1, return an empty list
    if n <= 1:
        return []

    # If n is even, add n/2 to the previous level and then add 1
    elif n % 2 == 0:
        return [n // 2] + make_a_pile(n // 2)

    # If n is odd, add n-1 to the previous level and then add 1
    else:
        return [n - 1] + make_a_pile(n - 1)

    # Example usage:
