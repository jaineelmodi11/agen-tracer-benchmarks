
def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    # If n is 1, there's only one number that starts or ends with 1, which is 1 itself.
    if n == 1:
    return 1

    # If n is 2, there are 2 numbers that start or end with 1: 10 and 11.
    if n == 2:
    return 2

    # For n > 2, there are 2^(n-1) numbers that start or end with 1.
    return 2 ** (n - 1)
