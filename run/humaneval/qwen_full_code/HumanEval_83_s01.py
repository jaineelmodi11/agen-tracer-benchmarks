
def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    if n == 1:
        return 1
    else:
        # For n > 1, there are 2^(n-1) possible n-digit numbers,
        # but we subtract 1 to exclude those that both start and end with 1.
        return 2**(n-1) - 1
